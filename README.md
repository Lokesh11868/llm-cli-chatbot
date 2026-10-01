# llm-cli-chatbot

A simple Command-Line Interface (CLI) chatbot powered by the Groq API and Llama 3.1. This project demonstrates fundamental API interactions, conversation memory, and prompt engineering.

## Features
- Integrates with Groq LLM (`llama3-8b-8192`).
- CLI interface with a continuous chat loop.
- Conversation memory (retains context of earlier messages).
- Selectable system prompts/personas.
- Configurable temperature control.
- Graceful error handling for API failures and empty inputs.
- Colored terminal output for readability (`colorama`).
- Automatically exports the session conversation to a JSON file upon exit.

## Tech Stack
- **Python 3**
- **Groq API**
- **Llama 3.1 Model**
- **python-dotenv** (for environment variable management)
- **colorama** (for colored terminal outputs)

## Project Structure
```text
llm-cli-chatbot/
├── chatbot.py                 <- Main CLI chat loop
├── .env.example               <- Template for API key
├── .gitignore                 <- Git ignore rules
├── requirements.txt           <- Python dependencies
├── reflections.md             <- Observations on prompt engineering
├── sample_conversation.json   <- Example exported session
└── README.md                  <- Project documentation
```

## Prerequisites
- Python 3.7 or higher installed on your system.
- A free Groq API key from [Groq Console](https://console.groq.com).

## Setup
1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository_url>
   cd llm-cli-chatbot
   ```

2. **Create a virtual environment (Optional but recommended):**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and add your Groq API key:
     ```env
     GROQ_API_KEY=your_actual_api_key_here
     ```

## Usage
Start the chatbot by running:
```bash
python chatbot.py
```
- The application will ask you to select a persona.
- Type your messages to chat. The bot remembers previous context.
- Type `quit` or `exit` to stop the program. The session will automatically be saved to a `.json` file in the same directory.

## Prompt Engineering Experiment
The script provides three system prompts to test different personas:
1. **Coding Tutor**: Patient, clear, provides code examples.
2. **Concise Assistant**: Direct, factual, no pleasantries.
3. **Friendly Mentor**: Encouraging, warm, uses emojis.

## Temperature Experiment
The `TEMPERATURE` variable in `chatbot.py` is set to `0.7` by default.
- Lower values (e.g. `0.2`) yield deterministic, highly consistent responses.
- Higher values (e.g. `0.8+`) yield more creative and varied text.

## Error Handling
- **Empty input**: The bot will notify you without making a useless API call.
- **API Errors**: If Groq returns an error (e.g., bad API key, rate limit), it is caught and printed without crashing the program, and the conversation state remains valid.

## Security
- The Groq API key is stored locally in `.env`.
- `.env` is listed in `.gitignore` so the key is never accidentally committed to the repository.
- **Never expose or commit your API key.**

## Example Interaction
```
--- Select a Persona ---
1. Coding Tutor
2. Concise Assistant
3. Friendly Mentor
Choose a persona (default 1): 1
Persona set to: Coding Tutor

Chatbot is ready! Start typing...

You: What is a string in Python?

Assistant: In Python, a string is a sequence of characters enclosed in either single quotes ('...') or double quotes ("..."). 

You: quit
Goodbye!
Conversation saved to conversation_20261001_103045.json
```
