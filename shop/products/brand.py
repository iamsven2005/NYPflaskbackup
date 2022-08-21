class Brands:
    def __init__(self, brand):
        self.__brand = brand
    
    def set_brand(self, brand):
        self.__brand = brand
    def get_brand(self):
        return self.__brand

class Cat:
    def __init__(self, category):
        self.__category = category

    def set_category(self, category):
        self.__category = category
    def get_category(self):
        return self.__category