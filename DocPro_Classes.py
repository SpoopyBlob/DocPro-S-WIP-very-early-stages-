class Document_Node:
    
    def __init__(self, name = None, tags = None, upload_date = None, created_date = None, value = None, next_node = None, prev_node = None):
        #Metadata
        self.name = name
        self.tags = tags
        self.upload_date = upload_date
        self.created_date = created_date
        #Node Prop
        self.value = value
        self.next_node = next_node
        self.prev_node = prev_node

    #Node methods
    def get_value(self):
        return self.value
    
    def get_next_node(self):
        return self.next_node
    
    def get_prev_node(self):
        return self.prev_node
    
    def set_next_node(self, next_node):
        self.next_node = next_node

    def set_prev_node(self, prev_node):
        self.prev_node = prev_node

class Action_node:
    def __init__(self, action = None):
        self.action = action
        self.prev_action = None
        self.next_action = None

    def current_action(self):
        return self.action
    
    def get_next_action(self):
        return self.next_action
    
    def get_prev_action(self):
        return self.prev_action
    
    def set_next_action(self, next_action):
        self.next_action = next_action

    def set_prev_action(self, prev_action):
        self.prev_action = prev_action

class Search_results():

    def __init__(self):
        self.head_node = None
        self.tail_node = None

    #get & set methods
    def get_head_node(self):
        return self.head_node
    
    def get_tail_node(self):
        return self.tail_node
    
    def set_head_node(self, new_head):
        self.head_node = new_head

    def set_tail_node(self, new_tail):
        self.tail_node = new_tail

class Activity_Queue():
    max_size = 4

    def __init__(self, head = None, tail = None):
        self.head = head
        self.tail = tail
        self.size = 0

    def peek(self):
        if self.is_empty() == False:
            return self.head.get_value()
        print("No documents in the activity queue")
    
    def get_size(self):
        return self.size
    
    def is_empty(self):
        if self.get_size() == 0:
            return True
        return False
    
    def enqueue(self, document_node):
        item = document_node

        if self.is_empty() == True:
            self.head = item
            self.tail = item
        else:
            self.tail.set_next_node(item)
            self.tail = item
        self.size += 1

        if self.size > self.max_size:
            self.dequeue()

    def dequeue(self):
        if self.is_empty() == False:
            head_to_remove = self.head
            self.head = head_to_remove.get_next_node()
            self.size -= 1

class Undo_Redo:
    
    def __init__(self):
        self.top_item = None

    def peek(self):
        return self.top_item.current_action()
        
    def undo(self):
        item_to_remove = self.top_item
        self.top_item = item_to_remove

    def action(self, act):
        node = Action_node(action = act)
        self.top_item = node