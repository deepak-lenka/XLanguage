import requests
import logging
from typing import Dict, Any, Optional
from requests.exceptions import RequestException, Timeout

class XAIService:
    """
    Service for interacting with X.AI API for chat completions
    
    Attributes:
        api_key (str): Authentication key for X.AI API
        base_url (str): Base URL for X.AI API endpoints
        logger (logging.Logger): Logger for tracking API interactions
    """
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize XAI Service with API configuration
        
        Args:
            api_key (str): X.AI API authentication key
            base_url (str, optional): Custom base URL for API. Defaults to official endpoint.
        """
        self.api_key = api_key
        self.base_url = base_url or "https://api.x.ai/v1"
        
        # Configure logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
    
    def _prepare_headers(self) -> Dict[str, str]:
        """
        Prepare standard headers for API requests
        
        Returns:
            Dict[str, str]: Headers for API request
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def _validate_response(self, response_data: Dict[Any, Any]) -> Dict[Any, Any]:
        """
        Validate and process API response
        
        Args:
            response_data (Dict): Raw response from API
        
        Returns:
            Dict: Processed response with guaranteed structure
        """
        try:
            # Check for standard OpenAI-like response structure
            if 'choices' in response_data and response_data['choices']:
                return response_data
            
            # Fallback for alternative response structures
            return {
                'choices': [{
                    'message': {
                        'content': str(response_data.get('message', 'No response content'))
                    }
                }]
            }
        except Exception as e:
            self.logger.error(f"Response validation error: {e}")
            return {
                'choices': [{
                    'message': {
                        'content': 'Error processing API response'
                    }
                }]
            }
    
    def get_response(
        self, 
        user_message: str, 
        system_message: str = "You are a helpful AI assistant.",
        model: str = "grok-beta",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[Any, Any]:
        """
        Get AI response from X.AI API
        
        Args:
            user_message (str): User's input message
            system_message (str, optional): System context for response
            model (str, optional): AI model to use
            temperature (float, optional): Response creativity/randomness
            max_tokens (int, optional): Maximum response length
        
        Returns:
            Dict: Processed API response
        """
        try:
            # Prepare payload
            payload = {
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                "model": model,
                "temperature": temperature,
                "stream": False
            }
            
            # Add optional max_tokens if specified
            if max_tokens is not None:
                payload["max_tokens"] = max_tokens
            
            # Make API request
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self._prepare_headers(),
                json=payload,
                timeout=30  # 30-second timeout
            )
            
            # Check HTTP status
            if response.status_code != 200:
                self.logger.error(f"API Error: {response.status_code} - {response.text}")
                return {
                    "error": f"API returned status {response.status_code}",
                    "choices": [{
                        'message': {
                            'content': 'Service temporarily unavailable'
                        }
                    }]
                }
            
            # Process response
            response_data = response.json()
            return self._validate_response(response_data)
        
        except Timeout:
            self.logger.warning("X.AI API request timed out")
            return {
                "error": "Request timed out",
                "choices": [{
                    'message': {
                        'content': 'Request timed out. Please try again.'
                    }
                }]
            }
        
        except RequestException as e:
            self.logger.error(f"Network error with X.AI API: {e}")
            return {
                "error": f"Network error: {str(e)}",
                "choices": [{
                    'message': {
                        'content': 'Network error occurred. Please check your connection.'
                    }
                }]
            }
        
        except Exception as e:
            self.logger.error(f"Unexpected error in X.AI Service: {e}")
            return {
                "error": "Unexpected error",
                "choices": [{
                    'message': {
                        'content': 'An unexpected error occurred. Our team has been notified.'
                    }
                }]
            }