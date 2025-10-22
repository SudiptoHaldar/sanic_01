# Research Assistant

**Research Assistant** is a web application that provides all the company information you need at your fingertips. Built with the high-performance Sanic framework, it offers a clean and intuitive interface to view company details, bond information, and credit ratings.

## Features

- **Basic Information**: View essential company details including name, annual revenue, and profit
- **Bond Information**: Access detailed bond data including issuer, maturity dates, coupon rates, and ratings
- **Ratings Information**: See credit ratings from major agencies (Moody's, S&P, Fitch) with outlooks
- **Responsive Design**: Beautiful, modern UI that works on desktop and mobile devices
- **Fast Performance**: Built on Sanic for high-speed asynchronous request handling

## Screenshots

The application features a three-section interface:
- Left sidebar navigation for easy section switching
- Main content area displaying detailed information
- Color-coded visual design for better readability

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone or Download the Repository

```bash
git clone <repository-url>
cd sanic_01
```

Or if you already have the files, navigate to the project directory:

```bash
cd c:\Sudipto\Projects-external\AIML_projects\sanic_01
```

### Step 2: Create a Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Sanic web framework (v23.12.0 or higher)

### Step 4: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:8000` by default.

## Usage

1. Open your web browser and navigate to `http://localhost:8000`
2. You'll see the Research Assistant homepage with the sidebar navigation
3. Click on any section in the sidebar to view:
   - **Basic Information**: Company overview and financial summary
   - **Bond Information**: Detailed bond listings in table format
   - **Ratings Information**: Credit ratings from major agencies

## Project Structure

```
sanic_01/
│
├── app.py                  # Main Sanic application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── ui_v1.pptx             # UI design reference
└── extract_ppt.py         # Utility script for PowerPoint extraction
```

## Customization

### Changing the Company Data

Edit the `company_data` dictionary in [app.py](app.py) (around line 8) to display information for a different company:

```python
company_data = {
    "company_name": "Your Company Name",
    "annual_revenue": "$XXX.XB",
    "annual_profit": "$XXX.XB",
    "bond_info": [
        {"issuer": "...", "maturity": "...", "coupon": "...", "rating": "..."},
    ],
    "ratings": [
        {"agency": "...", "rating": "...", "outlook": "..."},
    ]
}
```

### Changing the Port

To run the application on a different port, modify the last line in [app.py](app.py):

```python
app.run(host="0.0.0.0", port=8080, debug=True)  # Change 8000 to your preferred port
```

### Styling

All CSS styles are embedded in the HTML template in [app.py](app.py). Look for the `<style>` section to customize:
- Colors
- Fonts
- Layout
- Responsive breakpoints

## Technology Stack

- **Backend**: [Sanic](https://github.com/sanic-org/sanic) - Async Python web framework
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Design**: Responsive, mobile-first design with gradient backgrounds

## Development

### Debug Mode

The application runs in debug mode by default, which provides:
- Automatic reloading on code changes
- Detailed error messages
- Request logging

To disable debug mode for production:

```python
app.run(host="0.0.0.0", port=8000, debug=False)
```

### Adding New Routes

To add new endpoints, use the Sanic route decorator:

```python
@app.route("/api/data")
async def get_data(request):
    return response.json({"status": "success"})
```

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, either:
1. Stop the application using that port
2. Change the port in `app.py` to an available port

### Module Not Found Error

Make sure you've activated your virtual environment and installed all dependencies:

```bash
pip install -r requirements.txt
```

### Python Version Issues

Ensure you're using Python 3.8 or higher:

```bash
python --version
```

## License

This project is provided as-is for educational and commercial use.

## Support

For issues, questions, or contributions, please refer to the project repository or contact the development team.

---

**Built with Sanic** - Making Python web development fast and simple!
