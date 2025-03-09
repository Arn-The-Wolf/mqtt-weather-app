# MQTT Weather Station Dashboard

This application collects temperature and humidity data from MQTT sensors and displays it in a real-time dashboard with historical data visualization.

## Features

- Real-time temperature and humidity monitoring
- Historical data storage in SQLite database
- Interactive graph showing temperature and humidity trends
- 5-minute data averaging for historical view
- Admin panel with protected routes
- Data export functionality to CSV
- Alert system for temperature and humidity thresholds

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd weather-station-dashboard
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```

3. Install required Python packages:
   ```bash
   pip install flask flask-socketio paho-mqtt pandas flask-login plotly
   ```

4. Configure the application:
   - Review and update the MQTT broker settings in `config.py` if needed
   - Update the secret key in `server.py` for production use
   - Adjust alert thresholds in `config.py` if desired

5. Initialize the database:
   - The database will be automatically created when you run the server
   - Default location: `weather_data.db`

6. Run the server:
   ```bash
   python run.py
   ```

7. Access the dashboard:
   - Open your browser and navigate to `http://localhost:5000`
   - Admin panel available at `http://localhost:5000/admin`

## Project Structure

- `server.py`: Main application file with Flask routes and MQTT handling
- `run.py`: Application entry point
- `config.py`: Configuration settings
- `templates/`: Frontend templates
  - `index.html`: Main dashboard template
  - `admin.html`: Admin panel template
- `weather_data.db`: SQLite database for historical data
- `utils/`: Utility functions and helpers
  - `logger.py`: Logging configuration

## Development

To run the application in development mode: