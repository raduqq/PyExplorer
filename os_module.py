import os

class MyOS:
    # Initialize with the starting directory
    def __init__(self, curr_dir):
        self.curr_dir = curr_dir
        self.all_list = []
        self.file_list = []
        self.dir_list = []
        self.update_files()

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
    def change_dir_child_click(self, new_dir):
        if new_dir:
            self.change_dir(self.curr_dir + "/" + new_dir)

    # Go to the parent directory
    def change_dir_parent(self):
        self.change_dir(os.path.dirname(self.curr_dir))

    # Test methods
    def get_dir(self):
        return self.curr_dir
                
    def get_file_list(self):
        return self.file_list

    def get_dir_list(self):
        return self.dir_list