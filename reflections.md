# Prompt Engineering & Temperature Reflections

## 1. What is a system prompt, and why does it change the bot's behavior?
A system prompt is a set of initial instructions given to the LLM before the user starts chatting. It establishes the AI's persona, boundaries, and tone. It changes the bot's behavior because the LLM uses this initial context to frame all subsequent responses. For instance, when I set the system prompt to "Concise Assistant," the model provided very short, direct answers without pleasantries. When changed to "Friendly Mentor," it used emojis and a warmer, more encouraging tone.

## 2. What did changing the temperature actually do to the responses you got?
The temperature parameter controls the randomness of the model's predictions. 
During my experiments:
- **At a lower temperature (e.g., 0.2):** The bot gave very predictable, highly focused, and almost mechanical answers. It would give the exact same or very similar response if asked the same question twice.
- **At a higher temperature (e.g., 0.8):** The bot's responses varied more wildly. It introduced different vocabulary, structure, and sometimes slightly creative analogies to explain the same concepts. It felt less rigid but sometimes slightly less focused.

## 3. What was the trickiest part of getting the API call or conversation memory working?
The trickiest part of getting the conversation memory working was ensuring that the message list correctly interleaved `user` and `assistant` roles. If an API call fails (for example, due to a network error), the user's message was already added to the list. If I didn't remove that failed message from the `messages` array, the next attempt would send two consecutive `user` messages, which could confuse the API or break the flow. Adding the `messages.pop()` in the exception handler resolved this issue.
