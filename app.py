# - *- coding: utf- 8 - *-
import asyncio
import time
from datetime import datetime
import telebot
import menu
import config
import db
language = None

bot = telebot.TeleBot(config.token, parse_mode=None)
print("Start")


joinedFile = open("joined.txt", "r")
joinedUsers = set()
for line in joinedFile:
    joinedUsers.add(line.strip())
joinedFile.close()

order_client = None


local_food = None
user = None
@bot.message_handler(commands=["start"])
def send_welcome(message):
    if not str(message.chat.id) in joinedUsers:
        joinedFile = open("joined.txt", "a")
        joinedFile.write(str(message.chat.id) + "\n")
        joinedUsers.add(str(message.chat.id))
        bot.send_message(message.chat.id, "Assalomu alaykum!🖐 Chopar Pizza🍕 yetkazib berish xizmatiga xush kelibsiz.\n\n   Biz eng mazali pizzani👌 yaratamiz. Xatolarni tan olishdan va muvaffaqiyatlaringizni siz bilan baham ko'rishdan qo'rqmaymiz. Ammo bizning asosiy maqsadimiz sizga eng mazali pitssani iloji boricha tezroq etkazib berishdir.\n\n Здравствуйте! Добро пожаловать в службу доставки Chopar Pizza🍕.\n\n   Мы создаём саммый вкусный пицции👌. Не боимся признавать ошибки и делиться успехами с вами. Но наша главная цель — доставлять вам самую вкусную пиццу максимально быстро.", reply_markup=menu.start)
    else:
        bot.send_message(message.chat.id, "Assalomu alaykum!🖐 Chopar Pizza🍕 yetkazib berish xizmatiga xush kelibsiz.\n\n   Biz eng mazali pizzani👌 yaratamiz. Xatolarni tan olishdan va muvaffaqiyatlaringizni siz bilan baham ko'rishdan qo'rqmaymiz. Ammo bizning asosiy maqsadimiz sizga eng mazali pitssani iloji boricha tezroq etkazib berishdir.\n\n Здравствуйте! Добро пожаловать в службу доставки Chopar Pizza🍕.\n\n   Мы создаём саммый вкусный пицции👌. Не боимся признавать ошибки и делиться успехами с вами. Но наша главная цель — доставлять вам самую вкусную пиццу максимально быстро.", reply_markup=menu.start)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        menus = menu.Read()
        if call.data == 'Пицца':
            bot.send_message(chat_id=call.message.chat.id, text="Выбирай",
                                           reply_markup=menu.pizza5_ru)

        elif call.data == 'Pizza':
            bot.send_message(chat_id=call.message.chat.id, text="Tanlang",
                                           reply_markup=menu.pizza5_uz)

        elif call.data == "minus":
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          inline_message_id=call.inline_message_id, reply_markup=menu.food_num('minus', local_food, call.message.chat.id))
        elif call.data == "plus":
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          inline_message_id=call.inline_message_id, reply_markup=menu.food_num('plus', local_food, call.message.chat.id))

        elif call.data == 'cart':
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          inline_message_id=call.inline_message_id, reply_markup=menu.plus())


        elif call.data == 'Комбо':
            bot.answer_callback_query(
                callback_query_id=call.id, show_alert=False, text="К сожалению, данный товар закончился")

        else:
            bot.send_message(call.message.chat.id, "Ничего не понятно!")


@bot.message_handler(content_types=["text"])
def send(message):
    menus = menu.Read()
    user = message.chat.id
    if message.text == "O'zbekcha🇺🇿":
        photo = open('/home/yoqub/bot/dodo_2077.jpeg', 'rb')
        bot.send_photo(message.chat.id, photo)
        bot.send_message(message.chat.id, "Pizza buyurtma berish:",
                         reply_markup=menu.pizza_uz)
    elif message.text == 'Русский🇷🇺':
        photo = open('/home/yoqub/bot/dodo_2077.jpeg', 'rb')
        bot.send_photo(message.chat.id, photo)
        bot.send_message(message.chat.id, "Заказать пиццу:",
                         reply_markup=menu.pizza_ru)

    elif message.text == 'Заказать🍕':
        bot.send_message(message.chat.id, "Выберите категорию: ", reply_markup=menu.eda_napitki_ru)

    elif message.text == 'Buyurtma berish🍕':
        bot.send_message(message.chat.id, "Kategoriyani tanlang: ", reply_markup=menu.eda_napitki_uz)

    elif message.text == 'Вконтакте☎️' or message.text == 'Murojat☎️':
        bot.send_message(
            message.chat.id, "Admin: +998901234567", reply_markup=menu.location)

    elif message.text == '◀️Orqaga':
        bot.send_message(message.chat.id, "...", reply_markup=menu.pizza_uz)

    elif message.text == '◀️Назад':
        bot.send_message(message.chat.id, "...", reply_markup=menu.pizza_ru)

    elif message.text == '⬅️Orqaga':
        bot.send_message(message.chat.id, "...", reply_markup=menu.start)

    elif message.text == '⬅️Назад':
        bot.send_message(message.chat.id, "...", reply_markup=menu.start)

    elif message.text == 'Отправить местоположение':
        bot.send_message(message.chat.id, "...", reply_markup=menu.location)

    elif message.text in menus.list_in_list():
        local_food = message.text
        url = str(menus.food_info(message.text)[3])
        bot.send_message(message.chat.id,
                                  f"<a href='{url}'>{menus.food_info(message.text)[0]}</a>\n\nИнгредиенты: Пицца 30 см, {menus.food_info(message.text)[2]}\n\nЦена: {menus.food_info(message.text)[1]} сум.", parse_mode='HTML',
                         reply_markup=menu.cart_food)

        db.cursor.execute(f"INSERT INTO user (useername, phone, location, price, list_food, food_len) VALUES (?, ?, ?, ?, ?, ?)", (bot.user.id, None, None, menus.food_info(message.text)[1], message.text, 1))
        db.db.commit()
        # db.cursor.close()

    else:
        bot.send_message(message.chat.id, "Please if you have questions call this number +998901234567!")


if __name__ == '__main__':
    while True:
        try:
            bot.polling(non_stop=True, interval=0)
        except Exception as e:
            print(e)
            time.sleep(5)
            continue