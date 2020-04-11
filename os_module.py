import os

class MyOS:
    # Get all the files in the current directory, except the hidden ones
    def set_file_list(self):
        self.file_list = list(filter(lambda file: file[0] != '.', os.listdir(self.curr_dir)))

    # Get all the directories in the current directory
    def set_dir_list(self):
        self.dir_list = []
        try:
            self.dir_list = [file for file in self.file_list if os.path.isdir(file)]
        except:
            print("Error! Could not access the file list.")
    
    # Initialize with the starting directory
    def __init__(self, curr_dir):
        self.curr_dir = curr_dir
        self.set_file_list()
        self.set_dir_list()
    
    # Change current working directory
    def change_dir(self, new_dir):
        if new_dir:
            self.curr_dir += "/" + new_dir
            os.chdir(self.curr_dir)
            self.set_file_list()
            self.set_dir_list()

    # Go to the parent directory
    def change_dir_parent(self):
        self.curr_dir = os.path.dirname(self.curr_dir)
        os.chdir(self.curr_dir)
        self.set_file_list()
        self.set_dir_list()

    # Test methods
    def get_dir(self):
        return self.curr_dir
                
    def get_file_list(self):
        if self.file_list:
            return self.file_list

    def get_dir_list(self):
        if self.dir_list:
            return self.dir_list
# Test

os_module = MyOS(os.getcwd())

print(os_module.get_dir())
print(os_module.get_file_list())
print(os_module.get_dir_list())

# Change to child
dir_list = os_module.get_dir_list()
os_module.change_dir(dir_list[0])
print(os_module.get_dir())
print(os_module.get_file_list())
print(os_module.get_dir_list())

# Change to parent
os_module.change_dir_parent()
print(os_module.get_dir())
print(os_module.get_file_list())
print(os_module.get_dir_list())

# Change to parent again
os_module.change_dir_parent()
print(os_module.get_dir())
print(os_module.get_file_list())
print(os_module.get_dir_list())

# Change to parent again
os_module.change_dir_parent()
print(os_module.get_dir())
print(os_module.get_file_list())
print(os_module.get_dir_list())