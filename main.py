import os
import requests
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get API key from environment variables
GOOGLE_TRANSLATE_API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY")

def translate_text(text, target_language, source_language='auto'):
    """
    Translates text using Google Translate API
    
    Args:
        text (str): Text to translate
        target_language (str): Target language code (e.g., 'es' for Spanish)
        source_language (str): Source language code, or 'auto' for automatic detection
        
    Returns:
        dict: Translation result
    """
    url = "https://translation.googleapis.com/language/translate/v2"
    
    payload = {
        'q': text,
        'target': target_language,
        'key': GOOGLE_TRANSLATE_API_KEY
    }
    
    # Add source language if not auto
    if source_language != 'auto':
        payload['source'] = source_language
    
    try:
        response = requests.post(url, params=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        result = response.json()
        
        if 'data' in result and 'translations' in result['data']:
            return {
                'success': True,
                'translated_text': result['data']['translations'][0]['translatedText'],
                'detected_source_language': result['data']['translations'][0].get('detectedSourceLanguage')
            }
        else:
            return {'success': False, 'error': 'Unexpected API response format'}
            
    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    
    if not data or 'text' not in data or 'target_language' not in data:
        return jsonify({'success': False, 'error': 'Missing required parameters'}), 400
    
    text = data['text']
    target_language = data['target_language']
    source_language = data.get('source_language', 'auto')
    
    result = translate_text(text, target_language, source_language)
    return jsonify(result)

@app.route('/available_languages', methods=['GET'])
def get_available_languages():
    # You could make this dynamic by querying the API
    # Here's a static list of common languages and their codes
    languages = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh': 'Chinese (Simplified)',
        'zh-TW': 'Chinese (Traditional)',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'ru': 'Russian',
        'pt': 'Portuguese',
        'tr': 'Turkish'
    }
    
    return jsonify({'success': True, 'languages': languages})

if __name__ == '__main__':
    app.run(debug=True)