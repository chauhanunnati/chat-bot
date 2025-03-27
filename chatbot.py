import random
import json
import os
import wikipediaapi
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Constants
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

# Pydantic model for request validation
class ChatRequest(BaseModel):
    message: str

# Create FastAPI app
app = FastAPI()

# Load memory on startup
memory = load_memory()

@app.post("/chat")
async def chat(request: ChatRequest):
    user_input = request.message
    
    if user_input.lower() == "bye":
        return {"response": "Goodbye! Have a great day!"}
    
    response = generate_response(user_input, memory)
    
    # Optional: Learning mechanism
    if not response:
        return {"response": "I don't know that. Can you teach me?"}
    
    return {"response": response}

# For local development and testing
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))