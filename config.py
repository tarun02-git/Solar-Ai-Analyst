import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Analysis Configuration
CONFIDENCE_THRESHOLD = 0.7  # Minimum confidence score for analysis to be considered valid

# Solar Panel Configuration
PANEL_TYPES = {
    'standard': {
        'efficiency': 0.20,  # 20% efficiency
        'power_output': 400,  # 400W per panel
        'dimensions': (1.7, 1.0),  # meters
        'cost_per_panel': 250,  # USD
    },
    'premium': {
        'efficiency': 0.22,  # 22% efficiency
        'power_output': 450,  # 450W per panel
        'dimensions': (1.8, 1.1),  # meters
        'cost_per_panel': 350,  # USD
    }
}

# Financial Configuration
ANNUAL_MAINTENANCE_COST = 100  # USD per year
ELECTRICITY_RATE = 0.12  # USD per kWh
SYSTEM_LIFETIME = 25  # years
ANNUAL_DEGRADATION = 0.005  # 0.5% per year

# Supported image formats
SUPPORTED_IMAGE_FORMATS = ['jpg', 'jpeg', 'png']

# Installation Costs (USD)
BASE_INSTALLATION_COST = 2000
COST_PER_PANEL = 150
PERMIT_COST = 500
INSPECTION_COST = 300

# Maintenance Costs (USD per year)
CLEANING_COST = 150
MONITORING_COST = 100

# Energy Production Assumptions
AVERAGE_SUN_HOURS = 4.5  # hours per day
SYSTEM_LOSSES = 0.14  # 14% system losses

# ROI Calculations
ANNUAL_RATE_INCREASE = 0.03  # 3% annual increase

# AI Analysis Settings
MAX_IMAGE_SIZE = 1024  # pixels 