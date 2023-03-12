import telebot
import openpyxl
from telebot import types

start = telebot.types.ReplyKeyboardMarkup(True, False)
start.row("O'zbekcha🇺🇿", 'Русский🇷🇺')


class Read:
    def __init__(self):
        self.name = None
        self.price = None
        self.retsept = None
        self.img = None
        self.list = []
        self.list_menu = self.list_in_list()
        self.pizza = types.ReplyKeyboardMarkup(True, False)

    def list_in_list(self):
        list = []
        excel = openpyxl.load_workbook("list.xlsx")
        sheet = excel["sheet1"]
        for col in sheet['A']:
            list.append(col.value)
        return list

    def food_info(self, food):
        dict = {}
        id = 1
        excel = openpyxl.load_workbook("list.xlsx")
        sheet = excel["sheet1"]
        for col in sheet['A']:
            dict[id] = str(col.value)
            id += 1

        for id, name in dict.items():
            if str(food) == name:
                self.name = sheet[f'A{id}']
                self.price = sheet[f'B{id}']
                self.retsept = sheet[f'C{id}']
                self.img = sheet[f'D{id}']
        return [self.name.value, self.price.value, self.retsept.value, self.img.value]

    def read_sheet_uz(self):

        if len(self.list_menu) % 3 == 0:
            for col in range(len(self.list_menu) // 3):
                pizza5_uz.row(str(self.list_menu[col * 3]), str(self.list_menu[col*3 + 1]), str(self.list_menu[col*3 + 2]))
        else:
            for col in range(len(self.list_menu) // 3 + 1):
                pizza5_uz.row(str(self.list_menu[col * 3]), str(self.list_menu[col*3 + 1]), str(self.list_menu[col*3 + 2]))

    def read_sheet_ru(self):

        if len(self.list_menu) % 3 == 0:
            for col in range(len(self.list_menu) // 3):
                pizza5_ru.row(str(self.list_menu[col * 3]), str(self.list_menu[col*3 + 1]), str(self.list_menu[col*3 + 2]))
        else:
            for col in range(len(self.list_menu) // 3 + 1):
                pizza5_ru.row(str(self.list_menu[col * 3]), str(self.list_menu[col*3 + 1]), str(self.list_menu[col*3 + 2]))


pizza_ru = telebot.types.ReplyKeyboardMarkup(True, False)
pizza_ru.row("Заказать🍕", "Мои заказы📥")
pizza_ru.row("Вконтакте☎️", "⬅️Назад")

pizza_uz = telebot.types.ReplyKeyboardMarkup(True, False)
pizza_uz.row("Buyurtma berish🍕", "Buyutmalar📥")
pizza_uz.row("Murojat☎️", "⬅️Orqaga")


eda_napitki_ru = types.InlineKeyboardMarkup()
but_1 = types.InlineKeyboardButton(text="🍕Пицца", callback_data="Пицца")
but_2 = types.InlineKeyboardButton(text="🍱 Комбо", callback_data="Комбо")
eda_napitki_ru.add(but_1)
eda_napitki_ru.add(but_2)


eda_napitki_uz = types.InlineKeyboardMarkup()
but_1 = types.InlineKeyboardButton(text="🍕Pizza", callback_data="Pizza")
but_2 = types.InlineKeyboardButton(text="🍱 Kombo", callback_data="Kombo")
eda_napitki_uz.add(but_1)
eda_napitki_uz.add(but_2)

pizza5_uz = types.ReplyKeyboardMarkup(True, False)
Menu = Read()
Menu.read_sheet_uz()
pizza5_uz.add('◀️Orqaga')

pizza5_ru = types.ReplyKeyboardMarkup(True, False)
Menu = Read()
Menu.read_sheet_ru()
pizza5_ru.add('◀️Назад')


cart_food = types.InlineKeyboardMarkup()
cart = types.InlineKeyboardButton(text="➖", callback_data="minus")
cart1 = types.InlineKeyboardButton(text=0, callback_data="cart")
cart2 = types.InlineKeyboardButton(text="➕", callback_data="plus")
cart_food.row(cart, cart1, cart2)




def food_num(oper, food, user):
    i = 0
    if oper == 'plus':
        i+=1
        db.cursor.execute(f"UPDATE user SET food_len = {i} WHERE list_food = '{food}';")
        cart1.text = i
        db.db.commit()
    elif oper == 'minus':
        i-=1
        db.cursor.execute(f"UPDATE user SET food_len = {i} WHERE list_food = '{food}';")
        db.db.commit()
    else:
        print("so fire")



location = types.ReplyKeyboardMarkup(True, False)
button_geo = types.KeyboardButton(text="Отправить местоположение",
    request_contact=True)
location.add(button_geo)



import db

class Food:
    def __init__(self, user, food):
        self.food = food
        self.user = user

    def save_db(self):
        db.cursor.execute(f"INSERT INTO user (useername, phone, location, price, list_food, foo) VALUES (?, ?, ?, ?, ?)",
                          ())
        db.db.commit()


