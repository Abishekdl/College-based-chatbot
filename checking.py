import json
from nltk_utils import tokenize, stem, bag_of_words
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet

# Load intents data from JSON file with error handling
try:
    with open('intents.json', 'r') as f:
        intents = json.load(f)
except Exception as e:
    print(f'Error loading intents data: {e}')
    intents = None

# Preprocess data if intents data is loaded successfully
if intents:
    all_words = []
    tags = []
    xy = []
    for intent in intents['intents']:
        tag = intent['tag']
        tags.append(tag)
        for pattern in intent['patterns']:
            w = tokenize(pattern)
            all_words.extend(w)
            xy.append((w, tag))

    ignore_words = ['?', '!', '.', ',']
    all_words = [stem(w) for w in all_words if w not in ignore_words]
    all_words = sorted(set(all_words))
    tags = sorted(set(tags))

    X_train = []
    Y_train = []
    for (pattern_sentence, tag) in xy:
        bag = bag_of_words(pattern_sentence, all_words)
        X_train.append(bag)

        label = tags.index(tag)
        Y_train.append(label)

    X_train = np.array(X_train)
    Y_train = np.array(Y_train)

    # Rest of your code for creating DataLoader, defining model, training, etc.
    # ...

    print('Intents data loaded and preprocessed successfully.')
else:
    print('Intents data could not be loaded. Exiting program.')
