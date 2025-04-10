from flask import Flask, render_template, jsonify, request
import pandas as pd
import os

# ===========================
# 🔹 DataLoader CLASS
# ===========================
class DataLoader:
    """Handles data loading and processing for various datasets."""

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FOLDER = os.path.join(BASE_DIR, "templates", "data")

    @classmethod
    def load_dataset(cls, filename, column_name):
        """Loads a CSV file and returns the sum of the given column."""
        file_path = os.path.join(cls.DATA_FOLDER, filename)
        if not os.path.exists(file_path):
            print(f"❌ ERROR: {filename} not found.")
            return 0

        df = pd.read_csv(file_path)

        if column_name not in df.columns:
            print(f"❌ ERROR: Column '{column_name}' not found in {filename}")
            return 0

        return df[column_name].sum()

    @classmethod
    def get_grouped_data(cls, filename, group_by, sum_column, year_filter=None):
        """Returns grouped data from a CSV, summing the specified column by a group, sorted logically."""
        file_path = os.path.join(cls.DATA_FOLDER, filename)
        if not os.path.exists(file_path):
            print(f"❌ ERROR: {filename} not found.")
            return {"regions": [], "cases": [], "years": []}

        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"❌ ERROR reading {filename}: {str(e)}")
            return {"regions": [], "cases": [], "years": []}

        if group_by not in df.columns or sum_column not in df.columns:
            print(f"❌ ERROR: Missing columns in {filename}")
            return {"regions": [], "cases": [], "years": []}

        # Get all available years from the dataset for the filter
        available_years = []
        if "Year" in df.columns:
            available_years = sorted(df["Year"].unique().tolist())

        # Apply year filter if specified
        if year_filter and year_filter != "all" and "Year" in df.columns:
            try:
                year_filter = int(year_filter)
                df = df[df["Year"] == year_filter]
            except (ValueError, TypeError):
                # If year_filter is invalid, don't filter
                pass

        # Define the desired order (NCR first, BARMM last)
        desired_order = [
            "NCR",
            "REGION I (ILOCOS REGION)",
            "REGION II (CAGAYAN VALLEY)",
            "REGION III (CENTRAL LUZON)",
            "REGION IV-A (CALABARZON)",
            "REGION IV-B (MIMAROPA)",
            "REGION V (BICOL REGION)",
            "REGION VI (WESTERN VISAYAS)",
            "REGION VII (CENTRAL VISAYAS)",
            "REGION VIII (EASTERN VISAYAS)",
            "REGION IX (ZAMBOANGA PENINSULA)",
            "REGION X (NORTHERN MINDANAO)",
            "REGION XI (DAVAO REGION)",
            "REGION XII (SOCCSKSARGEN)",
            "REGION XIII (CARAGA)",
            "BARMM"
        ]

        # Group and sum the data
        grouped = df.groupby(group_by)[sum_column].sum().reset_index()

        # Get all unique regions from data (case-sensitive)
        all_regions = grouped[group_by].unique().tolist()

        # Create full order: desired regions first, then any others in alphabetical order
        missing_regions = sorted([r for r in all_regions if r not in desired_order])
        full_order = desired_order + missing_regions

        # Convert to categorical with our custom order
        grouped[group_by] = pd.Categorical(
            grouped[group_by], 
            categories=full_order, 
            ordered=True
        )
        
        # Sort by our custom order
        grouped = grouped.sort_values(group_by)

        return {
            "regions": grouped[group_by].tolist(),
            "cases": [int(x) for x in grouped[sum_column].tolist()],  # Remove decimal places
            "years": available_years
        }


# ===========================
# 🔹 FLASK APP & ROUTES
# ===========================
app = Flask(__name__)

@app.route('/')
def home():
    """Render the home page with the chart."""
    return render_template("home.html")

@app.route('/api/region-cases')
def region_cases():
    """API route that returns JSON data for the Chart.js graph."""
    year_filter = request.args.get('year', 'all')
    
    grouped_data = DataLoader.get_grouped_data(
        filename="cleaned_casesbyregion.csv",
        group_by="Region",
        sum_column="Estimated Cases",
        year_filter=year_filter
    )
    return jsonify(grouped_data)# Add these new endpoints to your Flask app
@app.route('/api/age-cases')
def age_cases():
    """API route that returns JSON data for age group distribution."""
    year_filter = request.args.get('year', 'all')
    grouped_data = DataLoader.get_grouped_data(
        filename="cleaned_casesbyagegroup.csv",
        group_by="Age Group",
        sum_column="Total",
        year_filter=year_filter
    )
    
    # Get male/female breakdown
    file_path = os.path.join(DataLoader.DATA_FOLDER, "cleaned_casesbyagegroup.csv")
    df = pd.read_csv(file_path)
    
    if year_filter and year_filter != "all":
        df = df[df["Year"] == int(year_filter)]
    
    age_data = {
        "age_groups": df["Age Group"].unique().tolist(),
        "male": df.groupby("Age Group")["Male"].sum().tolist(),
        "female": df.groupby("Age Group")["Female"].sum().tolist(),
        "years": sorted(df["Year"].unique().tolist())
    }
    return jsonify(age_data)

@app.route('/api/industry-cases')
def industry_cases():
    """API route that returns JSON data for industry distribution."""
    year_filter = request.args.get('year', 'all')
    file_path = os.path.join(DataLoader.DATA_FOLDER, "cleaned_casesbyindustry.csv")
    df = pd.read_csv(file_path)
    
    # Get all available years for the filter
    available_years = sorted(df["Year"].unique().tolist())
    
    # Apply year filter if specified
    if year_filter and year_filter != "all":
        try:
            year_filter = int(year_filter)
            df = df[df["Year"] == year_filter]
        except (ValueError, TypeError):
            # If year_filter is invalid, don't filter
            pass
    
    # Group by Industry and sum percentiles when "All Years" is selected
    if year_filter == "all":
        # Group by Industry and calculate mean of percentiles
        grouped_df = df.groupby("Industry")["Percentile"].mean().reset_index()
        
        # Normalize percentiles to ensure they sum to 100%
        total = grouped_df["Percentile"].sum()
        if total > 0:  # Avoid division by zero
            grouped_df["Percentile"] = (grouped_df["Percentile"] / total) * 100
            
        # Round to 1 decimal place for display
        grouped_df["Percentile"] = grouped_df["Percentile"].round(1)
        
        industry_data = {
            "industries": grouped_df["Industry"].tolist(),
            "percentiles": grouped_df["Percentile"].tolist(),
            "years": available_years
        }
    else:
        # Single year, just return the data as is
        industry_data = {
            "industries": df["Industry"].tolist(),
            "percentiles": df["Percentile"].tolist(),
            "years": available_years
        }
    
    return jsonify(industry_data)
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# ===========================
# 🔹 APP START
# ===========================
if __name__ == "__main__":
    app.run(debug=True)