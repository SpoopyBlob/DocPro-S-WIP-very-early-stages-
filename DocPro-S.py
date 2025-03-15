import os
import datetime
import csv
import shutil

#Custom import that stores my classes
import DocPro_Classes as DClass

def create_repos():
    path = check_if_first()
    if path == True:
        print("Enter the pathway of the desired location to store your repository.")
        print("e.g. C://Users//James//Documents\n")
        path = input("") + "//DocPro-s"
        write_user_path(path)

    os.makedirs(path + "//File_Repository", exist_ok=True)
    os.makedirs(path + "//Backup_Repository", exist_ok=True)
    os.makedirs(path + "//Upload", exist_ok=True)
    os.chdir(path)
    return path
    
#Checks if the user has the filepaths
def check_if_first():
    #creates file if it dosen't already exist
    file = open("user_path.txt", "a")
    file.close()

    file = open("user_path.txt", "r")
    read = file.read()
    if len(read) == 0:
        file.close()
        return True
    else:
        file.close()
        return read
    
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

def add_document_to_repository(path, filename):
    src = path
    dst = os.getcwd() + "//DocPro-s//File_Repository//" + filename
    shutil.move(src, dst)

def view_document(path):
    file = open(path, 'r')
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

def word_counter(string):
    word_count = len(string.split())
    return word_count

def create_document(name, string):
    path = os.getcwd() + "//File_repository//" + name + ".txt"
    with open (path, 'w') as file_to_write:
        file_to_write.write(string)

def delete_document(filename):
    dst = os.getcwd() + "//Backup_repository//" + filename + ".txt"
    src = os.getcwd() + "//File_repository//" + filename + ".txt"
    shutil.move(src, dst)

def dupblicate_document(filename, new_filename):
    path = os.getcwd() +"//File_repository//"
    document = open(path + filename + ".txt", 'r')
    document_contents = document.read()
    document.close()

    path = os.getcwd() +"//File_repository//"
    with open(path + new_filename + ".txt", 'w') as dub_file:
        dub_file.write(document_contents)

#temp function until manifesto is created
def view_documents(path):
    print(os.listdir(path + "//File_repository"))


#main 
welcome_message = "Welcome to DocPro-s"
print(welcome_message)
print("-" * len(welcome_message) + "\n")
path = create_repos()

running = True
while running == True
    current_files_string = "Current Files:"
    print(current_files_string + "\n" + ("-" * len(current_files_string)))
    view_documents(path)
    print("Add document(a), Remove document (r), Dupblicate_document(d), Create document (c), Exit program (e)")
    user_input = input("Control: ")

    if user_input.lower() == a:
        path = input("Enter path:")
        filename = input("Filename: ")
        add_document_to_repository(path, filename)

    elif user_input.lower() == r:
        filename = input("Filename")
        delete_document()
    elif user_input.lower() == d:
        filename = input("Filename: ")
        new_filename = input("New_filename: ")
        dupblicate_document()
    elif user_input.lower() == c:
        name = input("Name: ")
        string = input("String: ")
        create_document()
    elif user_input.lower() == e:
        running == False

    else:
        print("Input ERROR!!! Invalid Input")








        


#view_document("File_repository//Hello.txt")
os.chdir("D://Code//Document Processing System//DocPro-S")
dupblicate_document("Story.txt", "Story_2.txt")





