
from flask import Flask, render_template,  request
import pandas as pd
import os

# ===========================
# 🔹 PARENT function
# ===========================
class DataLoader:
    """Handles data loading and processing for various datasets."""

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FOLDER = os.path.join(BASE_DIR, "templates", "data")

# ===========================
# 🔹  CLASS methods
# ===========================
    @classmethod
    def load_csv(cls, filename, required_columns):
        """Generic method to load CSV data and validate required columns."""
        file_path = os.path.join(cls.DATA_FOLDER, filename)
        if not os.path.exists(file_path):
            print(f"❌ ERROR: Dataset '{filename}' not found.")
            return pd.DataFrame()
        
        df = pd.read_csv(file_path)
        for col in required_columns:
            if col not in df.columns:
                print(f"❌ ERROR: Missing column '{col}' in dataset!")
                return pd.DataFrame()
        return df

    @classmethod
    def load_arrivals(cls, selected_region=None):
        df = cls.load_csv("Tourist_Arrivals_Philippines.csv", [
            "Year", "Region", "Foreign Tourists", "Domestic Tourists", "Total Visitors", 
            "Revenue (PHP Billion)", "Top Visitor Country", "Purpose of Visit"
        ])
        
        if df.empty:
            return {"years": [], "regions": [], "tourists_by_country": {}}

        # Extract and sort unique regions
        regions = sorted(df["Region"].dropna().unique().tolist(), 
                        key=lambda x: int(x.split()[-1]) if x.split()[-1].isdigit() else float('inf'))

        # Filter by selected region
        if selected_region and selected_region != "All Regions":
            df = df[df["Region"] == selected_region]

        # Ensure 'Top Visitor Country' and 'Foreign Tourists' columns have valid data
        df = df.dropna(subset=["Top Visitor Country", "Foreign Tourists"])
        df["Foreign Tourists"] = pd.to_numeric(df["Foreign Tourists"], errors="coerce").fillna(0)

        # Aggregate correctly
        tourists_by_country = df.groupby("Top Visitor Country", as_index=False)["Foreign Tourists"].sum()
        tourists_by_country = tourists_by_country.sort_values(by="Foreign Tourists", ascending=False)
        
        # Convert to dictionary format expected by Highcharts
        tourists_by_country_dict = dict(zip(tourists_by_country["Top Visitor Country"], tourists_by_country["Foreign Tourists"]))

        return {
            "years": df["Year"].unique().tolist(),
            "regions": ["All Regions"] + regions,
            "tourists_by_country": tourists_by_country_dict
        }


    @classmethod
    def load_destinations(cls, selected_year=None):
            df = cls.load_csv("Tourist_Destinations_Philippines.csv", ["City/Province", "Tourist Arrivals", "Year"])
            if df.empty:
                return {"cities": [], "tourist_count": [], "years": []}

            # Extract unique years for the dropdown
            years = sorted(df["Year"].dropna().unique().tolist())

            # Convert year data to string to ensure consistent comparison
            df["Year"] = df["Year"].astype(str)

            # Filter data only if a valid year is selected
            if selected_year and selected_year != "All Time":
                df = df[df["Year"] == selected_year]

            df["Tourist Arrivals"] = pd.to_numeric(df["Tourist Arrivals"], errors="coerce").fillna(0)
            df_grouped = df.groupby("City/Province")["Tourist Arrivals"].sum().reset_index()
            df_sorted = df_grouped.sort_values(by="Tourist Arrivals", ascending=False).head(10)

            return {
                "cities": df_sorted["City/Province"].tolist(),
                "tourist_count": df_sorted["Tourist Arrivals"].tolist(),
                "years": ["All Time"] + years  # Add 'All Time' as the default option
            }



    @classmethod
    def load_occupancy_data(cls, selected_region=None):
            df = cls.load_csv("Hotel_Occupancy_Rates.csv", [
                "Year", "Month", "Region", "Occupancy Rate (%)", "Revenue (PHP)"
            ])
            if df.empty: 
                return {"years": [], "regions": [], "occupancy_rates": [], "revenue": []}

            # Extract unique regions for the dropdown
            regions = sorted(df["Region"].dropna().unique().tolist())

            # Filter data by region if selected
            if selected_region and selected_region != "All ":
                df = df[df["Region"] == selected_region]

            # Group by Year instead of Month for the x-axis
            df_grouped = df.groupby("Year", as_index=False).agg({
                "Occupancy Rate (%)": "mean",
                "Revenue (PHP)": "sum"
            })

            return {
                "years": df_grouped["Year"].astype(str).tolist(),  # Ensure years are strings for Highcharts
                "regions": ["All "] + regions,
                "occupancy_rates": df_grouped["Occupancy Rate (%)"].round(1).tolist(),
                "revenue": df_grouped["Revenue (PHP)"].astype(int).tolist()
            }



# ===========================
# 🔹 FLASK APP & ROUTES 
# ===========================

app = Flask(__name__)

@app.route('/')
def home():

    # this line is when u want to display the data in the home.html 
    data = {
        "destinations": DataLoader.load_destinations(),
        "arrivals": DataLoader.load_arrivals(),
        "occupancy": DataLoader.load_occupancy_data()
    }
    return render_template("home.html", **data)

@app.route('/destinations')
def destinations():
    selected_year = request.args.get('year', "All Time")  # Default to 'All Time'

    # Load destination data with selected year
    data = DataLoader.load_destinations(selected_year)

    # Ensure selected_year is treated as a string for consistency
    if selected_year != "All Time" and selected_year not in map(str, data["years"]):
        return render_template("404.html"), 404  # Redirect invalid year to 404 page

    return render_template("destinations.html", **data, selected_year=selected_year)

@app.route('/arrivals')
def arrivals():
    selected_region = request.args.get('region', "All Regions")

    # Load data and get valid regions
    data = DataLoader.load_arrivals(selected_region)
    valid_regions = data.get("regions", [])  # Assuming 'regions' is part of the data

    # Error handling for invalid regions
    if selected_region != "All Regions" and selected_region not in valid_regions:
        return render_template("404.html"), 404  # Invalid region -> 404

    return render_template("arrivals.html", **data, selected_region=selected_region)


@app.route('/hotel_occupancy')
def hotel_occupancy():
    selected_region = request.args.get('region', "All ")

    # Load data and get valid regions
    data = DataLoader.load_occupancy_data(selected_region)
    valid_regions = data.get("regions", [])  # Assuming 'regions' is part of the data

    # Error handling for invalid regions
    if selected_region != "All " and selected_region not in valid_regions:
        return render_template("404.html"), 404  # Invalid region -> 404

    return render_template("hotel_occupancy.html", occupancy_data=data, selected_region=selected_region)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)