import os.path
import yaml.loader


class Based:
    def __init__(self):
        self.deltaA = 0
        self.deltaB = 0
        self._deltaTime = 0
    def deltaTime(self, ticks):
        self.deltaA = ticks
        self._deltaTime = (self.deltaA - self.deltaB) / 1000.0
        self.deltaB = self.deltaA
        return self._deltaTime



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

