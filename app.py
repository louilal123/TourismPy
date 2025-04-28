from flask import Flask, render_template, jsonify, request
import pandas as pd

app = Flask(__name__)

luzon = pd.read_csv('templates/data/luzon_cleaned.csv')
visayas = pd.read_csv('templates/data/visayas_cleaned.csv')
mindanao = pd.read_csv('templates/data/mindanao_cleaned.csv')
all_data = pd.concat([luzon, visayas, mindanao])

@app.route('/api/island-cases')
def get_island_cases():
    year_filter = request.args.get('year', 'all')
    data = all_data if year_filter == 'all' else all_data[all_data['Year'] == int(year_filter)]
    
    island_totals = data.groupby('Island Group')['Estimated Cases'].sum().reset_index()
    # Convert to integers
    island_totals['Estimated Cases'] = island_totals['Estimated Cases'].astype(int)
    
    return jsonify({
        'island_groups': island_totals['Island Group'].tolist(),
        'cases': island_totals['Estimated Cases'].tolist(),
        'years': sorted(all_data['Year'].unique().tolist())
    })

@app.route('/api/regions')
def get_regions():
    island = request.args.get('island')
    regions = all_data[all_data['Island Group'] == island]['Region'].unique().tolist()
    return jsonify({'regions': regions})

@app.route('/api/region-data')
def get_region_data():
    island = request.args.get('island')
    region = request.args.get('region')
    year = request.args.get('year', 'all')

    filtered = all_data[(all_data['Island Group'] == island) & 
                        (all_data['Region'] == region)]

    if year != 'all':
        filtered = filtered[filtered['Year'] == int(year)]

    # GROUP BY Province AND Year
    grouped = filtered.groupby(['Province', 'Year'])['Estimated Cases'].sum().reset_index()
    grouped['Estimated Cases'] = grouped['Estimated Cases'].astype(int)  # Convert to integers

    result = {}
    for _, row in grouped.iterrows():
        province = row['Province']
        yr = row['Year']
        if province not in result:
            result[province] = {}
        result[province][yr] = int(row['Estimated Cases'])  # Ensure integer

    return jsonify(result)

@app.route('/api/estimated-cases-by-island-group')
def get_estimated_cases_by_island_group():
    island_group = request.args.get('island_group', 'all')
    year_filter = request.args.get('year', 'all')

    data = all_data 
    if island_group != 'all':
        data = data[data['Island Group'] == island_group]
    if year_filter != 'all':
        data = data[data['Year'] == int(year_filter)]

    # Group by Year and sum Estimated Cases
    grouped_data = data.groupby('Year')['Estimated Cases'].sum().reset_index()
    grouped_data['Estimated Cases'] = grouped_data['Estimated Cases'].astype(int)  # Convert to integers

    return jsonify({
        'data': grouped_data.to_dict(orient='records')
    })

@app.route('/')
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)