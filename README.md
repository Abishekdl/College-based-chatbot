# College Chatbot

A Flask-based intelligent chatbot application designed to assist with college-related queries. The chatbot uses Natural Language Processing (NLP) and a neural network model to understand and respond to user queries.

## Features

- Real-time chat interface
- Natural language understanding using NLTK
- Pattern matching and intent recognition
- Responsive web interface
- Support for various college-related queries including:
  - Course information
  - Fee structure
  - College timing
  - Contact information
  - Schedule queries
  - General assistance

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **NLP**: NLTK (Natural Language Toolkit)
- **Neural Network**: PyTorch
- **Data Format**: JSON

## Project Structure

```plaintext
chatbot/
├── app.py              # Flask application server
├── nltk_utils.py       # NLTK utilities for text processing
├── intents.json        # Training data and response patterns
├── static/
│   ├── app.js         # Frontend JavaScript
│   ├── style.css      # CSS styling
│   └── images/        # Image assets
└── templates/
    └── base.html      # Main HTML template

## Setup and Installation
1. Clone the repository
2. Install dependencies:
pip install -r requirements.txt

3. Install NLTK data:
import nltk
nltk.download('punkt')

4. Run the application:
python app.py
