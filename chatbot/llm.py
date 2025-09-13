import os
import json
import datetime
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Load environment variables
load_dotenv()

# Azure Inference credentials
AZURE_API_TOKEN = os.getenv("AZURE_MENTALHEALTH_TOKEN") 
AZURE_ENDPOINT = "https://models.github.ai/inference"
AZURE_MODEL = "openai/gpt-4.1" 

client = ChatCompletionsClient(
    endpoint=AZURE_ENDPOINT,
    credential=AzureKeyCredential(AZURE_API_TOKEN),
)

# Load intent keywords from external JSON
with open("intents.json", "r", encoding="utf-8") as f:
    INTENT_KEYWORDS = json.load(f)

# Profanity blacklist (customizable)
BLACKLIST_WORDS = ["damn", "shit", "fuck", "bastard"]

# -------- Mental Health Topic Detection -------- #
def is_mental_health_related(user_input, conversation_context=None):
    """
    Advanced mental health topic detection that considers context and intent.
    Returns True if it's mental health related, False otherwise.
    
    Args:
        user_input (str): The user's message
        conversation_context (list, optional): Previous messages for context
    """
    user_input = user_input.lower().strip()
    
    # Immediate exclusions for clearly technical/educational queries
    technical_patterns = [
        # Programming and technical queries
        r'\b(what is|define|explain|how to|tutorial|learn|teach me)\s+(python|javascript|java|html|css|sql|programming|coding|algorithm|function|variable|loop|array|object)\b',
        r'\b(install|setup|configure|debug|error|syntax|code|script|framework|library|api|database)\b',
        r'\b(vs code|visual studio|ide|compiler|interpreter|git|github|stack overflow)\b',
        
        # Academic subjects (non-emotional context)
        r'\b(what is|define|explain|formula|equation|theorem|calculate)\s+(math|mathematics|physics|chemistry|biology|calculus|algebra|geometry)\b',
        r'\b(history of|who is|when did|where is|capital of|population of)\b',
        
        # General information queries
        r'\b(weather|time|date|calendar|schedule|news|sports|music|movie|book|recipe)\b',
        r'\b(directions|location|address|map|gps|travel|flight|hotel)\b'
    ]
    
    import re
    for pattern in technical_patterns:
        if re.search(pattern, user_input):
            return False
    
    # Core emotional and mental health indicators
    mental_health_indicators = {
        # Direct emotional expressions
        'emotions': [
            'i feel', 'i\'m feeling', 'feeling', 'felt', 'emotions', 'emotional',
            'sad', 'happy', 'angry', 'frustrated', 'depressed', 'anxious', 
            'worried', 'scared', 'afraid', 'nervous', 'overwhelmed', 'lonely',
            'isolated', 'hopeless', 'helpless', 'guilty', 'ashamed', 'stressed'
        ],
        
        # Mental health conditions and symptoms
        'conditions': [
            'depression', 'anxiety', 'panic attack', 'panic', 'trauma', 'ptsd',
            'bipolar', 'adhd', 'ocd', 'eating disorder', 'self harm', 'suicide',
            'suicidal', 'insomnia', 'nightmare', 'nightmares'
        ],
        
        # Professional help and treatment
        'treatment': [
            'therapy', 'therapist', 'counseling', 'counselor', 'psychologist',
            'psychiatrist', 'medication', 'antidepressant', 'mental health'
        ],
        
        # Personal struggles and challenges (emotional context)
        'struggles': [
            'struggling with', 'having trouble', 'difficult time', 'hard time',
            'tough time', 'going through', 'dealing with', 'coping with',
            'can\'t handle', 'too much', 'breaking down', 'falling apart'
        ],
        
        # Help-seeking behaviors
        'help_seeking': [
            'need help', 'need support', 'need advice', 'need someone to talk',
            'don\'t know what to do', 'what should i do', 'how do i cope',
            'how do i deal', 'how do i handle', 'tips for managing', 'advice on',
            'give me tips', 'help me manage', 'how can i manage', 'manage it'
        ],
        
        # Physical symptoms with emotional context
        'physical_emotional': [
            'can\'t sleep', 'trouble sleeping', 'exhausted', 'no energy',
            'lost motivation', 'can\'t concentrate', 'can\'t focus', 'appetite',
            'tired all the time', 'physically drained', 'very tired', 'so tired',
            'really tired', 'extremely tired', 'actually tired'
        ],
        
        # Relationship and social issues
        'relationships': [
            'relationship problems', 'relationship issues', 'breakup', 'broke up',
            'fight with', 'argument with', 'family problems', 'friend problems',
            'social anxiety', 'trust issues', 'communication problems'
        ]
    }
    
    # Check for direct mental health indicators
    for category, keywords in mental_health_indicators.items():
        for keyword in keywords:
            if keyword in user_input:
                return True
    
    # Context-aware detection for conversational responses
    conversational_mental_health = [
        # Gratitude and acknowledgment in therapy context
        'thank you', 'thanks', 'that helps', 'that\'s helpful', 'i appreciate',
        'that makes sense', 'i understand', 'good advice', 'feel better',
        
        # Progress and improvement expressions
        'getting better', 'feeling better', 'making progress', 'improving',
        'helpful', 'working on myself', 'trying to', 'want to change',
        
        # Clarification and engagement
        'tell me more', 'how do i', 'what about', 'is it normal', 'am i',
        'should i', 'can you help', 'any suggestions'
    ]
    
    # If we have conversation context, these phrases are likely mental health related
    if conversation_context and len(conversation_context) > 0:
        for phrase in conversational_mental_health:
            if phrase in user_input:
                return True
    
    # Academic stress with emotional indicators
    academic_stress_patterns = [
        r'\b(nervous|anxious|worried|stressed|scared|afraid|overwhelmed)\s+(about|for|before)\s+(exam|test|presentation|defense|interview|assignment|project|deadline)\b',
        r'\b(feel|feeling)\s+(nervous|anxious|worried|stressed|overwhelmed|pressure)\b',
        r'\b(too much|can\'t handle|struggling with|having trouble with)\s+(school|university|college|studies|work|workload|deadlines)\b',
        r'\b(burnout|exhausted|tired)\s+(from|because of|due to)\s+(school|studies|work|assignments|projects)\b'
    ]
    
    for pattern in academic_stress_patterns:
        if re.search(pattern, user_input):
            return True
    
    # Simple length and personal pronoun check for very short responses
    if len(user_input.split()) <= 3:
        personal_responses = ['i am', 'i\'m', 'me too', 'yes', 'no', 'okay', 'ok', 'sure']
        if any(response in user_input for response in personal_responses) and conversation_context:
            return True
    
    return False

# -------- Intent Detection -------- #
def detect_intent(user_input):
    user_input = user_input.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in user_input for keyword in keywords):
            return intent
    return "general_support"

# -------- Prompt Engineering -------- #
def generate_prompt(user_input):
    intent = detect_intent(user_input)

    if intent == "crisis_intervention":
        return (
            "URGENT: User expressed suicidal ideation. "
            "Provide immediate crisis support using this template:\n"
            "1. Validate feelings: 'I hear how much pain you're in...'\n"
            "2. Safety check: 'Are you somewhere safe right now?'\n"
            "3. Emergency resources: Share suicide hotline numbers\n"
            "4. Offer next-step support\n"
            "--- User input: " + user_input
        )
    elif intent == "anxiety_support":
        return (
            "Provide CBT-based anxiety support:\n"
            "1. Psycho-education about anxiety\n"
            "2. Grounding techniques (5-4-3-2-1 method)\n"
            "3. Cognitive restructuring example\n"
            "4. Short breathing exercise\n"
            "--- User input: " + user_input
        )
    elif intent == "depression_support":
        return (
            "Offer depression support using behavioral activation:\n"
            "1. Validate experience\n"
            "2. Small activity suggestion\n"
            "3. Social connection idea\n"
            "4. Hope-instilling message\n"
            "--- User input: " + user_input
        )
    else:
        return (
            "Provide general mental health support with:\n"
            "1. Active listening reflection\n"
            "2. Open-ended question\n"
            "3. Psycho-education snippet\n"
            "4. Resource suggestion\n"
            "--- User input: " + user_input
        )

# -------- Azure LLM Query -------- #
def query_llm(prompt):
    system_prompt = (
        "You are **MindCare Companion** - an AI mental health supporter for students. "
        "You combine professional therapeutic techniques with compassionate support.\n\n"
        "Core Protocols:\n"
        "1. 🚨 CRISIS: Detect urgency, provide resources, escalate if needed\n"
        "2. 🧠 CBT: Use cognitive restructuring, behavioral activation\n"
        "3. 🧘 MINDFULNESS: Offer grounding techniques when appropriate\n"
        "4. 📊 PROGRESS: Track user patterns (but don't diagnose)\n\n"
        "Communication Rules:\n"
        "- Always validate before problem-solving\n"
        "- Use simple, jargon-free language\n"
        "- Limit responses to 3-5 sentences\n"
        "- Ask open-ended questions\n"
        "- Never make clinical diagnoses\n"
    )

    try:
        response = client.complete(
            messages=[
                SystemMessage(system_prompt),
                UserMessage(prompt),
            ],
            temperature=0.7,
            top_p=0.9,
            model=AZURE_MODEL,
        )
        content = response.choices[0].message.content
        return apply_safety_filters(content)
    except Exception as e:
        return "I'm having technical difficulties. Please try again later."

# -------- Safety Filter -------- #
def apply_safety_filters(response):
    for word in BLACKLIST_WORDS:
        response = response.replace(word, "[censored]")
    return response

# -------- Interaction Logger -------- #
def log_interaction(user_input, intent, response):
    with open("interaction_log.txt", "a", encoding="utf-8") as f:
        f.write(
            f"[{datetime.datetime.now()}] "
            f"Intent: {intent} | Input: {user_input} | Response: {response[:100]}...\n"
        )

# -------- Main Chatbot Function -------- #
def chatbot_response(user_input, is_first_message=False, conversation_context=None):
    # Check if the input is related to mental health
    if not is_mental_health_related(user_input, conversation_context):
        non_mental_health_response = (
            "I'm MindCare Companion, designed specifically to provide mental health and emotional support. "
            "I'm here to help you with feelings, stress, anxiety, relationships, academic pressure, or any emotional challenges you're facing.\n\n"
            "If you'd like to talk about how you're feeling or need emotional support, I'm here to listen. "
            "What's on your mind today? 💙"
        )
        log_interaction(user_input, "non_mental_health", non_mental_health_response)
        
        greeting = (
            "🌱 Welcome to MindCare Companion. I'm here to listen and support you.\n"
            "This is a safe space to share what's on your mind.\n\n"
            "Remember: I'm not a replacement for professional care.\n\n"
        ) if is_first_message else ""
        
        return greeting + non_mental_health_response
    
    # Process mental health related queries
    intent = detect_intent(user_input)
    prompt = generate_prompt(user_input)
    response = query_llm(prompt)

    log_interaction(user_input, intent, response)

    greeting = (
        "🌱 Welcome to MindCare Companion. I'm here to listen and support you.\n"
        "This is a safe space to share what's on your mind.\n\n"
        "Remember: I'm not a replacement for professional care.\n\n"
    ) if is_first_message else ""

    return greeting + response
