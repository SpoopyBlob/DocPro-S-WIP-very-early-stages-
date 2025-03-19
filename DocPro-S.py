#tackle tags issue, find a better way to implament tags that is more user friendly
#Implament the manifesto in every user control function
#Implament a search feature

import os
from datetime import datetime
import csv
import shutil
import uuid

#Custom import that stores my classes
import DocPro_Classes as DClass

#Functions used to create the enviroment
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
    fieldnames = ["id", "file_size", "filename", "path", "tags", "upload_date", "status"]
    with open(manifesto_path, 'w') as manifesto:
        writer_object = csv.DictWriter(manifesto, fieldnames = fieldnames)
        writer_object.writeheader()

def write_user_path(path):
    file = open("user_path.txt", "w")
    file.write(path)
    file.close()

#Functions related to the File Manifesto (excluding the creation of file manifesto)
def get_metadate(filename, mode):

    with open("File_manifesto.csv", "r") as manifesto:
        read_object = csv.DictReader(manifesto)

        for rows in read_object:
            if mode == "upload_date":
                if rows["filename"] == filename:
                    return rows["upload_date"]
            elif mode == "tags":
                if rows["filename"] == filename:
                    return rows["tags"]
 
def upload_to_file_manifesto(filename, path, upload_date = None, tags = None):
    fieldnames = ["id", "file_size", "filename", "path", "tags", "upload_date", "status"]
    id_num = uuid.uuid4()
    id_num_string = str(id_num)
    
    
    if upload_date == None:
        upload_datet = datetime.now()

    if tags == None:
        tags = add_tags()
    

    row_to_add = {
        "id": id_num_string,
        "file_size": os.path.getsize(path),
        "filename": filename,
        "path": path,
        "tags": tags,
        "upload_date": upload_date,
        "status": True
    }
    
    with open("File_Manifesto.csv", "a") as manifesto:
        writer_object = csv.DictWriter(manifesto, fieldnames = fieldnames)
        writer_object.writerow(row_to_add)

def store_by_upload_date(date_from_manifest = None):
    if date_from_manifest == None:
        date = datetime.now()
    else:
        date = date_from_manifest.strftime('%Y-%m-%d %H:%M:%S')
    sub_folder = date.strftime("%m %Y")
    path = os.path.join(os.getcwd(), "File_Repository", sub_folder)
    os.makedirs(path, exist_ok = True)
    return path



    shutil.move(src, dst)
    return "undo_add_to_repos", src, dst, filename

def return_path_from_manifesto(filename):
    with open(os.path.join(os.getcwd(), "File_Manifesto.csv"), "r") as manifesto:
        reader_object = csv.DictReader(manifesto)
        for rows in reader_object:
            if rows["filename"] == filename:
                return rows["path"]
        print("Doc not found...")
        return None

def update_manifesto(filename, mode = None, change = None):
    csv_contents = []
    with open(os.path.join(os.getcwd(), "File_Manifesto.csv"), "r") as manifesto:
        reader_object = csv.DictReader(manifesto)
        csv_contents = []
        for rows in reader_object:
            if mode == "perm_delete" and rows["status"] == "False":
                    continue
            if rows["filename"] == filename:
                if mode == "rename":
                    rows["filename"] = change.get("filename", rows["filename"])
                    rows["path"] = change.get("path", rows["path"])
                elif mode == "delete":
                    rows["status"] = False
                    rows["path"] = change.get("path", rows["path"])
                elif mode == "tags":
                    rows["tags"] = change.get("tags", rows["tags"])
                elif mode == "undo_del":
                    rows["path"] = change.get("path", rows["path"])
                    rows["status"] = True

            csv_contents.append(rows)

    with open(os.path.join(os.getcwd(), "File_Manifesto.csv"), "w") as write_manifesto:
        fieldnames = ["id", "file_size", "filename", "path", "tags", "upload_date", "status"]
        writer_object = csv.DictWriter(write_manifesto, fieldnames = fieldnames)
        writer_object.writeheader()
        
        for dict in csv_contents:
            writer_object.writerow(dict)

#User control functions (includes undo functions)
def view_documents(path_view):

    with open(os.path.join(os.getcwd(), "File_Manifesto.csv"), "r") as docs:
        reader_object = csv.DictReader(docs)
        filenames = []
        for rows in reader_object:
            if rows["status"] == "False":
                continue
    
            filenames.append(rows["filename"])

        print(filenames)

def user_read_document(filename):
    path_to_doc = return_path_from_manifesto(filename)
    if path_to_doc == None:
        print("Filename dose not exist.")
        return

    
    if os.path.exists(path_to_doc):
        with open(path_to_doc, 'r') as doc:
            readable_file = doc.read()
        
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
                voidVar = input("\n Type any character to return to the home page")
            doc.close()
    else:
        print(f"File dose not exist: {path_to_doc}")

def read_document(file_name):
    document = open(file_name, 'r')
    text = document.read()
    document.close()
    return text

def dupblicate_document(filename, new_filename):
    path_dub = return_path_from_manifesto(filename)
    if os.path.exists(path_dub):
        document = open(path_dub, 'r')
        document_contents = document.read()
        document.close()
    else:
        print(f"This document dose not exist {path_dub}")
        return None

    path_dub = os.path.join(path_dub[:-(len(filename) + 4)], new_filename + ".txt")
    if os.path.exists(path_dub):
        print(f"A document with the name already exists {path_dub}")
        return None
    else:
        with open(path_dub, 'w') as dub_file:
            dub_file.write(document_contents)
        
        upload_date = get_metadate(filename, "upload_date")
        tags = get_metadate(filename, "tags")
        upload_to_file_manifesto(new_filename, path_dub, upload_date = upload_date, tags = tags)

        return "dub", path_dub, new_filename

def rename_document(filename, new_filename):
    src = return_path_from_manifesto(filename)
    dst = os.path.join(src[:-(len(filename) + 4)], new_filename + ".txt")
    
    if os.path.exists(src):
        pass
    else:
        print(f"This path dose not exist: {src}")
        return None
    
    if os.path.exists(dst):
        print(f"A file with this name already exists: {dst}")
        return None
        
    update_manifesto(filename, mode = "rename", change = {"filename": new_filename, "path": dst})
    os.rename(src, dst)

    return "rename", filename, new_filename

def create_document(name, string):
    path_create = os.path.join(store_by_upload_date(), name + ".txt")
    if os.path.exists(path_create):
        print(f"A document with the same name already exists: {path_create}")
        return 
    
    with open (path_create, 'w') as file_to_write:
        file_to_write.write(string)

    upload_to_file_manifesto(name, path_create)

    return "create", path_create, name

def delete_document(filename):
        dst = os.path.join(os.getcwd(), "Backup_repository", filename + ".txt")
        src = return_path_from_manifesto(filename)
        if os.path.exists(src):
            update_manifesto(filename, mode = "delete", change = {"path": dst})
            shutil.move(src, dst)
            return "del", src, dst, filename
        else:
            print(f"This document dose not exist {src}")
            return 

def add_to_repos(src, filename):
 
    if os.path.exists(src):
        path = os.path.join(store_by_upload_date(), filename + ".txt")
        shutil.move(src, path)
        upload_to_file_manifesto(filename, path)
        return "add_to_repos", src, path, filename
    else:
        print(f"This path dose not exist {src}")

def undo_del(filename):
    src = return_path_from_manifesto(filename)
    dst = os.path.join(store_by_upload_date(), filename + ".txt")
    update_manifesto(filename, mode = "undo_del", change = {"path": dst})
    shutil.move(src, dst)
    return "undo_del", src, dst, filename


 
    if os.path.exists(src):
        path = os.path.join(store_by_upload_date(), filename + ".txt")
        shutil.move(src, path)
        upload_to_file_manifesto(filename, path)
        return "add_to_repos", src, path, filename
    else:
        print(f"This path dose not exist {src}")

def undo_add_to_repos(src, dst, filename):

    shutil.move(src, dst)
    return "undo_add_to_repos", src, dst, filename

#WIP
def alter_tags(filename):
    pass
    print(get_metadate(filename, "tags"))
    user_input = input("Add tags (1), Remove tags (2)")

    if user_input == "1":
        tags = list(add_tags())
        old_tags = get_metadate(filename, "tags")
        print(tags)
        print(old_tags)
        for tag in old_tags:
            print(tag)
            tags.append(tag)
        print(tags)
        wait = input("OOOOOO")
        update_manifesto(filename, mode = "tags", change = {"tags": tags})
        return "add tags", filename, tags, old_tags

#Misc Functions
def word_counter(string):
    word_count = len(string.split())
    return word_count

def add_tags():
    print("Please input the tags you would like to associate with this document, seperating each tag with a comma.")
    print("For example: Coding,VSCode,The Internet, would turn into --> coding | vscode | the internet")
    tags = input("Tags: ")
    split_tags = tags.split(",")
    return split_tags
                

#main 
welcome_message = "Welcome to DocPro-s"
print(welcome_message)
print("-" * len(welcome_message) + "\n")

path = create_repos()
undo = DClass.Undo_Redo()
redo = DClass.Undo_Redo()

print(return_path_from_manifesto("CatDogCat"))

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
        filename = input("filename: ")
        if filename == None:
            pass
        else:
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

        if attributes["action"] == "create" or attributes["action"] == "dub" or attributes["action"] == "undo_del":
            act, prev_path, new_path, filename = delete_document(attributes["filename"])
            undo.pop()
            redo.push(act = act, path = new_path, prev_path = prev_path, filename = filename)

        elif attributes["action"] == "del":
            act, prev_path, new_path, filename = undo_del(attributes["filename"])
            undo.pop()
            redo.push(act = act, prev_path = prev_path, path = new_path, filename = filename)

        elif attributes["action"] == "rename":
            act, prev_name, new_name = rename_document(attributes["filename"], attributes["prev_name"])
            undo.pop()
            redo.push(act = act, prev_name = prev_name, filename = new_name)

        elif attributes["action"] == "add_to_repos":
            act, prev_path, new_path, filename = undo_add_to_repos(attributes["path"], attributes["prev_path"], attributes["filename"])
            undo.pop()
            redo.push(act = act, prev_path = prev_path, path = new_path, filename = filename)
        
        elif attributes["action"] == "undo_add_to_repos":
            act, prev_path, new_path, filename = add_to_repos(attributes["path"], attributes["prev_path"], attributes["filename"])
            undo.pop()
            redo.push(act = act, prev_path = prev_path, path = new_path, filename = filename)
            

    elif user_input == "8":
        if redo.peek() == None:
            print("Nothing to redo")
            continue
        attributes = redo.peek().get_attributes()

        if attributes["action"] == "create" or attributes["action"] == "dub" or attributes["action"] == "undo_del":
            act, prev_path, new_path, filename = delete_document(attributes["filename"])
            redo.pop()
            undo.push(act = act, path = new_path, prev_path = prev_path, filename = filename)

        elif attributes["action"] == "del":
            act, prev_path, new_path, filename = undo_del(attributes["filename"])
            redo.pop()
            undo.push(act = act, prev_path = prev_path, path = new_path, filename = filename)

        elif attributes["action"] == "rename":
            act, prev_name, new_name = rename_document(attributes["filename"], attributes["prev_name"])
            redo.pop()
            undo.push(act = act, prev_name = prev_name, filename = new_name)

        elif attributes["action"] == "add_to_repos":
            act, prev_path, new_path, filename = undo_add_to_repos(attributes["path"], attributes["prev_path"], attributes["filename"])
            redo.pop()
            undo.push(act = act, prev_path = prev_path, path = new_path, filename = filename)

        elif attributes["action"] == "undo_add_to_repos":
            act, prev_path, new_path, filename = add_to_repos(attributes["path"], attributes["prev_path"], attributes["filename"])
            redo.pop()
            undo.push(act = act, prev_path = prev_path, path = new_path, filename = filename)

    elif user_input == "9":
        filename = input("Filename: ")
        results = alter_tags(filename)
        act, filename, tags, prev_tags = results
        undo.push(act = act, filename = filename, tags = tags, prev_tags = prev_tags)
    
    elif user_input.lower() == "e":
        running = False

    else:
        print("Input ERROR!!! Invalid Input")

#removes files from backup folder when program is closed
shutil.rmtree(os.path.join(os.getcwd(), "Backup_Repository"))
os.makedirs(os.path.join(os.getcwd() + "/Backup_Repository"), exist_ok=True)
update_manifesto("n/a", mode = "perm_delete")
