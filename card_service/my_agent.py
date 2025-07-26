from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled, ModelSettings
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import requests

import asyncio

load_dotenv()
set_tracing_disabled(True)

BASE_URL = os.getenv("BASE_URL")

# Async client with Gemini API configuration
provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",

)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.5-flash",
    openai_client=provider,


)

# Tool wrappers
@function_tool
def add_card(title: str, description: str = None):
    """Add a card to the database."""
    response = requests.post(f"{BASE_URL}/cards/", json={"title": title, "description": description})
    return response.json()

@function_tool
def remove_card(card_id: str = None, title: str = None):
    """Delete a card by id or by title. If card_id is given, delete by id. If title is given, delete by title."""
    if card_id:
        if card_id == "None" or card_id is None:
            return {"error": "Invalid card_id provided."}
        response = requests.delete(f"{BASE_URL}/cards/{card_id}")
        return response.json()
    elif title:
        response = requests.get(f"{BASE_URL}/cards/")
        cards = response.json()
        for card in cards:
            if card.get("title", "").lower() == title.lower():
                card_id = card.get("id")
                if not card_id or card_id == "None":
                    return {"error": "No card found with the provided title."}
                delete_response = requests.delete(f"{BASE_URL}/cards/{card_id}")
                return delete_response.json()
        return {"error": f"Card not found with the provided title '{title}'."}
    else:
        return {"error": "Provide either card_id or title to delete a card."}

@function_tool
def modify_card(card_id: str = None, title: str = None, new_title: str = None, description: str = None):
    """Update a card by id or by title. If card_id is given, update by id. If title is given, update by title."""
    update_data = {}
    if new_title is not None:
        update_data["title"] = new_title
    if description is not None:
        update_data["description"] = description
    
    if card_id:
        if card_id == "None" or card_id is None:
            return {"error": "Invalid card_id provided."}
        response = requests.patch(f"{BASE_URL}/cards/{card_id}", json=update_data)
        return response.json()
    elif title:
        response = requests.get(f"{BASE_URL}/cards/")
        cards = response.json()
        for card in cards:
            if card.get("title", "").lower() == title.lower():
                card_id = card.get("id")
                if not card_id or card_id == "None":
                    return {"error": "No card found with the provided title."}
                patch_response = requests.patch(f"{BASE_URL}/cards/{card_id}", json=update_data)
                return patch_response.json()
        return {"error": f"Card not found with the provided title '{title}'."}
    else:
        return {"error": "Provide either card_id or title to update a card."}

@function_tool
def fetch_card(card_id: str = None, title: str = None):
    """Get a card by id or by title. If card_id is given, get by id. If title is given, get by title."""
    if card_id:
        if card_id == "None" or card_id is None:
            return {"error": "Invalid card_id provided."}
        response = requests.get(f"{BASE_URL}/cards/{card_id}")
        return response.json()
    elif title:
        response = requests.get(f"{BASE_URL}/cards/")
        cards = response.json()
        for card in cards:
            if card.get("title", "").lower() == title.lower():
                card_id = card.get("id")
                if not card_id or card_id == "None":
                    return {"error": "No card found with the provided title."}
                return card
        return {"error": f"Card not found with the provided title '{title}'."}
    else:
        return {"error": "Provide either card_id or title to get a card."}

@function_tool
def fetch_all_cards():
    """Get all cards."""
    response = requests.get(f"{BASE_URL}/cards/")
    return response.json()



# Agent with comprehensive instructions
agent = Agent(
    name="CardManager",
    instructions="""You are CardManager, an intelligent assistant for managing a card database. You can perform the following operations:

1. **Add Cards**: Create new cards with title and optional description
2. **Get Cards**: Retrieve cards by ID or title, or list all cards
3. **Update Cards**: Modify existing cards by ID or title
4. **Delete Cards**: Remove cards by ID or title

**Key Features:**
- You can work with cards using either their ID or title
- When updating cards, you can change the title, description, or both
- You provide clear, helpful responses and handle errors gracefully
- You always confirm the action taken and provide relevant details

**Usage Examples:**
- "Add a card titled 'Meeting Notes' with description 'Important discussion points'"
- "Get the card with title 'Meeting Notes'"
- "Update the card titled 'Meeting Notes' to have description 'Updated discussion points'"
- "Delete the card titled 'Meeting Notes'"
- "Show me all cards"

Always be helpful, clear, and confirm what action you're taking before executing it.""",

    tools= [add_card, remove_card, modify_card, fetch_card, fetch_all_cards],
    model= model,
    model_settings=ModelSettings(
        temperature= 1.2,
        tool_choice="required",

    ),
    tool_use_behavior="run_llm_again",


)


async def interactive_agent():
    print("Type 'exit' or 'quit' to stop.")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            print("Exiting interactive agent.")
            break
        result = await Runner.run(starting_agent=agent, input=user_input)
        # Print the agent's final output in bold green
        print(f"\033[1;32mAgent: {result.final_output}\033[0m")

if __name__ == "__main__":
    asyncio.run(interactive_agent()) 
