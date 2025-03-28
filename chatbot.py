import random
import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import wikipediaapi

# Constants
MEMORY_FILE = "chatbot_memory.json"
USER_AGENT = "NatureNexisChatbot/1.0 (contact: chauhan.unnati10@gmail.com)"
wiki_wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent=USER_AGENT
)

# Load chatbot memory
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    return {
        "wildlife": [
            "I'm knowledgeable about various wildlife species. What would you like to know?",
            "I can help you learn about animals and their habitats."
        ],
        "hello": [
            "Hello! I'm NatureNexis, your wildlife companion.",
            "Hi there! Ready to explore the world of wildlife?"
        ]
    }

# Save new responses to memory
def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file)

# Get response from Wikipedia
def search_wikipedia(query): 
    try:
        page = wiki_wiki.page(query)
        if page.exists():
            summary = page.summary
            return summary[:300] + "..." if len(summary) > 300 else summary
        return f"I couldn't find detailed information about '{query}'."
    except Exception as e:
        return f"An error occurred while searching: {str(e)}"

# Generate response
def generate_response(user_input, memory):
    user_input = user_input.lower()
    
    # Check predefined memory first
    for key, responses in memory.items():
        if key in user_input:
            return random.choice(responses)
    
    # If no predefined response, search Wikipedia
    return search_wikipedia(user_input)

# Pydantic model for request validation
class ChatRequest(BaseModel):
    message: str

# Create FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load memory on startup
memory = load_memory()

@app.post("/chat")
async def chat(request: ChatRequest):
    user_input = request.message
    
    if user_input.lower() in ["bye", "goodbye"]:
        return {"response": "Goodbye! Have a great day exploring wildlife!"}
    
    response = generate_response(user_input, memory)
    
    return {"response": response}

# For local development and testing
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
