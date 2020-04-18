import os

class MyOS:
    # Initialize with the starting directory
    def __init__(self, curr_dir):
        self.curr_dir = curr_dir
        self.path = []
        self.all_list = []
        self.file_list = []
        self.dir_list = []

        self.set_path(curr_dir)
        self.update_files()
        self.counter = len(self.path) - 1

    # Get the path as a list of strings, for later use
    def set_path(self, dir):
        self.path = (self.curr_dir.split("/"))[1::]

    # Get all the files in the current directory, except the hidden ones
    def set_all_files_list(self):
        self.all_list = list(filter(lambda file: file[0] != '.', os.listdir(self.curr_dir)))

    # Get all the directories in the current directory
    def set_dir_list(self):
        self.dir_list = [file for file in self.all_list if os.path.isdir(file)]
    
    # Get the files that are not directories in the current directory
    def set_file_list(self):
        self.file_list = [file for file in self.all_list if not os.path.isdir(file)]
       
    # Helper function to update all the files
    def update_files(self):
        self.set_all_files_list()
        self.set_file_list()
        self.set_dir_list()
    
    # Change current working directory
    def change_dir(self, new_dir):
        if new_dir:
            self.curr_dir = new_dir
            os.chdir(self.curr_dir)
            self.update_files()

    # Change current working directory to child
    def change_dir_child(self, new_dir):
        if new_dir and self.counter < len(self.path):
            self.change_dir(self.curr_dir + "/" + new_dir)
            self.set_path(self.get_dir())
            self.counter = len(self.path) - 1

    # Go to the parent directory
    def change_dir_parent(self):
        self.change_dir(os.path.dirname(self.curr_dir))
        self.path = self.path[:-1]
        self.counter -= 1

    # Change to the next and previous directory in the path
    def change_dir_previous(self):
        self.change_dir(os.path.dirname(self.curr_dir))
        self.counter -= 1

    def change_dir_next(self):
        if self.counter < len(self.path) - 1:
            self.change_dir(os.getcwd() + "/" + self.path[self.counter + 1])
            self.counter += 1

    # Get current directory
    def get_dir(self):
        return self.curr_dir
                
    # Get the list of files in the current directory
    def get_file_list(self):
        return self.file_list

    # Get the list of child directories in the current directory
    def get_dir_list(self):
        return self.dir_list

    # Get the full path of the current directory
    def get_path(self):
        str_list = []
        for elem in self.path:
            str_list.append("/")
            str_list.append(elem)
        return ''.join(str_list)

"""
abc = os.getcwd()

list1 = (abc.split("/"))[1::]
print(list1)

list2 = list1[0:4:]
print(list2)

counter = 0
for (x1, x2) in zip(list1, list2):
    if x1 != x2:
        break
    counter += 1


os_module = MyOS(os.getcwd()) # Initializaza os_module la un director anume
print(os_module.get_dir())
print(os_module.get_dir_list())
print(os_module.get_file_list())
print(os_module.counter)
'''
os_module.change_dir_previous()
print(os_module.get_dir())
print(os_module.get_dir_list())
print(os_module.get_file_list())
print(os_module.counter)

os_module.change_dir_previous()
print(os_module.get_dir())
print(os_module.get_dir_list())
print(os_module.counter)

os_module.change_dir_next()
print(os_module.get_dir())
print(os_module.get_dir_list())
print(os_module.counter)

os_module.change_dir_next()
print(os_module.get_dir())
print(os_module.get_dir_list())
print(os_module.counter)

#TODO sa modific cand schimb intr-un child pe cazuri
#TODO sa mai grupez din functii
#TODO coding style
"""
