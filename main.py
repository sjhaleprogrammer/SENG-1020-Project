from LinkedList import LinkedList
from model import NeuralNet
from nltk.stem.porter import PorterStemmer


import numpy as np
import random
import json
import torch
import tkinter as tk
import nltk


stemmer = PorterStemmer()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "training_data.pth"
data = torch.load(FILE)

model = NeuralNet(data["input_size"], data["hidden_size"], data["output_size"]).to(device)
model.load_state_dict(data["model_state"])
model.eval()

dictionary = LinkedList()
bot_name = "Librarian"

# Create a dictionary to cache the model's output for frequently asked questions
model_output_cache = {}

def get_model_output(X):
    # Check if the output for this input is already in the cache
    if str(X) in model_output_cache:
        return model_output_cache[str(X)]

    # Otherwise, run the model and cache the output
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = data['tags'][predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    output_data = (tag, prob)
    model_output_cache[str(X)] = output_data
    return output_data

def main():
    window = tk.Tk()
    window.resizable(False, False)
    window.geometry("800x600")
    window.title("VocabAI")
    window.config(bg="#263238")
    
    chat_label = tk.Label(window, text="VocabAI", bg="#263238", fg="#FFF", font=("Arial", 16))
    chat_label.pack(pady=5)
    
    chatbox = tk.Listbox(window, height=20, width=120, bg="#263238", fg="#FFF", font=("Arial", 12))
    chatbox.pack(padx=10, pady=10)

    greeting = "Librarian: Hello welcome to the dictionary program, ask me to add new words, search for them, or view them.\n"
    chatbox.insert(tk.END, greeting)
    
    
    

    
    def send_message():
        message = message_entry.get()
        message_entry.delete(0, tk.END)

        if message == "quit":
            window.quit()

        chatbox.insert(tk.END, f"You: {message}")

        sentence = nltk.word_tokenize(message)

        sentence_words = [stemmer.stem(word.lower()) for word in sentence]
        # initialize bag with 0 for each word
        X = np.zeros(len(data['all_words']), dtype=np.float32)
        for idx, w in enumerate(data['all_words']):
            if w in sentence_words: 
                X[idx] = 1

        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        tag, prob = get_model_output(X)

        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:

                    response = f"{bot_name}: {random.choice(intent['responses'])}"

                    if tag == "goodbye":
                        chatbox.insert(tk.END, response)
                        window.quit()
                    elif tag == "add":
                        chatbox.insert(tk.END, response)
                        add_word_window = tk.Toplevel(window)
                        add_word_window.geometry("400x200")
                        add_word_window.title("Add Word")
                        add_word_window.config(bg="#263238")
                        add_word_window.resizable(False, False)

                        # Bring the window to the top
                        add_word_window.lift()

                        word_label = tk.Label(add_word_window, bg="#263238", fg="#FFF", text="Word", font=("Arial", 12))
                        word_label.pack(pady=5)

                        word_entry = tk.Entry(add_word_window, width=30, font=("Arial", 12))
                        word_entry.pack(pady=5)

                        definition_label = tk.Label(add_word_window, bg="#263238", fg="#FFF", text="Definition", font=("Arial", 12))
                        definition_label.pack(pady=5)

                        definition_entry = tk.Entry(add_word_window, width=30, font=("Arial", 12))
                        definition_entry.pack(pady=5)

                        def add_word():
                            word = word_entry.get()
                            definition = definition_entry.get()
                            dictionary.add_word(word, definition)
                            chatbox.insert(tk.END, f"Added word '{word}' with definition '{definition}' to dictionary.")
                            add_word_window.destroy()

                        add_button = tk.Button(add_word_window, text="Add", width=10, font=("Arial", 12), command=add_word)
                        add_button.pack(pady=5)

                    elif tag == "delete":   
                        # create a new window for the delete functionality
                        delete_window = tk.Toplevel(window)
                        delete_window.title("Delete Word")
                        delete_window.config(bg="#263238")
                        delete_window.resizable(False, False)

                        # Bring the window to the top
                        delete_window.lift()

                        # create a label and an entry box for the user to enter the word to delete
                        search_label = tk.Label(delete_window, bg="#263238", fg="#FFF", text="Enter word to delete:", font=("Arial", 12))
                        search_label.pack(pady=10)
                        search_entry = tk.Entry(delete_window, width=30, font=("Arial", 14))
                        search_entry.pack(pady=10)

                        # define the function to delete the word from the dictionary
                        def delete_word():
                            # get the search term and delete the word from the dictionary
                            word = search_entry.get()
                            success = dictionary.delete_word(word)

                            # display a message indicating whether the word was successfully deleted or not
                            if success:
                                message = f"{bot_name}: '{word}' has been deleted from the dictionary.\n"
                            else:
                                message = f"{bot_name}: '{word}' was not found in the dictionary.\n"

                            # display the message in the chatbox
                            chatbox.insert(tk.END, message)

                            # close the delete window
                            delete_window.destroy()

                        # create a button to delete the word
                        delete_button = tk.Button(delete_window, text="Delete", font=("Arial", 14), command=delete_word)
                        delete_button.pack(pady=10)
                                            

                    elif tag == "view":
                        if dictionary.isEmpty():
                            chatbox.insert(tk.END, "Librarian: Your dictionary is currently empty.")
                        else:
                            message = f"{bot_name}: {random.choice(intent['responses'])}\n"
                            chatbox.insert(tk.END, dictionary.display_words())

                    elif tag == "search":
                        # create a new window for search
                        search_window = tk.Toplevel(window)
                        search_window.title("Search")
                        search_window.config(bg="#263238")
                        search_window.resizable(False, False)

                        # Bring the window to the top
                        search_window.lift()

                        # create a label and entry for the search term
                        search_label = tk.Label(search_window, bg="#263238", fg="#FFF", text="Enter word", font=("Arial", 12))
                        search_label.pack(pady=10)
                        search_entry = tk.Entry(search_window, width=30, font=("Arial", 14))
                        search_entry.pack(pady=10)

                        def search():
                            # get the search term and search for the word in the dictionary
                            word = search_entry.get()
                            definition = dictionary.search_word(word)

                            # display the search result in the main chat window
                            if definition is not None:
                                chatbox.insert(tk.END, f"{bot_name}: I found the word you searched for: {word}: {definition}\n")
                            else:
                                chatbox.insert(tk.END, f"{bot_name}: Word not found\n")

                            # close the search window
                            search_window.destroy()

                        # create a search button
                        search_button = tk.Button(search_window, text="Search", font=("Arial", 14), command=search)
                        search_button.pack(pady=10)
                    else:
                        chatbox.insert(tk.END, response)
        else:
            chatbox.insert(tk.END, f"{bot_name}: I do not understand, what did you say?")


    button_img = tk.PhotoImage(file="button_image.png")
    button_img = button_img.subsample(6, 6)  # resize the image to half its original size

    message_frame = tk.Frame(window)
    message_frame.pack(padx=10, pady=5, fill="x")

    message_entry = tk.Entry(message_frame, width=50, bg="#FFF", fg="#263238", font=("Arial", 18))
    message_entry.bind("<Return>", lambda event: send_message())
    message_entry.pack(side="left", expand=True, fill="x")

    button = tk.Button(message_frame, image=button_img, bd=0, command=send_message, height=30, width=30)
    button.pack(side="right")


    window.mainloop()

        



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

