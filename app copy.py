from flask import Flask, render_template
import pandas as pd
import os

class DataLoader:
    """Handles data loading and processing for various datasets."""

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FOLDER = os.path.join(BASE_DIR, "templates", "data")

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
    def load_hotel_rates(cls):
        df = cls.load_csv("Hotel_Rates_Philippines.csv", ["Category", "Price Range (PHP/night)"])
        if df.empty: return {"price_ranges": {}}

        df["Price Range (PHP/night)"] = df["Price Range (PHP/night)"].astype(str).str.strip()
        unique_price_ranges = sorted(df["Price Range (PHP/night)"].unique())
        
        price_category_counts = {pr: {"Budget": 0, "Mid-Range": 0, "Luxury": 0} for pr in unique_price_ranges}
        for _, row in df.iterrows():
            category, price_range = row["Category"], row["Price Range (PHP/night)"]
            if price_range in price_category_counts and category in price_category_counts[price_range]:
                price_category_counts[price_range][category] += 1

        return {"price_ranges": price_category_counts}

    @classmethod
    def load_arrivals(cls):
        df = cls.load_csv("Tourist_Arrivals_Philippines.csv", [
            "Year", "Foreign Tourists", "Domestic Tourists", "Top Visitor Country", "Revenue (PHP Billion)"
        ])
        if df.empty: return {"years": [], "revenue": [], "countries": {}, "tourists_by_country": {}}

        df = df.sort_values(by="Year").drop_duplicates(subset="Year")
        tourists_by_country = df.groupby("Top Visitor Country")["Foreign Tourists"].sum().to_dict()
        return {
            "years": df["Year"].tolist(),
            "revenue": df["Revenue (PHP Billion)"].fillna(0).astype(float).tolist(),
            "countries": list(tourists_by_country.keys()),
            "tourists_by_country": tourists_by_country
        }

    @classmethod
    def load_destinations(cls):
        df = cls.load_csv("Tourist_Destinations_Philippines.csv", ["City/Province", "Tourist Arrivals"])
        if df.empty: return {"cities": [], "tourist_count": []}

        df["Tourist Arrivals"] = pd.to_numeric(df["Tourist Arrivals"], errors="coerce").fillna(0)
        df_grouped = df.groupby("City/Province")["Tourist Arrivals"].sum().reset_index()
        df_sorted = df_grouped.sort_values(by="Tourist Arrivals", ascending=False).head(10)

        return {
            "cities": df_sorted["City/Province"].tolist(),
            "tourist_count": df_sorted["Tourist Arrivals"].tolist()
        }


    @classmethod
    def load_occupancy_data(cls):
        df = cls.load_csv("Hotel_Occupancy_Rates.csv", [
            "Year", "Occupancy Rate (%)", "Revenue (PHP)"
        ])
        if df.empty: 
            return {"years": [], "occupancy_rates": [], "revenue": []}

        # Group by 'Year' and calculate averages/sums
        df_grouped = df.groupby("Year", as_index=False).agg({
            "Occupancy Rate (%)": "mean",
            "Revenue (PHP)": "sum"
        })

        return {
            "years": df_grouped["Year"].astype(str).tolist(),
            "occupancy_rates": df_grouped["Occupancy Rate (%)"].round(1).tolist(),
            "revenue": df_grouped["Revenue (PHP)"].astype(int).tolist()
        }



# ===========================
# 🔹 FLASK APP & ROUTES
# ===========================

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/hotel_rates')
def hotel_rates():
    return render_template("hotel_rates.html", price_ranges=DataLoader.load_hotel_rates()["price_ranges"])

@app.route('/arrivals')
def arrivals():
    return render_template("arrivals.html", **DataLoader.load_arrivals())

@app.route('/destinations')
def destinations():
    return render_template("destinations.html", **DataLoader.load_destinations())

@app.route('/hotel_occupancy')
def hotel_occupancy():
    return render_template("hotel_occupancy.html", occupancy_data=DataLoader.load_occupancy_data())

if __name__ == "__main__":
    app.run(debug=True)