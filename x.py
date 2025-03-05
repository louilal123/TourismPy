from flask import Flask, render_template_string

app = Flask(__name__)  # Fix _name_ to __name__

# CSS Styling (same as before)
styles = """
<style>
body {
    font-family: Arial, sans-serif;
    background-color: #f8f9fa;
    margin: 0;
    padding: 20px; 
    line-height: 1
}

h1 {
    color: #007bff;
    margin-right: 100px; /* Move the title a bit to the right */
}

ul {
    list-style-type: none;
    padding: 0;
}

li {
    background: #e3f2fd;
    margin: 10px;
    padding: 10px;
    border-radius: 0px;
}

a {
    text-decoration: none;
    color: #007bff;
    font-weight: bold;
}

nav {
    margin-top: 20px;
}

.header {
    display: flex;
    justify-content: space-between;  /* Space between the title and navigation links */
    padding: 0;
    background-color: #007bff;
    color: white;
}

.header h1 {
    margin: 0;
}

.header nav {
    margin-top: 0;
}

.main-container {
    display: flex;
    justify-content: space-between;
    padding: 20px;
}

.destinations-list {
    width: 30%;
    padding: 20px;
}

.graph-container {
    width: 45%;
    padding: 20px;
    background-color: #e3f2fd;
    border-radius: 10px;
}

footer {
    background-color: #007bff;
    color: white;
    padding: 10px;
    text-align: center;
    position: fixed;
    bottom: 0;
    width: 50%;
}
</style>
"""

# Homepage with Left Title & Right Introduction
home_page = styles + """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tourism Insights PH:Destination, Arrivals & Hotels- Home</title>
</head>
<body>
        <nav>
            <a href="/destinations">Destinations</a> |
            <a href="/stats">Tourism Stats</a> |
            <a href="/contact">Contact Us</a>
        </nav>
    </div>
    <p style="text-align: center;">Discover the best tourist destinations in the Philippines!</p>
</body>
</html>
"""
# Homepage
home_page = styles + """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tourism Insights PH: Destination, Arrivals & Hotels - Home</title>
</head>
<body>

    <header>
        <h1>Welcome to Tourism Insights PH: Destination, Arrivals & Hotels</h1>
    </header>

    <main>
        <section>
            <h2>Welcome to Tourism Insights PH!</h2>
            <p>Explore the diverse beauty of the Philippines, one of the most sought-after travel destinations in Southeast Asia.</p>
            <p>Whether you’re a local traveler or a global explorer, this platform provides valuable insights into:</p>
            <ul>
                <li>The best tourist destinations</li>
                <li>The most popular hotels</li>
                <li>The latest tourism arrival trends</li>
            </ul>
        </section>

        <section>
            <h2>Our Mission</h2>
            <p>We aim to offer a comprehensive guide to the Philippines' thriving tourism industry.</p>
            <p>Our goal is to bring together crucial data on top destinations, hotel accommodations, and tourism statistics that are vital for both travelers and businesses in the tourism sector.</p>
        </section>

        <section>
            <h2>What You’ll Find Here:</h2>

            <article>
                <h3>🌴 Destination Insights</h3>
                <p>Discover must-visit places in the Philippines, from hidden gems to famous tourist hotspots like Boracay, Palawan, and Cebu.</p>
            </article>

            <article>
                <h3>🏨 Hotel Listings</h3>
                <p>Browse through our curated hotel listings across various regions of the Philippines. Whether you’re looking for luxurious resorts or budget-friendly stays, we’ve got you covered.</p>
            </article>

            <article>
                <h3>📊 Tourism Data</h3>
                <p>Access up-to-date data on tourism arrivals to the Philippines, including annual statistics, visitor demographics, and trends.</p>
            </article>
        </section>

        <p>Discover the best tourist destinations in the Philippines!</p>
    </main>

    <footer>
        <nav>
            <a href="/destinations">Destinations</a> |
            <a href="/stats">Tourism Stats</a> |
            <a href="/contact">Contact Us</a>
        </nav>
    </footer>

</body>
</html>

"""
# Destinations Page (with Graph for Tourist Destinations)
destinations_page = styles + """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-5">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tourism Insights PH: Destination,Arrivals & title</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h1>Top Destinations in the Philippines</h1>

    <div class="main-container">
        <div class="destinations-list">
            <ul>
                <li>Boracay - White Sand Beaches</li>
                <li>Palawan - Stunning Lagoons & Diving</li>
                <li>Cebu - Historical Landmarks & Waterfalls</li>
                <li>Siargao - Surfing Paradise</li>
                <li>Bohol - Chocolate Hills & Tarsiers</li>
            </ul>
            <a href="/">Back to Home</a>
        </div>

        <div class="graph-container">
            <canvas id="destinationChart" width="100" height="100"></canvas>
        </div>
    </div>

    <script>
        // Chart for Tourist Destinations
        const ctxDest = document.getElementById('destinationChart').getContext('2d');
        const destinationChart = new Chart(ctxDest, {
            type: 'bar', // Bar chart
            data: {
                labels: ['Boracay', 'Palawan', 'Cebu', 'Siargao', 'Bohol'],
                datasets: [{
                    label: 'Tourist Arrivals (in millions)',
                    data: [1.5, 1.2, 1.0, 0.8, 0.6], // Example data (millions of tourists)
                    backgroundColor: [
                 'rgba(255, 99, 132, 0.5)', // Boracay
                 'rgba(54, 162, 235, 0.5)', // Palawan
                 'rgba(255, 206, 86, 0.5)', // Cebu
                 'rgba(75, 192, 192, 0.5)', // Siargao
                 'rgba(153, 102, 255, 0.5)' // Bohol
                  ],

                    borderColor: 'rgb(62, 117, 161)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    </script>
</body>
</html>
"""

# Tourism Statistics Page (with graphs for Tourist Arrivals and Hotel Rates)
stats_page = styles + """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ExplorePH - Tourism Stats</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h1>Philippine Tourism Statistics</h1>
    <p>Latest data on tourist arrivals and spending:</p>
    <ul>
        <li>2023 Tourist Arrivals: 5.4 million</li>
        <li>Top Visitors: South Korea, USA, China</li>
        <li>Peak Season: December – April</li>
        <li>Average Spending: PHP 35,000 per tourist</li>
    </ul>

    <div class="main-container">
        <div class="graph-container">
            <canvas id="arrivalsChart" width="100" height="100"></canvas>
        </div>
        
        <div class="graph-container">
            <canvas id="hotelRatesChart" width="100" height="100"></canvas>
        </div>
    </div>
   <a href="/">Back to Home</a>
    
    <script>
        // Chart for Tourist Arrivals
        const ctxArrivals = document.getElementById('arrivalsChart').getContext('2d');
        const arrivalsChart = new Chart(ctxArrivals, {
            type: 'line', // Line chart
            data: {
                labels: ['January', 'February', 'March', 'April', 'May', 'June'], 
                datasets: [{
                    label: 'Tourist Arrivals (in millions)',
                    data: [0.4, 0.5, 0.7, 0.9, 1.0, 0.8], 
                    borderColor:[ 
                      'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 206, 86)',
                'rgb(75, 192, 192)',
                'rgb(153, 102, 255)'
             ],
                    fill: false,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        // Chart for Hotel Rates (average price per night)
        const ctxHotelRates = document.getElementById('hotelRatesChart').getContext('2d');
        const hotelRatesChart = new Chart(ctxHotelRates, {
            type: 'bar', // Bar chart
            data: {
                labels: ['Manila', 'Cebu', 'Davao', 'Boracay', 'Palawan'],
                datasets: [{
                    label: 'Average Hotel Rates (in PHP)',
                    data: [3500, 2500, 2200, 5500, 4500], // Example rates in PHP
                    backgroundColor: [ 
                 'rgba(255, 99, 132, 0.5)', // Boracay
                 'rgba(54, 162, 235, 0.5)', // Palawan
                 'rgba(255, 206, 86, 0.5)', // Cebu
                 'rgba(75, 192, 192, 0.5)', // Siargao
                 'rgba(153, 102, 255, 0.5)' // Bohol
                  ],

                    borderColor: 'rgba(0, 123, 255, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    </script>
</body>
</html>
"""

# Contact Page (same as before)
contact_page = styles + """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ExplorePH - Contact</title>
</head>
<body>
    <h1>Contact Us</h1>
    <p>Email: Tourism InsightPH:@gmail.com</p>
    <p>Phone: +63 912 345 6789</p>
    <p>Facebook page:Tourism InsightPH:Destination, Arrivals & Hotels </p>
    <p> Visit us today and start planning your dream trip!

If you have any questions or need more information, feel free to send us a message. 
Our team is ready to assist you in making your travel experience unforgettable.
See you on Tourism InsightPH – your gateway to exploring the Philippines! 🌎✨</p>

<p>Best regards,</p>

<p>[Your Name]</p>
 
 <p>Tourism InsightPH Team</p>
    <a href="/">Back to Home</a>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(home_page)

@app.route('/destinations')
def destinations():
    return render_template_string(destinations_page)

@app.route('/stats')
def stats():
    return render_template_string(stats_page)

@app.route('/contact')
def contact():
    return render_template_string(contact_page)

if  '__name__' == '__main__':  # Fix _name__ to __name__
    app.run(debug=True)