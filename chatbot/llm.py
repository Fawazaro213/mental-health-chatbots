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
def is_mental_health_related(user_input):
    """
    Check if the user input is related to mental health or emotional support.
    Returns True if it's mental health related, False otherwise.
    """
    user_input = user_input.lower()
    
    # Mental health and emotional keywords
    mental_health_keywords = [
        # Emotions and feelings
        "feel", "feeling", "feelings", "emotion", "emotions", "mood", "moods",
        "sad", "happy", "angry", "frustrated", "depressed", "anxious", "worry", "worried",
        "scared", "afraid", "fear", "fearful", "nervous", "excited", "overwhelmed",
        "lonely", "isolated", "hopeless", "helpless", "guilty", "shame", "ashamed",
        
        # Mental health conditions
        "depression", "anxiety", "panic", "stress", "stressed", "trauma", "ptsd",
        "bipolar", "adhd", "ocd", "eating disorder", "self harm", "suicide", "suicidal",
        
        # Mental health related activities
        "therapy", "therapist", "counseling", "counselor", "psychologist", "psychiatrist",
        "medication", "antidepressant", "mental health", "wellbeing", "wellness",
        
        # Academic/life stress (common for students)
        "exam", "exams", "test", "tests", "study", "studying", "assignment", "assignments",
        "project", "projects", "deadline", "deadlines", "grade", "grades", "academic",
        "school", "university", "college", "pressure", "burnout", "workload",
        "defence", "defense", "presentation", "presentations", "interview", "interviews",
        
        # Relationships and social
        "relationship", "relationships", "friend", "friends", "family", "parents",
        "boyfriend", "girlfriend", "breakup", "break up", "conflict", "fight", "fighting",
        "social", "communication", "trust", "betrayal",
        
        # Life challenges
        "problem", "problems", "issue", "issues", "trouble", "difficulty", "difficulties",
        "challenge", "challenges", "struggle", "struggling", "hard time", "tough time",
        "crisis", "emergency", "urgent", "help", "support", "advice", "guidance",
        
        # Sleep and physical symptoms related to mental health
        "sleep", "insomnia", "nightmare", "nightmares", "tired", "exhausted", "fatigue",
        "appetite", "eating", "weight", "energy", "motivation", "concentrate", "focus",
        
        # Coping and recovery
        "cope", "coping", "manage", "managing", "recovery", "healing", "better",
        "improve", "improvement", "progress", "growth", "change", "changing"
    ]
    
    # Check if any mental health keywords are present
    return any(keyword in user_input for keyword in mental_health_keywords)

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
            "1. Psychoeducation about anxiety\n"
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
            "3. Psychoeducation snippet\n"
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
def chatbot_response(user_input, is_first_message=False):
    # Check if the input is related to mental health
    if not is_mental_health_related(user_input):
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
