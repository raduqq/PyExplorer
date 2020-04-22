import os

class MyOS:
    # Initialize with the starting directory
    def __init__(self, curr_dir):
        self.curr_dir = curr_dir
        self.path = []
        self.all_list = []
        self.file_list = []
        self.dir_list = []
        self.counter = -1

        self.update()
      
    def update(self):
        self.set_path()
        self.update_files()
        self.counter = len(self.path) - 1

    # Get the path as a list of strings, for later use
    def set_path(self):
        self.path = (self.curr_dir.split("/"))[1::]

    # Get all the files in the current directory, except the hidden ones
    def set_all_files_list(self):
        self.all_list = list(filter(lambda file: file[0] != '.', os.listdir(self.curr_dir)))

    # Get all the directories in the current directory
    def set_dir_list(self):
        self.dir_list = [file for file in self.all_list if os.path.isdir(file)]
        self.dir_list.sort()

    # Get the files that are not directories in the current directory
    def set_file_list(self):
        self.file_list = [file for file in self.all_list if not os.path.isdir(file)]
        self.file_list.sort()
       
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
            self.set_path()
            self.counter = len(self.path) - 1

    # Go to the parent directory
    def change_dir_parent(self):
        if self.counter >= 1:
            self.change_dir(os.path.dirname(self.curr_dir))
            self.path = self.path[:-1]
            self.counter -= 1

    # Change to the next and previous directory in the path
    def change_dir_previous(self):
        if self.counter > 0:
            self.change_dir(os.path.dirname(self.curr_dir))
            self.counter -= 1

    def change_dir_next(self):
        if self.counter < len(self.path) - 1:
            self.change_dir(os.getcwd() + "/" + self.path[self.counter + 1])
            self.counter += 1

    # Change current working directory to a directory in the path
    def change_dir_path(self, new_dir):
        location = self.path.index(new_dir)
        new_location = self.path[:location + 1]
        self.change_dir(self.get_path(new_location))
        self.counter = location

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
    def get_path(self, temp_path):
        str_list = []
        for elem in temp_path:
            str_list.append("/")
            str_list.append(elem)
        return ''.join(str_list)

    # Get the path as a list of string
    def get_path_list(self):
        return self.path

    # Get the location of the cursor in the path
    def get_counter(self):
        return self.counter
