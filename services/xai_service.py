import requests

class XAIService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.x.ai/v1/chat/completions"

    def get_response(self, user_message, system_message):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": system_message
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "model": "grok-beta",
                "stream": False,
                "temperature": 0.7,  # Added some randomness
                "timeout": 30  # Increased timeout
            }

            response = requests.post(
                self.base_url, 
                headers=headers, 
                json=payload,
                timeout=30  # Increased timeout from 10 to 30 seconds
            )
            
            # Check if the response is successful
            if response.status_code == 200:
                return response.json()
            else:
                error_message = f"API Error: Status {response.status_code}"
                print(error_message)
                return {"error": error_message}
                
        except requests.exceptions.Timeout:
            error_message = "Request timed out. Please try again."
            print(error_message)
            return {"error": error_message}
        except requests.exceptions.RequestException as e:
            error_message = f"Error calling X.AI API: {str(e)}"
            print(error_message)
            return {"error": error_message}
