import os
import telebot
import requests
from telebot import types

API_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

bot = telebot.TeleBot(API_TOKEN)

def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('📊 تقرير يومي', '🔍 رصيد عميل')
    markup.add('💸 سحب موظف')
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🤖 أهلاً بيك في نظام إدارة الصالون 💈",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: m.text == '📊 تقرير يومي')
def daily_report(message):
    data = {"action": "daily_report", "secret": SECRET_KEY}
    response = requests.post(WEB_APP_URL, json=data).json()
    bot.send_message(message.chat.id, response.get('message', 'تم'), reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == '🔍 رصيد عميل')
def ask_phone(message):
    msg = bot.send_message(message.chat.id, "📱 ابعت رقم العميل:")
    bot.register_next_step_handler(msg, get_balance)

def get_balance(message):
    phone = message.text.strip()
    data = {"action": "get_customer_balance", "phone": phone, "secret": SECRET_KEY}
    response = requests.post(WEB_APP_URL, json=data).json()
    bot.send_message(message.chat.id, response.get('message', 'تم'), reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == '💸 سحب موظف')
def ask_employee(message):
    msg = bot.send_message(message.chat.id, "👤 اسم الموظف:")
    bot.register_next_step_handler(msg, ask_amount)

def ask_amount(message):
    employee = message.text.strip()
    msg = bot.send_message(message.chat.id, "💰 المبلغ:")
    bot.register_next_step_handler(msg, lambda m: do_withdraw(m, employee))

def do_withdraw(message, employee):
    amount = message.text.strip()
    data = {
        "action": "employee_withdraw",
        "employee_name": employee,
        "amount": amount,
        "secret": SECRET_KEY
    }
    response = requests.post(WEB_APP_URL, json=data).json()
    bot.send_message(message.chat.id, response.get('message', 'تم'), reply_markup=main_menu())

print("✅ Bot Running...")
bot.infinity_polling()
