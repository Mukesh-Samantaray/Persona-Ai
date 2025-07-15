# Reddit Persona AI

This project scrapes a Reddit user's posts/comments and uses Google's Gemini AI to generate a psychological persona.

## Features

- Extracts Reddit comments and text-only posts
- Summarizes motivation, personality traits, habits, frustrations, etc.
- Visual personality spectrum
- Downloadable `.txt` persona file
- Streamlit UI with reset and error handling

## Installation

### 1. Clone & Set Up Virtual Environment

```bash
git clone https://github.com/your-repo/reddit-persona.git
cd reddit-persona

python -m venv venv
venv\\Scripts\\activate

pip install -r requirements.txt

streamlit run app.py
```
