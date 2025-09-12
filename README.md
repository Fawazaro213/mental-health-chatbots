# Mental Health Chatbot 🧠💬

A comprehensive Django-based web application that provides AI-powered mental health support through conversational chatbots, mood tracking, and crisis intervention mechanisms.

## 🌟 Features

### Core Functionality
- **AI-Powered Chatbot**: GPT-4.1 integration via Azure AI for intelligent mental health conversations
- **Crisis Detection**: Automatic flagging of crisis-related messages with admin notifications
- **User Authentication**: Custom user management with university student verification
- **Mood Tracking**: Personal mood monitoring with historical data and analytics
- **Resource Library**: Curated mental health resources and emergency contacts
- **Administrative Dashboard**: Comprehensive admin panel for monitoring and management

### Security & Privacy
- Intent-based message classification for crisis intervention
- Secure user data handling with privacy controls
- Emergency contact integration
- Anonymous data collection options

## 🛠 Tech Stack

- **Backend**: Django 5.2.1
- **Database**: SQLite3 (development) / PostgreSQL (production ready)
- **AI Integration**: Azure AI Inference with GPT-4.1
- **Frontend**: Django Templates with Bootstrap styling
- **Authentication**: Custom User Model extending Django's AbstractUser
- **File Handling**: Pillow for image processing
- **API Integration**: Azure Core for cloud services

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)
- Azure AI API key (for chatbot functionality)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd mental-health-chatbots
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
AZURE_MENTALHEALTH_TOKEN=your_azure_ai_token_here
SECRET_KEY=your_django_secret_key_here
DEBUG=True
```

### 5. Set Up Database
```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser account
python manage.py createsuperuser
```

### 6. Load Sample Data (Optional)
```bash
# Load university student data
python manage.py load_students students.json
```

### 7. Run the Application
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## 🏗 Project Architecture

### Django Apps Structure

```
mental-health-chatbots/
├── mental_health_chatbot/    # Main project configuration
├── users/                    # User authentication & profiles
├── chatbot/                  # AI chatbot functionality
├── mood/                     # Mood tracking system
├── resources/                # Mental health resources
├── adminpanel/              # Administrative tools
├── templates/               # Shared HTML templates
├── static/                  # Static files (CSS, JS, images)
└── media/                   # User-uploaded content
```

### Key Models

#### User Management (`users/`)
- **CustomUser**: Extended user model with mental health preferences
- **UserProfile**: Additional user information and mood statistics
- **UniversityStudent**: Student records for verification
- **Notification**: System notifications for users

#### Chatbot System (`chatbot/`)
- **Conversation**: Chat sessions between users and bot
- **Message**: Individual chat messages with intent detection
- **FlaggedMessage**: Crisis-flagged messages requiring review
- **ChatThread**: Person-to-person chat functionality

#### Mood Tracking (`mood/`)
- **MoodEntry**: User mood records with scores (1-10) and notes

### URL Structure

```
/                    # Home page
/u/login/           # User authentication
/u/register/        # User registration
/u/profile/         # User profile management
/c/                 # Chatbot interface
/c/history/         # Conversation history
/mood/              # Mood tracking
/resources/         # Mental health resources
/admin-tools/       # Administrative panel
/admin/            # Django admin interface
```

## 🔧 Configuration

### Database Settings
The application uses SQLite for development. For production, configure PostgreSQL in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mental_health_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Azure AI Configuration
Ensure your Azure AI token is configured:
1. Set `AZURE_MENTALHEALTH_TOKEN` in your environment
2. Configure the AI endpoint in `chatbot/llm.py`

### Email Configuration
For crisis notifications, configure email settings:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your_smtp_server'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email'
EMAIL_HOST_PASSWORD = 'your_password'
```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users
python manage.py test chatbot
```

## 📊 Key Features Deep Dive

### Crisis Intervention System
- Keyword-based intent detection using `intents.json`
- Automatic flagging of concerning messages
- Admin email notifications for urgent cases
- Review system for flagged content

### Mood Analytics
- Daily mood scoring (1-10 scale)
- Historical mood tracking
- Average mood calculation
- Visual mood trends (frontend implementation pending)

### User Privacy Controls
- Optional data collection settings
- Anonymous usage statistics
- Secure data handling practices
- GDPR-compliant user data management

## 🔐 Security Considerations

- Custom authentication backend
- CSRF protection enabled
- Secure file upload handling
- Input sanitization for chat messages
- Crisis detection and reporting mechanisms

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG = False`
2. Configure secure `SECRET_KEY`
3. Set up proper database (PostgreSQL recommended)
4. Configure static file serving
5. Set up HTTPS
6. Configure email backend for notifications
7. Set up monitoring and logging

### Environment Variables for Production
```env
DEBUG=False
SECRET_KEY=your_production_secret_key
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
AZURE_MENTALHEALTH_TOKEN=your_azure_token
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow Django best practices
- Write tests for new functionality
- Update documentation for new features
- Follow PEP 8 style guidelines
- Add proper error handling and logging

## 📝 API Documentation

### Chatbot Endpoints
- `POST /c/send/` - Send message to chatbot
- `GET /c/history/` - Retrieve conversation history
- `GET /c/conversations/` - List user conversations

### Mood Tracking Endpoints
- `POST /mood/add/` - Add new mood entry
- `GET /mood/history/` - Get mood history
- `GET /mood/stats/` - Get mood statistics

## 🔧 Troubleshooting

### Common Issues

**Database Migration Errors**
```bash
python manage.py migrate --run-syncdb
```

**Static Files Not Loading**
```bash
python manage.py collectstatic
```

**Azure AI Connection Issues**
- Verify your Azure AI token is correct
- Check network connectivity
- Ensure token has proper permissions

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django community for the excellent framework
- Azure AI team for the GPT integration capabilities
- Mental health professionals for guidance on best practices
- Open source contributors who made this project possible

## 📞 Support

For support, please contact:
- Email: support@mindcare.ng
- Admin: admin@mindcare.ng

## 🗺 Roadmap

### Upcoming Features
- [ ] Mobile app development (React Native)
- [ ] Advanced mood analytics with charts
- [ ] Group therapy session scheduling
- [ ] Integration with wearable devices
- [ ] Multi-language support
- [ ] Improved AI conversation capabilities
- [ ] Therapist matching system
- [ ] Crisis hotline integration

---

**Note**: This application is designed to supplement, not replace, professional mental health services. Users experiencing severe mental health crises should seek immediate professional help.