import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq, GroqError
import colorama
from colorama import Fore, Style

# Initialize colorama for cross-platform colored terminal output
colorama.init(autoreset=True)

# ---------------- CONFIGURATION ---------------- #
# 1. Temperature: Controls randomness/creativity.
#    Lower (e.g., 0.2) = more focused/deterministic
#    Higher (e.g., 0.8) = more creative/variable
TEMPERATURE = 0.7 

# 2. System Prompts (Personas)
SYSTEM_PROMPTS = {
    "1": ("Coding Tutor", "You are a patient and helpful coding tutor. Explain concepts clearly and simply. Give practical examples when useful."),
    "2": ("Concise Assistant", "You are a concise technical assistant. Provide direct, factual answers without any fluff or pleasantries."),
    "3": ("Friendly Mentor", "You are a friendly study mentor. You encourage the user, use emojis, and offer gentle guidance.")
}
DEFAULT_PROMPT_KEY = "1"

# 3. Model
MODEL_NAME = "openai/gpt-oss-20b"
# ----------------------------------------------- #

def get_persona():
    """Prompt the user to select a persona for the chatbot."""
    print(f"{Fore.CYAN}--- Select a Persona ---{Style.RESET_ALL}")
    for key, (name, _) in SYSTEM_PROMPTS.items():
        print(f"{key}. {name}")
    
    choice = input(f"Choose a persona (default {DEFAULT_PROMPT_KEY}): ").strip()
    if choice not in SYSTEM_PROMPTS:
        choice = DEFAULT_PROMPT_KEY
        print(f"Invalid choice, defaulting to {SYSTEM_PROMPTS[choice][0]}")
    
    name, prompt = SYSTEM_PROMPTS[choice]
    print(f"{Fore.GREEN}Persona set to: {name}{Style.RESET_ALL}\n")
    return prompt

def save_conversation(messages):
    """Save the conversation history to a JSON file when the session ends."""
    if len(messages) <= 1:  # Only system message, no chat happened
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversation_{timestamp}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=4)
        print(f"{Fore.YELLOW}Conversation saved to {filename}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Failed to save conversation: {e}{Style.RESET_ALL}")

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Retrieve the API key from environment
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print(f"{Fore.RED}Error: GROQ_API_KEY not found. Please create a .env file with your API key.{Style.RESET_ALL}")
        sys.exit(1)

    # Initialize the Groq SDK client
    client = Groq(api_key=api_key)

    print(f"{Fore.MAGENTA}=========================================={Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}      Welcome to the Groq CLI Chatbot     {Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}=========================================={Style.RESET_ALL}")
    print(f"Type '{Fore.YELLOW}quit{Style.RESET_ALL}' or '{Fore.YELLOW}exit{Style.RESET_ALL}' to end the chat.\n")

    system_prompt = get_persona()
    
    # Initialize conversation history with the chosen system prompt
    messages = [
        {"role": "system", "content": system_prompt}
    ]

    print(f"{Fore.CYAN}Chatbot is ready! Start typing...{Style.RESET_ALL}\n")

    while True:
        try:
            # Read user input
            user_input = input(f"{Fore.BLUE}You:{Style.RESET_ALL} ").strip()
            
            # Handle exit commands
            if user_input.lower() in ['quit', 'exit']:
                print(f"{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
                break
                
            # Handle empty input
            if not user_input:
                print(f"{Fore.RED}Input cannot be empty. Please say something.{Style.RESET_ALL}")
                continue
                
            # Add user message to history
            messages.append({"role": "user", "content": user_input})
            
            # Request response from the LLM
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=TEMPERATURE
            )
            
            # Extract assistant reply
            assistant_reply = response.choices[0].message.content
            print(f"\n{Fore.GREEN}Assistant:{Style.RESET_ALL} {assistant_reply}\n")
            
            # Add assistant reply to conversation memory
            messages.append({"role": "assistant", "content": assistant_reply})
            
        except GroqError as e:
            print(f"{Fore.RED}Groq API Error: {e}{Style.RESET_ALL}")
            # Remove the last user message so it doesn't break history format on retry
            messages.pop()
        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}Session interrupted by user. Goodbye!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")
            break

    # Export session history
    save_conversation(messages)

if __name__ == "__main__":
    main()
