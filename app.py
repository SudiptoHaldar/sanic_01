from sanic import Sanic, response
from sanic.response import html
from basic import get_basic_info

app = Sanic("ResearchAssistant")

# Available competitors for checkbox selection
AVAILABLE_COMPETITORS = {
    "JPM": ["BAC", "C", "WFC", "GS"],  # Banks
    "AAPL": ["MSFT", "GOOGL", "AMZN", "META"],  # Tech
    "GOOGL": ["MSFT", "AAPL", "META", "AMZN"],  # Tech
    "BAC": ["JPM", "C", "WFC", "USB"],  # Banks
    "MSFT": ["AAPL", "GOOGL", "AMZN", "META"],  # Tech
}

# Sample bond and ratings data (will be replaced with database queries later)
def get_company_data(symbol):
    """Get all company data including basic info, bonds, and ratings"""
    basic_info = get_basic_info(symbol)

    # Placeholder bond and ratings data
    bond_info = [
        {"issuer": basic_info.get('company_name', symbol), "maturity": "2025-01-15", "coupon": "3.5%", "rating": "A+"},
        {"issuer": basic_info.get('company_name', symbol), "maturity": "2027-06-30", "coupon": "4.2%", "rating": "A+"},
    ]

    ratings = [
        {"agency": "Moody's", "rating": "Aa3", "outlook": "Stable"},
        {"agency": "S&P", "rating": "A+", "outlook": "Positive"},
        {"agency": "Fitch", "rating": "AA-", "outlook": "Stable"},
    ]

    return {
        **basic_info,
        "bond_info": bond_info,
        "ratings": ratings
    }

@app.route("/")
async def index(request):
    # Get symbol from query params or use default
    symbol = request.args.get('symbol', 'JPM').upper()
    company_data = get_company_data(symbol)

    # Get competitors for this symbol
    competitors = AVAILABLE_COMPETITORS.get(symbol, [])
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Research Assistant - Company Information</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}

            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}

            h1 {{
                text-align: center;
                color: white;
                margin-bottom: 30px;
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }}

            .sidebar {{
                background: white;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}

            .sidebar h2 {{
                color: #667eea;
                margin-bottom: 15px;
                font-size: 1.3em;
            }}

            .search-box {{
                background: white;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}

            .search-box h3 {{
                color: #667eea;
                margin-bottom: 15px;
                font-size: 1.1em;
            }}

            .symbol-input {{
                width: 100%;
                padding: 12px;
                border: 2px solid #e9ecef;
                border-radius: 5px;
                font-size: 1em;
                transition: border-color 0.3s;
            }}

            .symbol-input:focus {{
                outline: none;
                border-color: #667eea;
            }}

            .search-btn {{
                width: 100%;
                padding: 12px;
                margin-top: 10px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 1em;
                font-weight: bold;
                cursor: pointer;
                transition: background 0.3s;
            }}

            .search-btn:hover {{
                background: #5568d3;
            }}

            .competitors-box {{
                background: white;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}

            .competitors-box h3 {{
                color: #667eea;
                margin-bottom: 15px;
                font-size: 1.1em;
            }}

            .checkbox-item {{
                display: flex;
                align-items: center;
                padding: 8px;
                margin-bottom: 5px;
                border-radius: 5px;
                transition: background 0.2s;
            }}

            .checkbox-item:hover {{
                background: #f8f9fa;
            }}

            .checkbox-item input[type="checkbox"] {{
                margin-right: 10px;
                width: 18px;
                height: 18px;
                cursor: pointer;
            }}

            .checkbox-item label {{
                cursor: pointer;
                flex: 1;
            }}

            .current-symbol {{
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
                font-weight: bold;
                margin-left: 10px;
            }}

            .section-nav {{
                list-style: none;
            }}

            .section-nav li {{
                padding: 12px;
                margin-bottom: 8px;
                background: #f7f7f7;
                border-radius: 5px;
                cursor: pointer;
                transition: all 0.3s;
                border-left: 4px solid #667eea;
            }}

            .section-nav li:hover {{
                background: #e9ecef;
                transform: translateX(5px);
            }}

            .section-nav li.active {{
                background: #667eea;
                color: white;
                font-weight: bold;
            }}

            .content {{
                display: grid;
                grid-template-columns: 250px 1fr;
                gap: 20px;
            }}

            .main-content {{
                background: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}

            .section {{
                display: none;
            }}

            .section.active {{
                display: block;
            }}

            .section h2 {{
                color: #667eea;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 3px solid #667eea;
            }}

            .info-grid {{
                display: grid;
                gap: 15px;
                margin-top: 20px;
            }}

            .info-item {{
                padding: 15px;
                background: #f8f9fa;
                border-radius: 5px;
                border-left: 4px solid #667eea;
            }}

            .info-item label {{
                display: block;
                font-weight: bold;
                color: #495057;
                margin-bottom: 5px;
            }}

            .info-item value {{
                display: block;
                color: #212529;
                font-size: 1.1em;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}

            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #dee2e6;
            }}

            th {{
                background: #667eea;
                color: white;
                font-weight: bold;
            }}

            tr:hover {{
                background: #f8f9fa;
            }}

            @media (max-width: 768px) {{
                .content {{
                    grid-template-columns: 1fr;
                }}

                h1 {{
                    font-size: 1.8em;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 Research Assistant</h1>
            <p style="text-align: center; color: white; margin-bottom: 30px; font-size: 1.2em;">
                Provides all the company information you need at your fingertips
            </p>

            <div class="content">
                <div>
                    <!-- Symbol Search Box -->
                    <div class="search-box">
                        <h3>Search Company <span class="current-symbol">{symbol}</span></h3>
                        <form method="GET" action="/">
                            <input
                                type="text"
                                name="symbol"
                                class="symbol-input"
                                placeholder="Enter stock symbol (e.g., JPM, AAPL, GOOGL)"
                                value="{symbol}"
                                required
                            />
                            <button type="submit" class="search-btn">Search</button>
                        </form>
                    </div>

                    <!-- Competitors Selection -->
                    <div class="competitors-box">
                        <h3>Compare with Competitors</h3>
                        {'<div style="color: #6c757d; font-style: italic;">No competitors available for this symbol</div>' if not competitors else ''.join([f'''
                        <div class="checkbox-item">
                            <input type="checkbox" id="comp_{comp}" name="competitor" value="{comp}">
                            <label for="comp_{comp}">{comp}</label>
                        </div>
                        ''' for comp in competitors])}
                    </div>

                    <!-- Sections Navigation -->
                    <div class="sidebar">
                        <h2>Sections</h2>
                        <ul class="section-nav">
                            <li class="active" onclick="showSection('basic')">Basic Information</li>
                            <li onclick="showSection('bond')">Bond Information</li>
                            <li onclick="showSection('ratings')">Ratings Information</li>
                        </ul>
                    </div>
                </div>

                <div class="main-content">
                    <!-- Basic Information Section -->
                    <div id="basic" class="section active">
                        <h2>Basic Information</h2>
                        <div class="info-grid">
                            <div class="info-item">
                                <label>Company Name:</label>
                                <value>{company_data['company_name']}</value>
                            </div>
                            <div class="info-item">
                                <label>Annual Revenue:</label>
                                <value>{company_data['annual_revenue']}</value>
                            </div>
                            <div class="info-item">
                                <label>Annual Profit:</label>
                                <value>{company_data['annual_profit']}</value>
                            </div>
                        </div>
                    </div>

                    <!-- Bond Information Section -->
                    <div id="bond" class="section">
                        <h2>Bond Information</h2>
                        <table>
                            <thead>
                                <tr>
                                    <th>Issuer</th>
                                    <th>Maturity Date</th>
                                    <th>Coupon Rate</th>
                                    <th>Rating</th>
                                </tr>
                            </thead>
                            <tbody>
                                {''.join([f'''
                                <tr>
                                    <td>{bond['issuer']}</td>
                                    <td>{bond['maturity']}</td>
                                    <td>{bond['coupon']}</td>
                                    <td>{bond['rating']}</td>
                                </tr>
                                ''' for bond in company_data['bond_info']])}
                            </tbody>
                        </table>
                    </div>

                    <!-- Ratings Information Section -->
                    <div id="ratings" class="section">
                        <h2>Ratings Information</h2>
                        <table>
                            <thead>
                                <tr>
                                    <th>Rating Agency</th>
                                    <th>Rating</th>
                                    <th>Outlook</th>
                                </tr>
                            </thead>
                            <tbody>
                                {''.join([f'''
                                <tr>
                                    <td>{rating['agency']}</td>
                                    <td>{rating['rating']}</td>
                                    <td>{rating['outlook']}</td>
                                </tr>
                                ''' for rating in company_data['ratings']])}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <script>
            function showSection(sectionId) {{
                // Hide all sections
                const sections = document.querySelectorAll('.section');
                sections.forEach(section => {{
                    section.classList.remove('active');
                }});

                // Remove active class from all nav items
                const navItems = document.querySelectorAll('.section-nav li');
                navItems.forEach(item => {{
                    item.classList.remove('active');
                }});

                // Show selected section
                document.getElementById(sectionId).classList.add('active');

                // Add active class to clicked nav item
                event.target.classList.add('active');
            }}

            // Handle competitor checkbox selection
            document.addEventListener('DOMContentLoaded', function() {{
                const checkboxes = document.querySelectorAll('input[name="competitor"]');
                checkboxes.forEach(checkbox => {{
                    checkbox.addEventListener('change', function() {{
                        const selectedCompetitors = Array.from(checkboxes)
                            .filter(cb => cb.checked)
                            .map(cb => cb.value);

                        if (selectedCompetitors.length > 0) {{
                            console.log('Selected competitors:', selectedCompetitors);
                            // TODO: Add functionality to compare with competitors
                            // This will be implemented in future iterations
                        }}
                    }});
                }});

                // Allow pressing Enter in symbol input to submit
                const symbolInput = document.querySelector('.symbol-input');
                if (symbolInput) {{
                    symbolInput.addEventListener('keypress', function(e) {{
                        if (e.key === 'Enter') {{
                            e.target.closest('form').submit();
                        }}
                    }});
                }}
            }});
        </script>
    </body>
    </html>
    """
    return html(html_content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
