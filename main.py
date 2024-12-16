from ttkbootstrap import Window, Label, Entry, Button, Treeview, OUTLINE, PRIMARY, DANGER, INFO, SECONDARY, SUCCESS, \
    WARNING
import os
from fnmatch import fnmatch
from pathlib import Path
from datetime import datetime
from ttkbootstrap.dialogs import Messagebox
import shutil
from tkinter import simpledialog

window = Window(title="Explore Path Application", themename="cyborg")
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(5, weight=1)

path_label = Label(window, text="Path")
path_label.grid(row=0, column=0, pady=10, padx=10, sticky="e")

path_entry = Entry(window)
path_entry.grid(row=0, column=1, pady=10, padx=(0, 10), sticky="ew")

item_list = []


def explore_path():
    """ this is as same as os and scandir / in here you don't need to make an object then work with this.
        also, it is useful for when you look for a specific file type (the file type is one of its attributes.)
        for removing a file or folder use : unlink() """
    path = path_entry.get()
    row_number = 1
    for item in item_list:
        explore_treeview.delete(item)
    item_list.clear()

    path_lib = Path(path)
    path_lib.iterdir()  # it is the same as scandir

    for window_path in path_lib.iterdir():
        entry_type = "File"
        entry_size = ""  # we calculate the size for only files not folders
        # stat gives back all the information of the file
        information = window_path.stat()
        if window_path.is_dir():
            entry_type = "Folder"
        else:
            entry_size = information.st_size // 1024

        date_created = datetime.fromtimestamp(information.st_ctime)
        date_modified = datetime.fromtimestamp(information.st_mtime)
        date_accessed = datetime.fromtimestamp(information.st_atime)

        item = explore_treeview.insert("", "end", iid=str(window_path), text=str(row_number),
                                       values=(window_path.name, entry_type, entry_size, date_created, date_modified,
                                               date_accessed))
        row_number += 1
        item_list.append(item)

    # # scandir() is a generator
    # for dir_entry in os.scandir(path):
    #     entry_type = "File"
    #     entry_size = ""  # we calculate the size for only files not folders
    #     # stat gives back all the information of the file
    #     information = dir_entry.stat()
    #     if dir_entry.is_dir():
    #         entry_type = "Folder"
    #     else:
    #         entry_size = information.st_size // 1024
    #
    #     date_created = datetime.fromtimestamp(information.st_ctime)
    #     date_modified = datetime.fromtimestamp(information.st_mtime)
    #     date_accessed = datetime.fromtimestamp(information.st_atime)
    #
    #     item = explore_treeview.insert("", "end", iid=dir_entry.path, text=str(row_number),
    #                                    values=(dir_entry.name, entry_type, entry_size, date_created,date_modified,date_accessed))
    #     row_number += 1
    #     item_list.append(item)


explore_button = Button(window, text="Explore", command=explore_path)
explore_button.grid(row=0, column=2, pady=10, padx=(0, 10), sticky="w")


def open_folder():
    full_path = explore_treeview.selection()[0]
    path_entry.delete(0, "end")
    path_entry.insert(0, full_path)
    explore_path()


open_folder_button = Button(window, text="Open", bootstyle=WARNING, command=open_folder)
open_folder_button.grid(row=0, column=3, pady=10, padx=(0, 10), sticky="w")

new_folder_label = Label(window, text="New Folder")
new_folder_label.grid(row=1, column=0, pady=(0, 10), padx=(0, 10), sticky="e")

new_folder_entry = Entry(window)
new_folder_entry.grid(row=1, column=1, pady=10, padx=(0, 10), sticky="ew")


def create_folder():
    new_folder = new_folder_entry.get()
    path_lib = Path(new_folder)
    # if os.path.exists(new_folder):
    if path_lib.exists():
        Messagebox.show_error(title="Error", message="Cannot Create The Folder ! It already Exists")
    else:
        # os.mkdir(new_folder)

        path_lib.mkdir()
        Messagebox.show_info(title="Info", message="Folder Created Successfully")


new_folder_button = Button(window, text="Create", bootstyle=INFO, command=create_folder)
new_folder_button.grid(row=1, column=2, pady=10, padx=(0, 10), sticky="ew")

search_label = Label(window, text="Search in Folder")
search_label.grid(row=2, column=0, pady=10, padx=10, sticky="e")

search_entry = Entry(window)
search_entry.grid(row=2, column=1, pady=10, padx=(0, 10), sticky="ew")


def search():
    for item in item_list:
        explore_treeview.delete(item)
    item_list.clear()
    term = search_entry.get()
    path = path_entry.get()
    row_number = 1  # Move row_number initialization outside the loop

    for main_folder, folder_list, file_list in os.walk(path):
        for file in file_list:
            if fnmatch(file, term):
                full_path = os.path.join(main_folder, file)  # you can get the full address of the file using join
                path_lib = Path(full_path)

                entry_type = "File"
                entry_size = ""
                if path_lib.is_dir():
                    entry_type = "Folder"
                else:
                    entry_size = path_lib.stat().st_size // 1024

                date_created = datetime.fromtimestamp(path_lib.stat().st_ctime)
                date_modified = datetime.fromtimestamp(path_lib.stat().st_mtime)
                date_accessed = datetime.fromtimestamp(path_lib.stat().st_atime)

                item = explore_treeview.insert("", "end", iid=str(path_lib), text=str(row_number),
                                               values=(path_lib.name, entry_type, entry_size, date_created,
                                                       date_modified,
                                                       date_accessed))
                row_number += 1
                item_list.append(item)


search_button = Button(window, text="Search", bootstyle=SUCCESS, command=search)
search_button.grid(row=2, column=2, pady=10, padx=(0, 10), sticky="ew")


# this is code for one path deletion
# def delete():
#     delete_files = explore_treeview.selection()
#
#     if delete_files:
#         file_path = delete_files[0]
#         confirm = Messagebox.show_question(
#             title="Confirm Deletion",
#             message="Are you sure you want to delete this file?",
#             buttons=['No:secondary', 'Yes:danger']
#         )
#         if confirm == 'Yes':
#             if os.path.exists(file_path):
#                 for path in delete_files:
#                     path_lib = Path(file_path)
#                     if path_lib.is_file():
#                         """ we have 3 ways to delete a file """
#                         """ but there is something that you should consider : what if someone delete the file earlier that you do in your application?
#                                             in this occasion using path lib will give back error to you . unless you handel the error using a parameter for unlink named : missing ok """
#                         path_lib.unlink(missing_ok=True)
#                         # os.unlink(file_path)
#                         # os.remove(file_path)  # For files
#                         Messagebox.show_info(title="Success", message="File deleted successfully")
#                         explore_path()  # Refresh the view
#                     elif path_lib.is_dir():
#                         # os.rmdir(file_path)  # For directories
#                         full_path = str(path_lib)
#                         shutil.rmtree(full_path)  # if the folder was not empty
#                         Messagebox.show_info(title="Success", message="Folder deleted successfully")
#                         explore_path()  # Refresh the view
#         else:
#             Messagebox.show_warning(title="Warning", message="Please select a file to delete")   # this s

def delete():
    """this is a method for delete multiple paths"""
    delete_files = explore_treeview.selection()
    if delete_files:
        confirm = Messagebox.show_question(
            title="Confirm Deletion",
            message=f"Are you sure you want to delete {len(delete_files)} item(s)?",
            buttons=['No:secondary', 'Yes:danger']
        )
        if confirm == 'Yes':
            for file_path in delete_files:
                if os.path.exists(file_path):
                    path_lib = Path(file_path)
                    if path_lib.is_file():
                        path_lib.unlink(missing_ok=True)
                    elif path_lib.is_dir():
                        shutil.rmtree(str(path_lib))
            Messagebox.show_info(title="Success", message="Items deleted successfully")
            explore_path()
    else:
        Messagebox.show_warning(title="Warning", message="Please select files to delete")


delete_button = Button(window, text="Delete", bootstyle=DANGER + OUTLINE, command=delete)
delete_button.grid(row=3, column=1, pady=(0, 10), padx=(0, 10), sticky="ew")


def rename():
    source_path = explore_treeview.selection()[0]
    if source_path:
        new_name = simpledialog.askstring("Rename", "Enter new name:")
        if new_name:
            try:
                path_lib = Path(source_path)
                new_path = path_lib.parent / new_name
                os.rename(source_path, new_path)
                Messagebox.show_info(title="Success", message="Renamed successfully!")
                explore_path()
            except OSError as e:
                Messagebox.show_error(title="Error", message=f"Could not rename: {str(e)}")

        else:
            error_message = Messagebox.show_error(title="Error", message="Please enter a new name")

    else:
        error_message = Messagebox.show_error(title="Error", message="No File or Folder s being selected ")


rename_button = Button(window, text="Rename", bootstyle=WARNING + OUTLINE, width=50, command=rename)
rename_button.grid(row=4, column=1, pady=10, padx=(40, 0), sticky="w")


def move():
    source_paths = explore_treeview.selection()
    if source_paths:
        destination_path = simpledialog.askstring("Destination", f"Enter destination for {len(source_paths)} item(s):")
        if destination_path:
            try:
                for path in source_paths:
                    shutil.move(path, destination_path)
                Messagebox.show_info(title="Success", message="Items moved successfully!")
                explore_path()
            except Exception as e:
                Messagebox.show_error(title="Error", message=f"Could not move: {str(e)}")


move_button = Button(window, text="Move", bootstyle=WARNING + OUTLINE, width=50, command=move)
move_button.grid(row=4, column=1, pady=10, padx=(0, 0))


def copy():
    source_paths = explore_treeview.selection()
    if source_paths:
        destination_path = simpledialog.askstring("Destination", f"Enter destination for {len(source_paths)} item(s):")
        if destination_path:
            try:
                for file_path in source_paths:
                    if os.path.exists(file_path):
                        path_lib = Path(file_path)
                        dest = Path(destination_path) / path_lib.name

                        # Handle name conflicts
                        counter = 1
                        while dest.exists():
                            new_name = f"{path_lib.stem}_{counter}{path_lib.suffix}"
                            dest = Path(destination_path) / new_name
                            counter += 1

                        if path_lib.is_file():
                            shutil.copy2(file_path, dest)
                        elif path_lib.is_dir():
                            shutil.copytree(file_path, dest)

                Messagebox.show_info(title="Success", message="Items copied successfully")
                explore_path()
            except Exception as e:
                Messagebox.show_error(title="Error", message=f"Could not copy: {str(e)}")
    else:
        Messagebox.show_warning(title="Warning", message="Please select files to Copy")


copy_button = Button(window, text="Copy", bootstyle=WARNING + OUTLINE, width=50, command=copy)
copy_button.grid(row=4, column=1, pady=10, padx=(0, 40), sticky="e")

explore_treeview = Treeview(window, columns=("name", "type", "size", "create", "modified", "accessed"))
explore_treeview.grid(row=5, column=1, pady=(0, 10), padx=(0, 10), sticky="nsew")

explore_treeview.heading("#0", text="#")
explore_treeview.heading("#1", text="Name")
explore_treeview.heading("#2", text="Type")
explore_treeview.heading("#3", text="Size(KB)")
explore_treeview.heading("#4", text="Date Created")
explore_treeview.heading("#5", text="Date Modified")
explore_treeview.heading("#6", text="Date Accessed")

explore_treeview.column("#0", width=50)

window.mainloop()
