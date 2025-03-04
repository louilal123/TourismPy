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
def load_destinations():
    """ Load hotel data from the CSV file and structure it properly. """
    if not os.path.exists(DATA_FILE):
        print(f"❌ ERROR: Dataset '{DATA_FILE}' not found.")
        return {"destinations": [], "categories": {}}

    df = pd.read_csv(DATA_FILE)

    # Ensure necessary columns exist
    required_columns = ["Hotel Name", "Location", "Category", "Price Range (PHP/night)", "Common Amenities", "Peak Season Surcharge (%)"]
    for col in required_columns:
        if col not in df.columns:
            print(f"❌ ERROR: Missing column '{col}' in dataset!")
            return {"destinations": [], "categories": {}}

    # Convert to list of dictionaries
    destinations_list = df.to_dict(orient="records")

    # Group by category and count hotels
    category_counts = df["Category"].value_counts().to_dict()

    return {"destinations": destinations_list, "categories": category_counts}

# ===========================
# 🔹 FLASK ROUTES
# ===========================

@app.route('/')
def home():
    """ Render Home Page """
    return render_template("home.html")

@app.route('/destinations')
def destinations():
    """ Render Destinations Page with Data """
    data = load_destinations()
    return render_template("destinations.html", destinations=data["destinations"], categories=data["categories"])

@app.route('/stats')
def stats():
    """ Render Statistics Page """
    return render_template("stats.html")

@app.route('/contact')
def contact():
    """ Render Contact Page """
    return render_template("contact.html")

# ===========================
# 🔹 RUN FLASK APP
# ===========================

if __name__ == '__main__':
    app.run(debug=True)