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
    """ Load and process hotel rates for visualization. """
    hotel_file = os.path.join(DATA_FOLDER, "Hotel_Rates_Philippines.csv")

    if not os.path.exists(hotel_file):
        print(f"❌ ERROR: Dataset '{hotel_file}' not found.")
        return {"hotels": [], "categories": {}, "surcharge": {}, "avg_price": []}

    df = pd.read_csv(hotel_file)

    required_columns = ["Hotel Name", "Location", "Category", "Price Range (PHP/night)", "Common Amenities", "Peak Season Surcharge (%)"]
    for col in required_columns:
        if col not in df.columns:
            print(f"❌ ERROR: Missing column '{col}' in dataset!")
            return {"hotels": [], "categories": {}, "surcharge": {}, "avg_price": []}

    # Extract hotel names
    hotel_names = df["Hotel Name"].tolist()

    # Extract peak season surcharge
    peak_surcharge = df["Peak Season Surcharge (%)"].astype(float).tolist()

    # Extract and calculate the average price range
    avg_price = []
    for price_range in df["Price Range (PHP/night)"]:
        try:
            prices = list(map(int, price_range.replace("₱", "").replace(",", "").split(" - ")))
            avg_price.append(sum(prices) / len(prices))  # Compute average
        except:
            avg_price.append(0)  # Handle errors gracefully

    # Group by category and count hotels
    category_counts = df["Category"].value_counts().to_dict()

    # Group by category and calculate average surcharge
    surcharge_avg = df.groupby("Category")["Peak Season Surcharge (%)"].mean().to_dict()

    return {
        "hotels": hotel_names,
        "categories": category_counts,
        "surcharge": surcharge_avg,
        "avg_price": avg_price,
        "peak_surcharge": peak_surcharge
    }



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
    data = load_hotel_rates()
    return render_template("hotel_rates.html",
                           hotel_names=data["hotels"],
                           avg_price=data["avg_price"],
                           peak_surcharge=data["peak_surcharge"],
                           categories=data["categories"],
                           surcharge=data["surcharge"])


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
    """ Render destinations Page """
    return render_template("destinations.html")

# ===========================
# 🔹 RUN FLASK APP
# ===========================

if __name__ == '__main__':
    app.run(debug=True)