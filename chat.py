import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as f:
    intents = json.load(f)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()



bot_name = "Friday"


def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    
    return "I'm not sure how to respond to that. Could you please rephrase?"
    words = tokenize(msg)
    response = "Hi, I'm Friday. How can I assist you?"

    # Check for exact matches in patterns
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            if msg.lower() == pattern.lower():
                response = random.choice(intent['responses'])
                return response

    # Check for partial matches in patterns
    for intent in intents["intents"]:
        if any(msg.lower() in pattern.lower() for pattern in intent["patterns"]):
            response = random.choice(intent['responses'])
            return response

    # Check for keyword matches in patterns
    for intent in intents["intents"]:
        for keyword in intent.get("keywords", []):
            if keyword.lower() in msg.lower():
                for pattern in intent["patterns"]:
                    if keyword.lower() in pattern.lower():
                        response = random.choice(intent['responses'])
                        return response

    return response