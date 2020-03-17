"""Each ListNode holds a reference to its previous node
as well as its next node in the List."""

from functools import reduce


class ListNode:
    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next

    def __str__(self):
        return f"{self.value}"

    def insert_after(self, value):
        """Wrap the given value in a ListNode and insert it
        after this node. Note that this node could already
        have a next node it is point to."""
        current_next = self.next
        self.next = ListNode(value, self, current_next)
        if current_next:
            current_next.prev = self.next

    def insert_before(self, value):
        """Wrap the given value in a ListNode and insert it
        before this node. Note that this node could already
        have a previous node it is point to."""
        current_prev = self.prev
        self.prev = ListNode(value, current_prev, self)
        if current_prev:
            current_prev.next = self.prev

    def delete(self):
        """Rearranges this ListNode's previous and next pointers
        accordingly, effectively deleting this ListNode."""
        if self.prev:
            self.prev.next = self.next
        if self.next:
            self.next.prev = self.prev



class DoublyLinkedList:
    """Our doubly-linked list class. It holds references to
    the list's head and tail nodes."""
    def __init__(self, node=None):
        self.head = node
        self.tail = node
        self.length = 1 if node is not None else 0

    def __len__(self):
        return self.length

    def __str__(self):
        start = "#["
        middle = ""
        end = "]"
        current_node = self.head

        if current_node is None:
            return f"{start}{middle}{end}"

        while current_node is not None:
            trail = " (<->) " if current_node.next is not None else ""
            middle += f"{current_node}{trail}"
            current_node = current_node.next

        return f"{start} {middle} {end}"

    def add_to_head(self, value):
        """Wraps the given value in a ListNode and inserts it
        as the new head of the list. Don't forget to handle
        the old head node's previous pointer accordingly."""
        self.length += 1

        prev = self.head
        new_node = ListNode(value, None, prev)
        self.head = new_node
        if prev is not None:
            prev.prev = self.head
        else:
            self.tail = new_node


    def remove_from_head(self):
        """Removes the List's current head node, making the
        current head's next node the new head of the List.
        Returns the value of the removed Node."""
        if self.length == 0:
            return None

        prev_head = self.head

        self.length -= 1

        if prev_head.next is None:
            self.head = None
            self.tail = None
        else:
            new_head = prev_head.next
            new_head.prev = None
            self.head = new_head

        return prev_head.value

    def add_to_tail(self, value):
        """Wraps the given value in a ListNode and inserts it
        as the new tail of the list. Don't forget to handle
        the old tail node's next pointer accordingly."""
        self.length += 1

        prev_tail = self.tail
        new_node = ListNode(value, prev_tail, None)
        self.tail = new_node

        if self.head is None:
            self.head = new_node

        if prev_tail is not None:
            prev_tail.next = new_node

    def remove_from_tail(self):
        """Removes the List's current tail node, making the
        current tail's previous node the new tail of the List.
        Returns the value of the removed Node."""
        if self.length == 0:
            return None

        prev_tail = self.tail

        self.length -= 1

        if prev_tail.prev is None:
            self.head = None
            self.tail = None
        else:
            new_tail = prev_tail.prev
            new_tail.next = None
            self.tail = new_tail

        return prev_tail.value

    def find_node(self, node):
        """ Finds the node that matches the one passed in. If no node matches it
        returns None. """

        should_continue = True
        found_node = None

        if self.length == 0:
            should_continue = False
        elif self.length == 1 and self.head == node:
            should_continue = False
            found_node = self.head

        current_node = self.head

        while should_continue:
            if current_node == node:
                should_continue = False
                found_node = current_node

            if current_node.next is None:
                should_continue = False

            if current_node.next is not None:
                current_node = current_node.next

        return found_node

    def traverse(self, cb):
        current_node = self.head

        while current_node is not None:
            cb(current_node)

            current_node = current_node.next

    def move_to_front(self, node):
        """Removes the input node from its current spot in the
        List and inserts it as the new head node of the List."""

        if node == self.head:
            return

        found_node = self.find_node(node)

        prev_node, next_node = (found_node.prev, found_node.next)

        if self.length == 2:
            prev_tail = self.tail
            prev_head = self.head

            self.tail = prev_head
            self.tail.next = None
            self.tail.prev = prev_tail

            self.head = prev_tail
            self.head.prev = None
            self.head.next = prev_head

            return

        if found_node == self.tail:
            self.tail = prev_node
            self.tail.next = None
            self.tail.prev = prev_node.prev
        elif next_node is not None:
            next_node.prev = prev_node

        prev_head = self.head

        self.head = found_node
        self.head.prev = None
        self.head.next = prev_head
        prev_head.prev = self.head

        if prev_node is not None:
            prev_node.next = next_node

    def move_to_end(self, node):
        """Removes the input node from its current spot in the
        List and inserts it as the new tail node of the List."""

        found_node = self.find_node(node)
        if found_node == self.tail:
            return

        prev_node, next_node = (found_node.prev, found_node.next)

        if self.length == 2:
            prev_tail = self.tail
            prev_head = self.head

            self.tail = prev_head
            self.tail.next = None
            self.tail.prev = prev_tail

            self.head = prev_tail
            self.head.prev = None
            self.head.next = prev_head

            return

        if found_node == self.head:
            self.head = next_node
            self.head.prev = None
            self.head.next = next_node.next
        elif next_node is not None:
            next_node.prev = prev_node

        prev_tail = self.tail

        self.tail = found_node
        self.tail.next = None
        self.tail.prev = prev_tail
        prev_tail.next = self.tail

        if prev_node is not None:
            prev_node.next = next_node


    def delete(self, node):
        """Removes a node from the list and handles cases where
        the node was the head or the tail"""

        self.length -= 1

        if self.length == 0:
            self.head = None
            self.tail = None
            return

        if node == self.head:
            self.head = node.next
            self.head.prev = None
            return
        if node == self.tail:
            self.tail = node.prev
            self.tail.next = None
            return

        found_node = self.find_node(node)
        prev_node, next_node = (found_node.prev, found_node.next)

        if prev_node is not None:
            prev_node.next = next_node
        if next_node is not None:
            next_node.next = prev_node

    def get_max(self):
        """Returns the highest value currently in the list"""
        dll_max = self.head
        current_node = self.head

        while current_node is not None:
            if current_node.value > dll_max.value:
                dll_max = current_node
            current_node = current_node.next

        return dll_max.value
