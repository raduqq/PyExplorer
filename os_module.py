import os

class MyOS:
    def __init__(self, curr_dir):
        self.curr_dir = curr_dir

    def print_dir(self):
        print(self.curr_dir)

    # Get all the files in the current directory, except the hidden ones
    def get_file_list(self):
        self.file_list = list(filter(lambda file: file[0] != '.', os.listdir(self.curr_dir)))
        return self.file_list

    # Get all the directories in the current directory
    def get_dir_list(self):
        dir_list = []
        try:
            dir_list = [file for file in self.file_list if os.path.isdir(file)]
        except:
            print("Error!")
        return dir_list
    
    # Change current working directory
    def change_dir(self, new_dir):
        if new_dir:
            self.curr_dir += "/" + new_dir
            os.chdir(self.curr_dir)

    # Go to the parent directory
    def change_dir_parent(self):
        self.curr_dir = os.path.dirname(self.curr_dir)
        os.chdir(self.curr_dir)
                
# Test

os_module = MyOS(os.getcwd())

os_module.print_dir()
os_module.get_file_list()

dir_list = os_module.get_dir_list()
print(dir_list)

os_module.change_dir(dir_list[0])
os_module.print_dir()

os_module.change_dir_parent()
os_module.print_dir()