import os
from flask import Flask, render_template, request, jsonify
from services.xai_service import XAIService
from config.config import XAI_API_KEY
import logging
from typing import Dict, Any
from werkzeug.exceptions import HTTPException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize XAI Service
try:
    xai_service = XAIService(XAI_API_KEY)
except Exception as e:
    logger.error(f"Failed to initialize XAI Service: {str(e)}")
    xai_service = None

@app.route('/')
def home():
    """Render the main chat page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat requests with enhanced error handling and response formatting
    
    Expected JSON payload:
    {
        'message': str,  # User's message
        'target_language': str (optional)  # Target language for response
    }
    """
    try:
        # Validate request data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract message and language
        user_message = data.get('message', '').strip()
        target_language = data.get('target_language', 'English')
        
        # Validate message
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Comprehensive system message for consistent response formatting
        system_message = f"""You are a helpful assistant. Please ensure your responses are formatted as follows:
- Use bullet points for lists.
- Keep paragraphs short (2-3 sentences max).
- Add line breaks between different sections.
- Use markdown formatting where appropriate.
- Respond directly and succinctly.
Respond in {target_language}."""


        
        # Handle potential XAI service initialization failure
        if xai_service is None:
            return jsonify({
                'error': 'AI service is currently unavailable',
                'choices': [{'message': {'content': 'Sorry, the AI service is temporarily down.'}}]
            }), 503
        
        # Get AI response
        response = xai_service.get_response(user_message, system_message)
        
        # Error handling for different response types
        if isinstance(response, dict):
            if 'error' in response:
                logger.error(f"XAI Service Error: {response['error']}")
                return jsonify({
                    'error': response['error'],
                    'choices': [{'message': {'content': 'An error occurred while processing your request.'}}]
                }), 500
            
            # If response is a dictionary, attempt to extract content
            content = response.get('choices', [{}])[0].get('message', {}).get('content', '')
            return jsonify({
                'choices': [{
                    'message': {
                        'content': content or 'Sorry, I could not generate a response.'
                    }
                }]
            })
        
        # Handle string or other response types
        return jsonify({
            'choices': [{
                'message': {
                    'content': str(response)
                }
            }]
        })
    
    except HTTPException as http_err:
        # Handle HTTP-specific exceptions
        logger.error(f"HTTP Error: {http_err}")
        return jsonify({
            'error': str(http_err),
            'choices': [{'message': {'content': 'An HTTP error occurred.'}}]
        }), http_err.code
    
    except Exception as e:
        # Catch-all for unexpected errors
        logger.error(f"Unexpected error in chat route: {str(e)}")
        return jsonify({
            'error': 'An unexpected error occurred',
            'choices': [{'message': {'content': 'Sorry, something went wrong.'}}]
        }), 500

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    """Handle bad request errors"""
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(500)
def internal_server_error(error):
    """Handle internal server errors"""
    return jsonify({'error': 'Internal server error'}), 500

# Run the application
if __name__ == '__main__':
    # Ensure debug mode is safe for production
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(
        host='0.0.0.0', 
        port=int(os.environ.get('PORT', 5000)), 
        debug=debug_mode
    )