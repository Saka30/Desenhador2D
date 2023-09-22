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

    def _getnode(self, index):
        pointer = self.head
        for i in range(index):
            if pointer:
                pointer = pointer.next
            else:
                raise IndexError("list index out of range")  # return None
        return pointer

    def __getitem__(self, index):
        pointer = self._getnode(index)
        if pointer:
            return pointer.data
        else:
            raise IndexError("list index out of range")

    def __setitem__(self, index, elem):
        pointer = self._getnode(index)

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

    def insert(self, index, elem):
        node = Node(elem)
        if index == 0:
            node.next = self.head
            self.head = node
        else:
            pointer = self._getnode(index - 1)
            node.next = pointer.next
            pointer.next = node
        self._size = self._size + 1

    def remove(self, elem):
        if self.head is None:
            raise ValueError(f"{elem} is not in list")
        elif self.head.data == elem:
            self.head = self.head.next
            self._size = self._size - 1
            return True
        else:
            ancestor = self.head
            pointer = self.head.next
            while pointer:
                if pointer.data == elem:
                    ancestor.next = pointer.next
                    pointer.next = None
                    self._size = self._size - 1
                    return True
                ancestor = pointer
                pointer = pointer.next
        raise ValueError(f"{elem} is not in list")

    def pop(self):
        if self.head is None:
            raise IndexError("pop from empty list")

        self._size -= 1
        # se tiver apenas um elemento
        if self.head.next is None:
            removed_data = self.head.data
            self.head = None
            return removed_data

        current = self.head
        while current.next.next is not None:
            current = current.next

        removed_data = current.next.data
        current.next = None
        return removed_data

    def is_empty(self):
        if self.head is None:
            return True

        return False

    def __repr__(self):
        r = ""
        pointer = self.head
        while pointer:
            r = r + str(pointer.data) + "->"
            pointer = pointer.next
        return r

    def __str__(self):
        return self.__repr__()

    def limpa(self):
        self.head = None

