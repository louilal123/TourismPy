from flask import Flask, render_template
import pandas as pd
import os

# Initialize Flask app
app = Flask(__name__)

# Define the correct path to the dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get absolute path
DATA_FOLDER = os.path.join(BASE_DIR, "templates", "data")
DATA_FILE = os.path.join(DATA_FOLDER, "Tourist_Destinations_Philippines.csv")

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
    print("✅ Created missing 'templates/data' directory.")

# Check if dataset exists
if not os.path.exists(DATA_FILE):
    print(f"❌ ERROR: Dataset '{DATA_FILE}' not found.")
else:
    print(f"✅ Dataset found: {DATA_FILE}")
# ===========================
# 🔹 DATA LOADING FUNCTION
# ===========================

# FUNCTION TO EXTRACT THE DATA FROM THE hotel_rates_Philippines.csv 
def load_hotel_rates():
    """ Load and process hotel rates dynamically. """
    hotel_file = os.path.join(DATA_FOLDER, "Hotel_Rates_Philippines.csv")

    if not os.path.exists(hotel_file):
        print(f"❌ ERROR: Dataset '{hotel_file}' not found.")
        return {"price_ranges": {}}

    df = pd.read_csv(hotel_file)

    required_columns = ["Category", "Price Range (PHP/night)"]
    for col in required_columns:
        if col not in df.columns:
            print(f"❌ ERROR: Missing column '{col}' in dataset!")
            return {"price_ranges": {}}

    # Remove extra spaces and clean price range values
    df["Price Range (PHP/night)"] = df["Price Range (PHP/night)"].astype(str).str.strip()

    # Dynamically extract unique price ranges
    unique_price_ranges = sorted(df["Price Range (PHP/night)"].unique())

    # Initialize dictionary dynamically
    price_category_counts = {pr: {"Budget": 0, "Mid-Range": 0, "Luxury": 0} for pr in unique_price_ranges}

    # Count hotels per category in each price range
    for _, row in df.iterrows():
        category = row["Category"]
        price_range = row["Price Range (PHP/night)"]

        if price_range in price_category_counts and category in price_category_counts[price_range]:
            price_category_counts[price_range][category] += 1

    print("✅ DEBUG: Hotel Price Ranges Data →", price_category_counts)  # 🔍 Debugging

    return {"price_ranges": price_category_counts}

# FUNCTION TO EXTRACT THE DATA FROM THE Tourist_Arrivals_Philippines.csv 
def load_arrivals():
    """ Load and process tourist arrival data for visualization. """
    arrivals_file = os.path.join(DATA_FOLDER, "Tourist_Arrivals_Philippines.csv")

    if not os.path.exists(arrivals_file):
        print(f"❌ ERROR: Dataset '{arrivals_file}' not found.")
        return {"years": [], "revenue": [], "countries": {}, "tourists_by_country": {}}

    df = pd.read_csv(arrivals_file)

    # Ensure required columns exist
    required_columns = ["Year", "Foreign Tourists", "Domestic Tourists", "Top Visitor Country", "Revenue (PHP Billion)"]
    for col in required_columns:
        if col not in df.columns:
            print(f"❌ ERROR: Missing column '{col}' in dataset!")
            return {"years": [], "revenue": [], "countries": {}, "tourists_by_country": {}}

    # Remove duplicates and sort by year
    df = df.sort_values(by="Year").drop_duplicates(subset="Year")

    # Extract relevant data
    years = df["Year"].tolist()

    # Convert revenue to a list of floats, handling NaN values
    revenue = df["Revenue (PHP Billion)"].fillna(0).astype(float).tolist()  # ✅ Ensures JSON serializability

    # Group by top visitor country and sum tourists
    tourists_by_country = df.groupby("Top Visitor Country")["Foreign Tourists"].sum().to_dict()
    countries = list(tourists_by_country.keys())

    return {
        "years": years,
        "revenue": revenue,  # ✅ Always a valid list
        "countries": countries,
        "tourists_by_country": tourists_by_country
    }


# FUNCTION TO EXTRACT DATA FROM THE Tourist_Destinations_Philippines.csv
def load_destinations():
    """ Load and process the top 10 most visited tourist destinations based on arrivals. """
    destinations_file = os.path.join(DATA_FOLDER, "Tourist_Destinations_Philippines.csv")

    if not os.path.exists(destinations_file):
        print(f"❌ ERROR: Dataset '{destinations_file}' not found.")
        return {"cities": [], "tourist_count": []}

    df = pd.read_csv(destinations_file)

    # 🔹 Fix the column name here (replace "City" with "City/Province")
    required_columns = ["City/Province", "Tourist Arrivals"]
    for col in required_columns:
        if col not in df.columns:
            print(f"❌ ERROR: Missing column '{col}' in dataset!")
            return {"cities": [], "tourist_count": []}

    # Convert 'Tourist Arrivals' column to numeric (handling any formatting issues)
    df["Tourist Arrivals"] = pd.to_numeric(df["Tourist Arrivals"], errors="coerce")

    # Remove NaN values from 'Tourist Arrivals'
    df = df.dropna(subset=["Tourist Arrivals"])

    # Aggregate by 'City/Province' to sum tourist arrivals (some cities appear multiple times)
    df_grouped = df.groupby("City/Province")["Tourist Arrivals"].sum().reset_index()

    # Sort by total tourist arrivals in descending order and get the top 10
    df_sorted = df_grouped.sort_values(by="Tourist Arrivals", ascending=False).head(10)

    cities = df_sorted["City/Province"].tolist()
    tourist_count = df_sorted["Tourist Arrivals"].tolist()

    print("✅ DEBUG: Final Cities →", cities)
    print("✅ DEBUG: Final Tourist Counts →", tourist_count)

    return {
        "cities": cities,
        "tourist_count": tourist_count
    }


# ===========================
# 🔹 FLASK ROUTES
# ===========================




@app.route('/')
def home():
    """ Render Home Page """
    return render_template("home.html")

@app.route('/hotel_rates')
def hotel_rates():
    """ Render Hotel Rates Page with Data """
    data = load_hotel_rates()  # Load the hotel rates dynamically

    return render_template(
        "hotel_rates.html",
        price_ranges=data["price_ranges"]  # ✅ Pass the updated data structure
    )


@app.route('/arrivals')
def arrivals():
    data = load_arrivals()
    
    # Ensure revenue is always defined as a list
    revenue = data.get("revenue", [])
    
    return render_template(
        "arrivals.html",
        years=data.get("years", []),
        revenue=revenue,  # ✅ Ensure revenue is not None
        countries=data.get("countries", []),
        tourists_by_country=data.get("tourists_by_country", {})
    )
@app.route('/destinations')
def destinations():
    """ Render destinations Page with Data """
    data = load_destinations()

    return render_template(
        "destinations.html",
        cities=data.get("cities", []),  # ✅ Use .get() to avoid KeyError
        tourist_count=data.get("tourist_count", [])
    )
     
# ===========================
# 🔹 RUN FLASK APP
# ===========================

if __name__ == '__main__':
    app.run(debug=True)