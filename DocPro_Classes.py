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

class Undo_Redo_Node:

    def __init__(self, act = None, filename = None, path = None, prev_name = None, prev_path = None, prev_node = None, next_node = None):
        self.act = act
        self.filename = filename
        self.path = path
        self.prev_name = prev_name
        self.prev_path = prev_path
        self.prev_node = prev_node
        self.next_node = next_node

    def get_attributes(self):
        return {
            "action": self.act,
            "filename": self.filename,
            "path": self.path,
            "prev_name": self.prev_name,
            "prev_path": self.prev_path
        }

    def set_prev_node(self, prev_node):
        self.prev_node = prev_node

    def get_prev_node(self):
        return self.prev_node
    
class Undo_Redo:
    
    def __init__(self, type = 1):
        self.top_item = None

    def peek(self):
        return self.top_item
          
    def pop(self):
        if self.top_item is not None:
            node_to_remove = self.top_item
            self.top_item = self.top_item.get_prev_node()
            return node_to_remove
        return None

    def push(self, act = None, filename = None, path = None, prev_name = None, prev_path = None):
        node = Undo_Redo_Node(act, filename, path, prev_name, prev_path)
        if self.top_item is not None:
            node.set_prev_node(self.top_item)
        self.top_item = node
            



