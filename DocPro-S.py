#Rename variable names, I had a conflict that kept effecting view document which caused a crash

import os
from datetime import datetime
import csv
import shutil

#Custom import that stores my classes
import DocPro_Classes as DClass

#checks if this is the first time running the application/if the user has the DocPro-S repo already
def check_if_first():
    #creates file if it dosen't already exist
    file = open("user_path.txt", "a")
    file.close()

    file = open("user_path.txt", "r")
    read = file.read()
    if len(read) == 0:
        file.close()
        return False
    else:
        file.close()
        return read

def create_repos():
    path_repos = check_if_first()
    if path_repos == False:
        while True:
            print("Enter the pathway of the desired location to store your repository.")
            print("e.g. C:/Users/James/Documents\n")
            path_repos = input("Path: ")
            if os.path.exists(path_repos):
                try:
                    path_repos = os.path.join(path_repos, "DocPro-s")
                    write_user_path(path_repos)
                    create_file_manifesto(path_repos)
                    break
                except OSError as e:
                    print(f"Error, please check you have permissions to write to this directory... {path_repos}")
                    print(f"Error: {e}")
                break
            else:
                print(f"Invalid path, the following path dose not exist {path_repos}")
            

    os.makedirs(os.path.join(path_repos + "/File_Repository"), exist_ok=True)
    os.makedirs(os.path.join(path_repos + "/Backup_Repository"), exist_ok=True)
    os.makedirs(os.path.join(path_repos + "/Upload"), exist_ok=True)
    os.chdir(path_repos)
    return path_repos
    
def create_file_manifesto(path_repos):
    manifesto_path = os.path.join(path_repos, "File_Manifesto.csv")
    fieldnames = ["file_size", "filename", "path", "tags", "upload_date"]
    with open(manifesto_path, 'w') as manifesto:
        writer_object = csv.DictWriter(manifesto, fieldnames = fieldnames)
        writer_object.writeheader()

def add_tags():
    print("Please input the tags you would like to associate with this document, seperating each tag with a comma.")
    print("For example: Coding,VSCode,The Internet, would turn into --> coding | vscode | the internet")
    tags = input("Tags: ")
    split_tags = tags.split(",")
    return split_tags

#Implament the undo functionality for the manifesto 
def upload_to_file_manifesto(filename, path):
    fieldnames = ["file_size", "filename", "path", "tags", "upload_date"]
    row_to_add = {
        "file_size": os.path.getsize(path),
        "filename": filename,
        "path": path,
        "tags": add_tags(),
        "upload_date": datetime.now()
    }
    
    with open("File_Manifesto.csv", 'a') as manifesto:
        writer_object = csv.DictWriter(manifesto, fieldnames = fieldnames)
        writer_object.writerow(row_to_add)
        
def write_user_path(path):
    file = open("user_path.txt", "w")
    file.write(path)
    file.close()

def add_to_active_queue(file_name):
    pass

def read_document(file_name):
    document = open(file_name, 'r')
    text = document.read()
    document.close()
    return text

def add_to_repos(src_path, filename):
    src = src_path
    dst = os.path.join(os.getcwd(), "File_Repository", filename + ".txt")
    if os.path.exists(src):
        shutil.move(src, dst)
        upload_to_file_manifesto(filename, dst)
        return "add_to_repos", src, dst, filename
    else:
        print(f"This path dose not exist {src}")

def undo_add_to_repos(src, dst, filename):
    shutil.move(src, dst)
    return "add_to_repos", src, dst, filename


def user_read_document(path_to_doc):
    path_to_doc = os.path.join(os.getcwd(), "File_repository", path_to_doc)
    if os.path.exists(path_to_doc):
        file = open(path_to_doc, 'r')
        readable_file = file.read()
        word_count = word_counter(readable_file)
        if word_count > 200:
            list_of_words = readable_file.split()
        
            list_to_print = []
            for word in list_of_words:
                if len(list_to_print) == 200:
                    print(" ".join(list_to_print))
                    list_to_print = []
                    #Change later
                    voidVar = input("\nType any character to view next page\n")

                list_to_print.append(word)
        else: 
            print(readable_file)

        file.close()
    else:
        print(f"File dose not exist: {path_to_doc}")


def word_counter(string):
    word_count = len(string.split())
    return word_count

def create_document(name, string):
    path_create = os.path.join(os.getcwd(), "File_repository", name + ".txt")
    if os.path.exists(path_create):
        print(f"A document with the same name already exists: {path_create}")
        return 
    with open (path_create, 'w') as file_to_write:
        file_to_write.write(string)
    return "create", path_create, name

def delete_document(filename):
        dst = os.path.join(os.getcwd(), "Backup_repository", filename + ".txt")
        src = os.path.join(os.getcwd(), "File_repository", filename + ".txt")
        if os.path.exists(src):
            shutil.move(src, dst)
            return "del", src, dst, filename
        else:
            print(f"This document dose not exist {src}")
            return 

def dupblicate_document(filename, new_filename):
    path_dub = os.path.join(os.getcwd(), "File_repository", filename + ".txt")
    if os.path.exists(path_dub):
        document = open(path_dub, 'r')
        document_contents = document.read()
        document.close()
    else:
        print(f"This document dose not exist {path_dub}")
        return None

    path_dub = os.path.join(os.getcwd(), "File_repository", new_filename + ".txt")
    if os.path.exists(path_dub):
        print(f"A document with the name already exists {path_dub}")
        return None
    else:
        with open(path_dub, 'w') as dub_file:
            dub_file.write(document_contents)

        return "dub", path_dub, new_filename

def rename_document(filename, new_filename):
    src = os.path.join("File_repository", filename + ".txt")
    dst = os.path.join("File_repository", new_filename + ".txt")
    
    if os.path.exists(src):
        pass
    else:
        print(f"This path dose not exist: {src}")
        return None
    
    if os.path.exists(dst):
        print(f"A file with this name already exists: {dst}")
        return None
        
    os.rename(src, dst)
    return "rename", filename, new_filename

#temp function until manifesto is created
def view_documents(path_view):
    print(os.listdir(os.path.join(path_view, "File_repository")))


#main 
welcome_message = "Welcome to DocPro-s"
print(welcome_message)
print("-" * len(welcome_message) + "\n")

path = create_repos()
undo = DClass.Undo_Redo()
redo = DClass.Undo_Redo()

running = True
while running == True:
    current_files_string = "Current Files:"
    print(current_files_string + "\n" + ("-" * len(current_files_string)))
    view_documents(path)
    
    print("Add document(1), Remove document (2), Dupblicate_document(3), Create document (4), View Document (5), Rename Document (6), Undo (7), Redo (8) Exit program (e)")
    user_input = input("Control: ")

    if user_input == "1":
        src_path = input("Enter path: ")
        filename = input("Filename: ")
        results = add_to_repos(src_path, filename)
        if results == None:
            pass
        else:
            act, prev_path, new_path, filename = results
            undo.push(act = act, prev_path = prev_path, path = new_path, filename = filename)
    
    elif user_input == "2":
        filename = input("Filename: ")
        results = delete_document(filename)
        if results == None:
            pass
        else:
            act, prev_path, new_path, filename = results
            undo.push(act = act, prev_path = prev_path, path = new_path, filename = filename)

    elif user_input == "3":
        filename = input("Filename: ")
        new_filename = input("New_filename: ")
        results = dupblicate_document(filename, new_filename)
        if results == None:
            pass
        else:
            act, new_path, filename = results
            undo.push(act = act, path = new_path, filename = filename)
        
    elif user_input == "4":
        name = input("Name: ")
        string = input("String: ")
        results = create_document(name, string)
        if results == None:
            pass
        else:
            act, new_path, filename = results
            undo.push(act = act, path = new_path, filename = filename)
        
    elif user_input == "5":
        filename = input("filename: ") + ".txt" 
        user_read_document(filename)

    elif user_input == "6":
        filename = input("Filename: ")
        new_filename = input("New_Filename: ")
        results = rename_document(filename, new_filename)
        if results == None:
            pass
        else:
            act, prev_name, new_name = results
            undo.push(act = act, prev_name = prev_name, filename = new_name)

    elif user_input == "7":
        if undo.peek() == None:
            print("Nothing to undo")
            continue
        attributes = undo.peek().get_attributes()

        if attributes["action"] == "create":
            act, prev_path, new_path, filename = delete_document(attributes["filename"])
            undo.pop()
            redo.push(act = act, path = new_path, prev_path = prev_path, filename = filename)

        elif attributes["action"] == "del":
            act, prev_path, new_path, filename = add_to_repos(attributes["path"], attributes["filename"])
            undo.pop()
            redo.push(act = act, prev_path = prev_path, path = new_path, filename = filename)

        elif attributes["action"] == "dub":
            act, prev_path, new_path, filename = delete_document(attributes["filename"])
            undo.pop()
            redo.push(act = act, path = new_path, prev_path = prev_path, filename = filename)

        elif attributes["action"] == "rename":
            act, prev_name, new_name = rename_document(attributes["filename"], attributes["prev_name"])
            undo.pop()
            redo.push(act = act, prev_name = prev_name, filename = new_name)

        elif attributes["action"] == "add_to_repos":
            act, prev_path, new_path, filename = undo_add_to_repos(attributes["path"], attributes["prev_path"], attributes["filename"])
            undo.pop()
            redo.push(act = act, prev_path = prev_path, path = new_path, filename = filename)

    elif user_input == "8":
        if redo.peek() == None:
            print("Nothing to redo")
            continue
        attributes = redo.peek().get_attributes()

        if attributes["action"] == "create":
            act, prev_path, new_path, filename = delete_document(attributes["filename"])
            redo.pop()
            undo.push(act = act, path = new_path, prev_path = prev_path, filename = filename)

        elif attributes["action"] == "del":
            act, prev_path, new_path, filename = add_to_repos(attributes["path"], attributes["filename"])
            redo.pop()
            undo.push(act = act, prev_path = prev_path, path = new_path, filename = filename)

        elif attributes["action"] == "dub":
            act, prev_path, new_path, filename = delete_document(attributes["filename"])
            redo.pop()
            undo.push(act = act, path = new_path, prev_path = prev_path, filename = filename)

        elif attributes["action"] == "rename":
            act, prev_name, new_name = rename_document(attributes["filename"], attributes["prev_name"])
            redo.pop()
            undo.push(act = act, prev_name = prev_name, filename = new_name)

        elif attributes["action"] == "add_to_repos":
            act, prev_path, new_path, filename = undo_add_to_repos(attributes["path"], attributes["prev_path"], attributes["filename"])
            redo.pop()
            undo.push(act = act, prev_path = prev_path, path = new_path, filename = filename)

    elif user_input.lower() == "e":
        running = False

    else:
        print("Input ERROR!!! Invalid Input")





