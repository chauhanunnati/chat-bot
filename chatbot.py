import random
import json
import os
import wikipediaapi

MEMORY_FILE = "chatbot_memory.json"
wiki_wiki = wikipediaapi.Wikipedia("en")

# Load chatbot memory
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    return {}

# Save new responses to memory
def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file)

# Get response from Wikipedia
def search_wikipedia(query):
    page = wiki_wiki.page(query)
    if page.exists():
        return page.summary[:300] + "..."
    return "I couldn't find anything on that topic."

# Generate response
def generate_response(user_input, memory):
    user_input = user_input.lower()

    # Check if chatbot already knows the response
    for key in memory:
        if key in user_input:
            return random.choice(memory[key])

    # If unknown, search Wikipedia
    return search_wikipedia(user_input)

# Chatbot function
def chatbot():
    print("ChatBot: Hello! I can answer anything. Type 'bye' to exit.")

    memory = load_memory()

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "bye":
            print("ChatBot: Goodbye! Have a great day!")
            break

        response = generate_response(user_input, memory)

        if response:
            print("ChatBot:", response)
        else:
            print("ChatBot: I don't know that. Can you teach me?")
            new_response = input("Teach me: ")

            if user_input not in memory:
                memory[user_input] = []

            memory[user_input].append(new_response)
            save_memory(memory)
            print("ChatBot: Thanks! I've learned something new.")

chatbot()