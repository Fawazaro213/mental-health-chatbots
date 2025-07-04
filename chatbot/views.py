from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import StartChatForm
from chatbot.llm import detect_intent, generate_prompt, query_llm
from django.core.mail import send_mail
from django.conf import settings
from chatbot.llm import chatbot_response
from django.utils.timezone import now, timedelta
from collections import defaultdict
from django.db.models import F

@login_required
def start_chat(request):
    if request.method == "POST":
        form = StartChatForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            message = form.cleaned_data["message"]

            # Create conversation
            convo = Conversation.objects.create(user=request.user, title=title)

            # Detect intent and save user message
            intent = detect_intent(message)
            user_msg = Message.objects.create(
                conversation=convo,
                sender="user",
                content=message,
                intent_detected=intent
            )

            # Get bot reply and save
            reply = chatbot_response(message, is_first_message=True)
            Message.objects.create(
                conversation=convo,
                sender="bot",
                content=reply,
                intent_detected=intent
            )

            # Crisis check (same as in ajax handler)
            if intent == "crisis_intervention":
                FlaggedMessage.objects.create(message=user_msg, reason=intent)
                send_mail(
                    subject="🚨 Crisis Message Detected",
                    message=f"A user sent a message flagged for crisis:\n\n{message}\n\nFrom user: {request.user.username}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=["admin@yoursite.com"],
                    fail_silently=True
                )

            return redirect("chat_session", convo_id=convo.id)
    else:
        form = StartChatForm()

    return render(request, "chatbot/start_chat.html", {"form": form})


@login_required
def chat_session(request, convo_id):
    convo = Conversation.objects.get(id=convo_id, user=request.user)

    # Group chats by time (Yesterday, Last Week, Last Month, Older)
    conversations = Conversation.objects.filter(user=request.user).order_by('-started_at')

    grouped_sessions = defaultdict(list)
    today = now().date()
    for chat in conversations:
        delta = today - chat.started_at.date()
        if delta.days == 0:
            label = "Today"
        elif delta.days == 1:
            label = "Yesterday"
        elif delta.days <= 7:
            label = "Last Week"
        elif delta.days <= 30:
            label = "Last Month"
        else:
            label = "Older"
        grouped_sessions[label].append(chat)

    return render(request, "chatbot/chat.html", {
        "conversation": convo,
        "sidebar_mode": "chat",
        "grouped_sessions": dict(grouped_sessions),
        "current_session": str(convo.id)
    })


@login_required
def ajax_chat_reply(request, convo_id):
    if request.method == "POST":
        convo = Conversation.objects.get(id=convo_id, user=request.user)
        user_input = request.POST.get("message")
        intent = detect_intent(user_input)

        user_msg = Message.objects.create(
            conversation=convo,
            sender="user",
            content=user_input,
            intent_detected=intent
        )

        prompt = generate_prompt(user_input)
        bot_reply = query_llm(prompt)

        bot_msg = Message.objects.create(
            conversation=convo,
            sender="bot",
            content=bot_reply,
            intent_detected=intent
        )

        # Flag if crisis
        if intent == "crisis_intervention":
            FlaggedMessage.objects.create(message=user_msg, reason=intent)
            # Notify admin
            send_mail(
                subject="🚨 Crisis Message Detected",
                message=f"A user sent a message flagged for crisis:\n\n{user_input}\n\nFrom user: {request.user.username}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["admin@yoursite.com"],
                fail_silently=True
            )

        return JsonResponse({
            "user_message": user_msg.content,
            "bot_response": bot_msg.content,
            "is_crisis": intent == "crisis_intervention"
        })
    

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Conversation
from django.contrib.auth.decorators import login_required

@require_POST
@login_required
def rename_chat(request):
    chat_id = request.POST.get("id")
    new_title = request.POST.get("title")
    try:
        convo = Conversation.objects.get(id=chat_id, user=request.user)
        convo.title = new_title
        convo.save()
        return JsonResponse({"success": True, "new_title": new_title})
    except Conversation.DoesNotExist:
        return JsonResponse({"success": False})

@require_POST
@login_required
def delete_chat(request):
    chat_id = request.POST.get("id")
    try:
        convo = Conversation.objects.get(id=chat_id, user=request.user)
        convo.delete()
        return JsonResponse({"success": True})
    except Conversation.DoesNotExist:
        return JsonResponse({"success": False})


@login_required
def chat_history(request):
    conversations = Conversation.objects.filter(user=request.user).order_by('-started_at')

    grouped = {
        "Today": [],
        "Yesterday": [],
        "Last 7 Days": [],
        "Last Month": [],
        "Older": [],
    }

    today = now().date()
    for convo in conversations:
        started = convo.started_at.date()
        delta = (today - started).days

        if delta == 0:
            grouped["Today"].append(convo)
        elif delta == 1:
            grouped["Yesterday"].append(convo)
        elif delta <= 7:
            grouped["Last 7 Days"].append(convo)
        elif delta <= 30:
            grouped["Last Month"].append(convo)
        else:
            grouped["Older"].append(convo)

    return render(request, "chatbot/chat_history.html", {
        "grouped_sessions": grouped,
        "sidebar_mode": "chat"  # so sidebar renders chat-specific layout
    })


@login_required
def chat_with_user(request, user_id):
    from django.shortcuts import get_object_or_404, redirect
    other_user = get_object_or_404(User, id=user_id)
    thread, _ = ChatThread.objects.get_or_create(
        user1=min(request.user, other_user, key=lambda u: u.id),
        user2=max(request.user, other_user, key=lambda u: u.id)
    )
    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            ChatMessage.objects.create(thread=thread, sender=request.user, content=content)
            return redirect('chat_with_user', user_id=other_user.id)

    messages = thread.messages.order_by('sent_at')
    return render(request, 'chat/chat.html', {'thread': thread, 'messages': messages, 'other_user': other_user})