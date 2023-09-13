class Node:
    def __init__(self, elem):
        self.data = elem
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def append(self, elem):
        if self.head:
            # inserção quando já houver elementos
            pointer = self.head
            while pointer.next:
                pointer = pointer.next
            pointer.next = Node(elem)
        else:
            # primeira inserção
            self.head = Node(elem)

        self._size += 1

    def __len__(self):
        return self._size

    def __getitem__(self, index):
        pointer = self.head

        if index < 0:
            index = self._size - abs(index)

        for i in range(index):
            if pointer:
                pointer = pointer.next
            else:
                raise IndexError("list index out of range")

        if pointer:
            return pointer.data

        raise IndexError("list index out of range")

    def __setitem__(self, index, elem):
        pointer = self.head
        for i in range(index):
            if pointer:
                pointer = pointer.next
            else:
                raise IndexError("list index out of range")

        if pointer:
            pointer.data = elem
        else:
            raise IndexError("list index out of range")

    def index(self, elem):
        pointer = self.head
        index = 0
        while pointer:
            if pointer.data == elem:
                return index
            pointer = pointer.next
            index += 1
        raise ValueError(f"{elem} was not found in the list")






