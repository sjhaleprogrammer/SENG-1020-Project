from LinkedList import LinkedList
import random
import json
import torch

from model import NeuralNet
from utils import bag_of_words, tokenize


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "training_data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

dictionary = LinkedList()
bot_name = "Librarian"


def main():
    
    print("Librarian: Hello and Welcome to the Dictionary Program, ask me anything.")
    print("")
    while True:
    
        sentence = input("User: ")
        print("")
        if sentence == "quit":
            break

        sentence = tokenize(sentence)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)

        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
        
                    if tag == "goodbye":
                        print(f"{bot_name}: {random.choice(intent['responses'])}")
                        exit()
                    elif tag == "add":
                        print(f"{bot_name}: {random.choice(intent['responses'])}")
                        word = input("Please enter word: ")
                        definition = input("Enter definition: ")
                        dictionary.add_word(word, definition)
                    elif tag == "delete":
                        print(f"{bot_name}: {random.choice(intent['responses'])}")
                        word = input("Enter word to delete: ")
                        dictionary.delete_word(word)
                    elif tag == "view":
                        if dictionary.isEmpty():
                            print("Librarian: Sure but your dictionary is empty.")
                        else:
                            print(f"{bot_name}: {random.choice(intent['responses'])}")
                            dictionary.display_words()
                    elif tag == "search":
                        print(f"{bot_name}: {random.choice(intent['responses'])}")
                        word = input("Enter word: ")
                        definition = dictionary.search_word(word)
                        if definition is not None:
                            print(word + ": " + definition)
                        else:
                            print("Word not found")

                    else:
                        print(f"{bot_name}: {random.choice(intent['responses'])}")
        
        else:
            print(f"{bot_name}: I do not understand, what did you say?")

        print("")

        
if __name__ == '__main__':
    main()






'''
def main():
    dictionary = LinkedList()
    while True:
        print("1. Add word")
        print("2. Search word")
        print("3. Display dictionary")
        print("4. Delete word")
        print("5. Quit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            word = input("Enter word: ")
            definition = input("Enter definition: ")
            dictionary.add_word(word, definition)
        elif choice == 2:
            word = input("Enter word: ")
            definition = dictionary.search_word(word)
            if definition is not None:
                print(word + ": " + definition)
            else:
                print("Word not found")
        elif choice == 3:
            dictionary.display_words()
        elif choice == 4:
            word = input("Enter word to delete: ")
            dictionary.delete_word(word)
        elif choice == 5:
            break
        else:
            print("Invalid choice")
'''

