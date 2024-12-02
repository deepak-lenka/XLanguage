import pytest
from app import app
from services.xai_service import XAIService

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that home page loads successfully"""
    rv = client.get('/')
    assert rv.status_code == 200

def test_chat_endpoint(client):
    """Test the chat endpoint"""
    data = {
        'message': 'Hello',
        'target_language': 'Spanish'
    }
    rv = client.post('/chat', json=data)
    assert rv.status_code == 200
    assert 'response' in rv.get_json()

def test_xai_service():
    """Test XAI service initialization"""
    service = XAIService()
    assert service is not None
