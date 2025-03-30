from flask import Flask, render_template, jsonify
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

        # Check if column exists
        if column_name not in df.columns:
            print(f"❌ ERROR: Column '{column_name}' not found in {filename}")
            return 0

        return df[column_name].sum()

    @classmethod
    def get_pie_chart_data(cls):
        """Retrieves summed child labor estimates for Luzon, Visayas, and Mindanao."""
        luzon_total = cls.load_dataset("luzon_dataset.csv", "Estimate ('000)")
        visayas_total = cls.load_dataset("visayas_dataset.csv", "Estimate ('000)")
        mindanao_total = cls.load_dataset("mindanao_dataset.csv", "Estimate ('000)")

        return {
            "labels": ["Luzon", "Visayas", "Mindanao"],
            "values": [luzon_total, visayas_total, mindanao_total]
        }

# ===========================
# 🔹 FLASK APP & ROUTES
# ===========================

app = Flask(__name__)

@app.route('/')
def home():
    """Render the home page with the pie chart."""
    return render_template("home.html")

@app.route('/get_pie_chart_data')
def get_pie_chart_data():
    """API route to serve pie chart data."""
    data = DataLoader.get_pie_chart_data()
    return jsonify(data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
