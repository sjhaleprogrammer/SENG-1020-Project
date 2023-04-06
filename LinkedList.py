from Node import Node


class LinkedList:
    def __init__(self):
        self.head = None

    def add_word(self, word, definition):
        new_node = Node(word, definition)
        if self.head is None:
            self.head = new_node
        else:
            current_node = self.head
            while current_node.next is not None:
                current_node = current_node.next
            current_node.next = new_node

    def search_word(self, word):
        current_node = self.head
        while current_node is not None:
            if current_node.word == word:
                return current_node.definition
            current_node = current_node.next
        return None

    def display_words(self):
        current_node = self.head
        while current_node is not None:
            print(current_node.word + ": " + current_node.definition)
            current_node = current_node.next

    def delete_word(self, word):
        if self.head is None:
            return
        if self.head.word == word:
            self.head = self.head.next
            return
        current_node = self.head
        while current_node.next is not None:
            if current_node.next.word == word:
                current_node.next = current_node.next.next
                return
            current_node = current_node.next

    def isEmpty(self):
        return self.head is None
