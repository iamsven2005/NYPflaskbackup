class Updates():
    def __init__(self, name, spend):
        self.__name = name
        self.__spend = spend
    def get_name(self):
        return self.__name
    def get_spend(self):
        return self.__spend
    def set_name(self, name):
        self.__name = name
    def set_spend(self, spend):
        self.__spend = spend