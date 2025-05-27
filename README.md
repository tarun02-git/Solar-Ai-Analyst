# Solar Industry AI Assistant

An intelligent system that analyzes rooftops from satellite imagery to provide solar potential assessments, installation recommendations, and ROI estimates.

## Prerequisites

- Python 3.8 or higher
- Git
- A Google Maps API key (for satellite imagery)
- An OpenAI API key (for AI analysis)
- A modern web browser

## Features

- Rooftop analysis using AI vision capabilities
- Solar potential assessment
- Installation recommendations
- ROI calculations
- Maintenance guidelines
- Regulatory compliance information

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/tarun02-git/Solar-Ai-Analyst.git
   ```

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following content:
   ```
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key
   ```

## Project Structure

```
solar-industry-ai-assistant/
├── app.py                 # Main Streamlit application
├── solar_analysis.py      # Solar potential calculation module
├── ai_utils.py           # AI integration utilities
├── config.py             # Configuration and constants
├── requirements.txt      # Project dependencies
├── .env                  # Environment variables (create this)
├── static/              # Static assets
│   ├── css/
│   └── images/
└── tests/               # Test files
```

## Running the Application

1. Ensure your virtual environment is activated:
   ```bash
   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

2. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

3. Access the application:
   - Open your web browser
   - Navigate to http://localhost:8501

## Usage Guide

1. **Property Analysis**
   - Enter the property address or coordinates
   - Upload a satellite image of the rooftop
   - Wait for the AI analysis to complete

2. **Review Results**
   The system will provide:
   - Solar potential assessment
   - Recommended panel types and configurations
   - Installation cost estimates
   - ROI calculations
   - Maintenance recommendations
   - Regulatory compliance information

3. **Export Results**
   - Download the analysis report in PDF format
   - Save the solar panel layout visualization
   - Export cost breakdown and ROI projections

## Development

### Setting Up Development Environment

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running Tests

```bash
pytest tests/
```

## API Documentation

The application uses the following APIs:
- OpenAI API for image analysis
- Google Maps API for satellite imagery
- Solar irradiance data API

For detailed API documentation, refer to the `docs/api.md` file.

## Contributing

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a Pull Request

## Future Improvements

- Integration with weather APIs for more accurate energy production estimates
- Support for multiple roof types and configurations
- Enhanced visualization of solar panel placement
- Integration with local solar incentive databases
- Mobile application development
- Real-time solar production monitoring
- Integration with smart home systems

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please:
1. Check the [documentation](docs/)
2. Open an issue in the GitHub repository
3. Contact the maintainers at support@example.com

## Acknowledgments

- OpenAI for providing the AI capabilities
- Google Maps for satellite imagery
- The open-source community for various libraries and tools 
