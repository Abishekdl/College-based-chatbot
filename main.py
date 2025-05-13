import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_input: str, patterns: list[str]) -> str | None:
    exact_matches = [pattern for pattern in patterns if pattern.lower() == user_input.lower()]
    if exact_matches:
        return exact_matches[0]
    else:
        matches = get_close_matches(user_input, patterns, n=1, cutoff=0.6)
        return matches[0] if matches else None

def get_response_for_tag(tag: str, knowledge_base: dict) -> str | None:
    for intent in knowledge_base["intents"]:
        if intent["tag"] == tag:
            return intent["responses"][0]  # Assuming only one response for simplicity

def chatbot():
    knowledge_base: dict = load_knowledge_base("intents.json")
    while True:
        user_input: str = input('you: ')

        if user_input.lower() == 'quit':
            break

        patterns = [pattern for intent in knowledge_base["intents"] for pattern in intent["patterns"]]
        best_match: str | None = find_best_match(user_input, patterns)

        if best_match:
            for intent in knowledge_base["intents"]:
                if best_match in intent["patterns"]:
                    response: str | None = get_response_for_tag(intent["tag"], knowledge_base)
                    if response:
                        print(f'bot: {response}')
                        break
            else:
                print('bot: Sorry, I do not have a response for that.')
        else:
            print('bot: Sorry, I do not understand. Can you teach me?')
            new_response: str = input('Type the response or "skip" to skip: ')

            if new_response.lower() != 'skip':
                tag: str = input('Enter the tag for this response: ')
                knowledge_base["intents"].append({
                    "tag": tag,
                    "patterns": [user_input],
                    "responses": [new_response]
                })
                save_knowledge_base("intents.json", knowledge_base)
                print('Friend: Thank you! I learned a new response!')

if __name__ == "__main__":
    chatbot()
