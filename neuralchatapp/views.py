from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Chat
from django.conf import settings
import openai
import uuid
import os


openai.api_key = settings.OPENAI_API_KEY


def welcome_page(request):
    return render(request, 'welcome_page.html')

@login_required
def new_chat(request):
    if request.method == 'POST':
        user_input = request.POST.get('message_input')

        # Get the currently logged-in user
        user = request.user

        # Check if there's an existing chat with a reply
        existing_chat = Chat.objects.filter(user=user, reply__isnull=False).first()

        if existing_chat:
            # If there's an existing chat with a reply, update the existing chat with the user input
            existing_chat.message = user_input
            existing_chat.save()

            # Generate a response using GPT-3
            response = generate_gpt_response(user_input, context=existing_chat.reply)

            # Update the existing chat object with GPT-3 response
            existing_chat.reply = response
            existing_chat.save()

            # Redirect to the chat_reply page with the existing chat id
            return redirect('chat_reply', id=existing_chat.id)

        else:
            # If there's no existing chat with a reply, create a new chat instance
            user_chat = Chat.objects.create(user=user, message=user_input, reply="")
            user_chat.save()

            # Generate a response using GPT-3
            response = generate_gpt_response(user_input, context="")

            # Update the new chat object with GPT-3 response
            user_chat.reply = response
            user_chat.save()

            # Redirect to the chat_reply page with the new chat id
            return redirect('chat_reply', id=user_chat.id)

    return render(request, 'neuralchatapp/new_chat.html')

@login_required
def chat_reply(request, id):
    chat = get_object_or_404(Chat, id=id)

    if request.method == 'POST':
        user_input = request.POST.get('message_input')

        # Create a new chat object and save user input
        user_chat = Chat.objects.create(user=chat.user, message=user_input, reply="")
        user_chat.save()

        # Generate a response using GPT-3
        response = generate_gpt_response(user_input, context=chat.reply)

        # Update the chat object with GPT-3 response
        user_chat.reply = response
        user_chat.save()

        # Do further processing on the response here

        # Pass the updated chat to the template
        return render(request, 'neuralchatapp/chat_reply.html', {'chat': user_chat})

    return render(request, 'neuralchatapp/chat_reply.html', {'chat': chat})

def generate_gpt_response(user_input, context=""):
    # Call OpenAI GPT-3 API for response generation
    prompt = f"Conversation with a human.\nHuman: {user_input}\nAI:{context}\n"
    response = openai.Completion.create(
        model="babbage-002",  # Use the recommended replacement for the specific model
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", " Human:", " AI:"]
    )
    return response.choices[0].text.strip()

def chat_details(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    return render(request, 'neuralchatapp/chat_details.html', {'chat': chat})