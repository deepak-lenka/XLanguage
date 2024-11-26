from flask import Flask, render_template, request, jsonify
from services.xai_service import XAIService
from config.config import XAI_API_KEY
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
xai_service = XAIService(XAI_API_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user_message = data.get('message')
        target_language = data.get('target_language', 'English')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Simple system message
        system_message = f"You are a helpful assistant. Respond in {target_language}."
        
        # Get response from X.AI
        response = xai_service.get_response(user_message, system_message)
        
        if 'error' in response:
            return jsonify(response), 500
            
        return jsonify(response)

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
