from LinkedList import LinkedList


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


if __name__ == '__main__':
    main()
