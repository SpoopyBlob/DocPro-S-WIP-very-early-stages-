import os
import datetime
import csv
import shutil

#Custom import that stores my classes
import DocPro_Classes as DClass

def create_repos():
    print("Enter the pathway of the desired location to store your repository.")
    print("e.g. C://Users//James//Documents\n")
    path = input("") + "//DocPro-s"
    os.makedirs(path + "//File_Repository", exist_ok=True)
    os.makedirs(path + "//Backup_Repository", exist_ok=True)
    os.makedirs(path + "//Upload")
    os.chdir(path)
    

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
    document = open(path + filename, 'r')
    document_contents = document.read()
    document.close()

    path = os.getcwd() +"//File_repository//"
    with open(path + new_filename, 'w') as dub_file:
        dub_file.write(document_contents)




        


#view_document("File_repository//Hello.txt")
os.chdir("D://Code//Document Processing System//DocPro-S")
dupblicate_document("Story.txt", "Story_2.txt")





