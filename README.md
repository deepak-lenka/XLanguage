# XLanguage - Multilingual Chat 



## 🌍 Overview

XLanguage is a sophisticated multilingual chat interface that leverages the power of X.AI to provide seamless communication across multiple languages. With support for various languages across European, Asian, Middle Eastern, African, and other regions, XLanguage breaks down language barriers in real-time conversation.

## ✨ Features

- **🌐 Multilingual Support**
  - European Languages (English, Spanish, French, German, etc.)
  - Asian Languages (Chinese, Japanese, Korean, Hindi, etc.)
  - Middle Eastern Languages (Arabic, Hebrew, Persian, Turkish)
  - African Languages (Swahili, Amharic, Zulu)
  - Other Regional Variants

- **🎯 Key Capabilities**
  - Real-time language switching
  - Intuitive user interface
  - Responsive design
  - Typing indicators
  - Message history
  - Error handling
  - Copy message functionality with formatting preservation
  - Secure API key management

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- X.AI API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/deepak-lenka/XLanguage.git
cd XLanguage
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
- Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
- Edit `.env` and add your X.AI API key:
```
XAI_API_KEY=your_api_key_here
```

4. **Run the application**
```bash
flask run
```
The application will be available at http://127.0.0.1:5000

## 🛠 Technical Stack

- **Backend**: Flask (Python web framework)
- **API Integration**: X.AI API for language processing
- **Error Handling**: Comprehensive logging and error management
- **Configuration**: Environment-based configuration
- **Session Management**: Conversation state management

## 📁 Project Structure

```
XLanguage/
├── app.py              # Main Flask application
├── config/            # Configuration files
├── services/          # Core services (XAI, Conversation)
├── static/            # Static assets
├── templates/         # HTML templates
└── requirements.txt   # Project dependencies
```

## 🔧 Configuration

1. **Environment Variables**
   Create a `.env` file with the following variables:
   ```
   XAI_API_KEY=your_api_key_here
   FLASK_DEBUG=False  # Set to True for development
   ```

2. **API Configuration**
   - Configure X.AI API settings in `config/config.py`
   - Adjust conversation settings in `services/conversation_manager.py`

## 💻 Development Setup

1. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## 🔒 Security

- API keys are stored securely in `.env` file
- `.env` is excluded from git repository
- Environment-specific configurations are supported
- Proper error handling for missing API keys

## 💡 Recent Updates

- Added secure API key management using environment variables
- Improved copy functionality with better text formatting
- Enhanced error handling and logging
- Added development environment configuration
- Created `.env.example` for easier setup

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🔒 Security

- API keys and sensitive data are managed through environment variables
- Debug mode is configurable via environment settings
- Comprehensive error handling to prevent information leakage

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
