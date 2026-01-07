# WhatsApp Image Sender

 A mobile-optimized Streamlit application to:
 
 - Upload images to Google Drive (organized by type)
 - Browse / delete images from a gallery
 - Generate marketing posters using AI (OpenAI) from a product-detail image + product photo
 - Send selected images to selected contacts (current implementation uses a Telegram bot sender)

## Features

- **Contact management** (Industrial / Distributer / Technicians)
- **Upload Normal Images** to Google Drive
- **AI Poster Generator (6-step workflow)**
  - Upload product detail image
  - Extract text using OpenAI vision (via LangChain)
  - Choose a poster style (from `backend/promptselection.txt`)
  - Upload product photo
  - Generate a poster using OpenAI image generation
  - Upload generated poster to Drive or regenerate with improvements
- **Gallery** (browse, filter, delete)
- **Mobile-friendly Streamlit UI**

## Prerequisites

- Python 3.8+
- Google Cloud Project with **Google Drive API** enabled
- OpenAI API key (for text extraction + poster generation)
- (Optional) Telegram Bot token + Chat ID (used by the current sender)

## Setup

1. Clone the repository:
```bash
git clone <https://github.com/NeelShroff/WhatsApp-bot-.git>
cd WhatsApp-bot-
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

4. Create a `.env` file (local-only)

This repo uses `python-dotenv` (`load_dotenv()`) in multiple places.

- **Required**:
  - `OPENAI_API_KEY` (used by `backend/imageEdit.py` and the OCR step)

Example:

```env
OPENAI_API_KEY=your_openai_key_here
```

Notes:

- `.env` is ignored by `.gitignore` and must **not** be committed.

5. Configure Google Drive:
   - Go to Google Cloud Console
   - Create/select a project
   - Enable **Google Drive API**
   - Create **OAuth client credentials**
   - Download the JSON and place it at:
     - `credentials/credentials.json`

On first run, the app will open a browser login and create:

- `credentials/token.json`

Both are ignored by `.gitignore`.

6. (Optional) Configure Telegram sender

The current “Send” page sends images via a Telegram bot (see `utils/telegram_sender.py`).
You’ll need:

- A Telegram bot token (from BotFather)
- A Telegram chat id

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

## Project Structure

```
WhatsApp-bot-/
├── app.py                     # Streamlit home
├── pages/                     # Streamlit pages (Send / Upload / Gallery)
├── components/                # UI components (includes AI poster generator workflow)
├── components/step_backends/  # Backends for the 6-step generator
├── backend/                   # Prompt templates + OpenAI generation helpers
├── utils/                     # Drive handler, contact manager, telegram sender
├── requirements.txt
├── run_app.bat
├── credentials/               # Local-only (ignored): OAuth credentials + token
└── *_contacts.json            # Local-only (ignored): contact lists
```

## Data & Secrets (what should NOT be pushed)

These are deliberately ignored by `.gitignore`:

- `.env` (API keys)
- `credentials/` (Google OAuth `credentials.json` + generated `token.json`)
- `*_contacts.json` (your local contact lists)

If you accidentally committed a secret already, rotate it immediately.

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
