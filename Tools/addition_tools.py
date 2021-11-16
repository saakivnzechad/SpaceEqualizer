import os.path
import yaml.loader


class Parser:
    # initialize the class instance
    def __init__(self, local_path):
        self.i = None
        self.path = os.path.abspath(local_path)  # find full .yaml file path
        with open(self.path) as file:  # open .yaml file
            self.opened = yaml.load(file, Loader=yaml.FullLoader)  # parse .yaml file

    # getting needed variable from parsed .yaml file
    def get_state(self, name):
        for i in self.opened:  # enum of dictionary
            if i == name:  # check accordance of dict element with param
                return self.opened[i]  # returned if successful
        return 'nothing found'  # returned if error
    