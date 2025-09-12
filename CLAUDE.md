# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django-based mental health chatbot web application that provides mental health support through AI-powered conversations. The system includes user management, mood tracking, resources, and administrative tools.

## Development Commands

### Running the Application
```bash
# Start development server
python manage.py runserver

# Load student data
python manage.py load_students students.json
```

### Database Management
```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Project Architecture

### Django Apps Structure
- **users**: Custom user authentication with `CustomUser` model, user profiles, and university student records
- **chatbot**: Core chatbot functionality with conversation management, LLM integration, and message flagging
- **mood**: Mood tracking system for users
- **resources**: Mental health resources and contact information
- **adminpanel**: Administrative tools and dashboards

### Key Components

#### Authentication & Users (`users/`)
- Uses `CustomUser` extending Django's `AbstractUser`
- `UserProfile` links to `UniversityStudent` records
- Custom authentication backend in `backends.py`
- Template tags for user-related functionality

#### Chatbot System (`chatbot/`)
- **LLM Integration**: `llm.py` contains Azure AI integration with GPT-4.1
- **Intent Detection**: Uses `intents.json` for keyword-based intent classification
- **Models**: `Conversation`, `Message`, `FlaggedMessage`, `ChatThread`
- **Crisis Intervention**: Automatic flagging for crisis-related messages

#### Configuration
- **Settings**: Main settings in `mental_health_chatbot/settings.py`
- **Database**: SQLite3 for development (configurable)
- **Static Files**: Configured for both development and production
- **Custom User Model**: `AUTH_USER_MODEL = 'users.CustomUser'`

### Environment Variables Required
- `AZURE_MENTALHEALTH_TOKEN`: Azure AI API token for LLM functionality

### Database Models Relationships
- `CustomUser` ↔ `UserProfile` (OneToOne)
- `UserProfile` ↔ `UniversityStudent` (OneToOne, optional)
- `Conversation` → `CustomUser` (ForeignKey)
- `Message` → `Conversation` (ForeignKey)
- `FlaggedMessage` → `Message` (OneToOne)

### URL Structure
- `/` - Home page
- `/c/` - Chatbot interactions
- `/u/` - User authentication and profiles
- `/mood/` - Mood tracking
- `/resources/` - Mental health resources
- `/admin-tools/` - Administrative panel

### Key Files
- `intents.json`: Intent classification keywords for crisis intervention and support categories
- `students.json`: University student data for user verification
- `requirements.txt`: Python dependencies including Django 5.2.1, Azure AI, and supporting packages

## Development Notes

- The application uses Django 5.2.1 with SQLite for development
- Time zone is set to 'Africa/Lagos'
- Custom middleware may be present for specific functionality
- Templates are stored in a shared `templates/` directory
- Static files are served from `static/` directory during development