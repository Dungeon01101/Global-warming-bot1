# импорт библиотек
import telebot

from config import *
from telebot import types
from weather import *

# "активация" бота
bot = telebot.TeleBot(TOKEN)

# функция на команду /start
@bot.message_handler(commands=['start'])
def start(message):
	sti = open('components/image.jpg', 'rb')
	bot.send_photo(message.chat.id, sti)

	# клавиатура
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Почему?🧐")
	item2 = types.KeyboardButton("Как я помогу?🧐")
	item3 = types.KeyboardButton("Назови погоду в моём городе🌥")

	markup.add(item1, item2, item3)

	bot.send_message(message.chat.id, 'Привет, {0.first_name}!\nЯ - {1.first_name}, бот созданный что бы объяснить тему и ответить на вопросы о глобальном потеплении.'.format(message.from_user, bot.get_me()),
		parse_mode='html', reply_markup=markup)

# функция на ответ
@bot.message_handler(content_types=['text'])
def answer(message):
	if message.chat.type == 'private':
		if message.text == 'Назови погоду в моём городе🌥':
			# функция для определённого сообщения
			def process_reply(message):
				try:
					bot.send_message(message.chat.id, temperature_w(message.text))
				except pyowm.commons.exceptions.TimeoutError:
					bot.send_message(message.chat.id, 'К сожалению сейчас невозможно определить температуру из-за технических неполадок☹️')	
				except Exception as a:
					print(repr(a))
					bot.send_message(message.chat.id, 'Пожалуйста напишите правильный город')		
			bot.send_message(message.chat.id, 'Назовите ваш город')
			bot.register_next_step_handler(message, process_reply)
			
		elif message.text == 'Почему?🧐':
			markup = types.InlineKeyboardMarkup(row_width=1)
			item1 = types.InlineKeyboardButton("Расскажи больше", callback_data='more')

			markup.add(item1)

			bot.send_message(message.chat.id, 'Ископаемые виды топлива — уголь, нефть и газ — вносят наибольший вклад в глобальное изменение климата: на их долю приходится свыше 75 процентов глобальных выбросов парниковых газов и почти 90 процентов всех выбросов углекислого газа.',
				reply_markup=markup)

		elif message.text == 'Как я помогу?🧐':
			bot.send_message(message.chat.id, '1) Чаще пользоваться общественным транспортом \n2) Экономить энергию \n3) Сократить потребление мяса \n4) Утилизировать отходы, использовать вторсырье, даже воду \n5) Информировать и обучать')

		else:
			bot.send_message(message.chat.id, 'Извините, я не понял☹️')	

# функция для "мини-клавиатуры" под сообщениями
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			if call.data == 'more':
				bot.send_message(call.message.chat.id, 'Ископаемые виды топлива — уголь, нефть и газ — вносят наибольший вклад в глобальное изменение климата: на их долю приходится свыше 75 процентов глобальных выбросов парниковых газов и почти 90 процентов всех выбросов углекислого газа.')
				bot.send_message(call.message.chat.id, 'Покрывая Землю, выбросы парниковых газов задерживают солнечное тепло. Это приводит к глобальному потеплению и изменению климата. В настоящее время планета нагревается быстрее, чем когда-либо в истории человечества. Повышение температуры со временем меняет погодные условия и нарушает обычный природный баланс. Это создает множество рисков для людей и всех остальных форм жизни на Земле.')
			
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Почему?🧐',
				reply_markup=None)

	except Exception as e:
		print(repr(e))

# запуск бота
bot.polling(none_stop=True)	
