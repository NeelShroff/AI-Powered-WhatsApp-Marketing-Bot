# WhatsApp Image Sender

A mobile-optimized Streamlit application for sending images via WhatsApp with Google Drive integration.

## Features

- Contact selection and management
- Image upload to Google Drive
- Image gallery with filtering
- Mobile-optimized interface
- Dark/Light theme support
- Image processing (resize, format conversion)
- Input validation
- Comprehensive logging

## Prerequisites

- Python 3.8 or higher
- Google Cloud Project with Drive API enabled
- WhatsApp Business API access
- Streamlit account

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/whatsapp-image-sender.git
cd whatsapp-image-sender
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your credentials
```

5. Configure Google Drive:
   - Go to Google Cloud Console
   - Create a new project
   - Enable Drive API
   - Create credentials (OAuth 2.0)
   - Download credentials and save as `credentials.json`

6. Configure WhatsApp Business API:
   - Sign up for WhatsApp Business API
   - Get your API credentials
   - Update the .env file with your credentials

## Running the Application

1. Start the application:
```bash
# Windows
.\run_app.bat

# Linux/Mac
streamlit run app.py
```

2. Open your browser and navigate to:
```
http://localhost:8501
```

## Development

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest
```

3. Format code:
```bash
black .
```

4. Check code style:
```bash
flake8
```

## Project Structure

```
whatsapp-image-sender/
├── .gitignore                 # Git ignore file
├── README.md                  # Project documentation
├── requirements.txt           # Project dependencies
├── setup.py                   # Package setup file
├── run_app.bat               # Windows batch file to run the app
├── app.py                    # Main application entry point
├── src/                      # Source code directory
│   ├── __init__.py
│   ├── config.py             # Configuration settings
│   ├── services.py           # Service layer
│   ├── pages/                # Page modules
│   │   ├── __init__.py
│   │   ├── send_page.py
│   │   ├── upload_page.py
│   │   └── gallery_page.py
│   └── utils/                # Utility functions
│       ├── __init__.py
│       ├── image_processing.py
│       ├── validation.py
│       └── logger.py
└── logs/                     # Log files directory
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. 