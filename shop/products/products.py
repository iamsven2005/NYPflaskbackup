class Product:
    def __init__(self, name, price, discount, stock, desc, brand, category,expenses):
        self.__name = name
        self.__price = price
        self.__discount = discount
        self.__stock = stock
        self.__desc = desc
        self.__brand = brand
        self.__category = category
        self.__image = ""
        self.__expenses = 0
    
    def set_name(self,name):
        self.__name = name
    def set_price(self, price):
        self.__price = price
    def set_discount(self,discount):
        self.__discount = discount
    def set_stock(self, stock):
        self.__stock = stock
    def set_desc(self, desc):
        self.__desc = desc
    def set_brand(self,brand):
        self.__brand = brand
    def set_category(self, category):
        self.__category = category
    def set_image(self, image):
        self.__image = image
    def set_expenses(self, expenses):
        self.__expenses = expenses

    def get_name(self):
        return self.__name
    def get_price(self):
        return self.__price
    def get_discount(self):
        return self.__discount
    def get_stock(self):
        return self.__stock
    def get_desc(self):
        return self.__desc 
    def get_brand(self):
        return self.__brand
    def get_category(self):
        return self.__category
    def get_image(self):
        return self.__image
    def get_expenses(self):
        return self.__expenses
    