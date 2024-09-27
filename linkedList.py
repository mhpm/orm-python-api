class Node:
    def __init__(self, element):
        self.element = element
        self.next = None


class LinkList:
    def __init__(self):
        self.head = None
        self.count = 0

    def push(self, element):
        node = Node(element)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = node
        self.count += 1

    def get_list(self):
        current = self.head
        while current is not None:
            print(current.element, end=" ")
            current = current.next
        print()

    def no_repeated_elements(self):
        current = self.head
        while current is not None:
            runner = current
            while runner.next is not None:
                if runner.next.element == current.element:
                    # Remove duplicate node
                    runner.next = runner.next.next
                    self.count -= 1
                else:
                    runner = runner.next
            current = current.next


# Create a linked list and add elements
list = LinkList()
list.push(1)
list.push(2)
list.push(1)
list.push(3)

print("Original list:")
list.get_list()

# Remove duplicates
list.no_repeated_elements()

print("List after removing duplicates:")
list.get_list()
