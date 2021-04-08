import json
import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


with open('cities.json', encoding="utf8") as file:
  init_cities = json.load(file)


def start(update: Update, _: CallbackContext) -> None:
  """Send a message when the command /start is issued."""
  update.message.reply_text('Hi!')
  with open('data.json', encoding="utf8") as file:
        data = json.load(file) 
  game = False
  hints = 3
  used_cities = []
  id = str(update.message.chat.id)
  data[id] = {'game':game, 'hints':hints, 'used_cities':used_cities}
  with open('data.json', 'w', encoding="utf8") as file:
    json.dump(data, file)
  update.message.reply_text('Write /game for playing cities')


def help_command(update: Update, _: CallbackContext) -> None:
  """Send a message when the command /help is issued."""
  with open('data.json', encoding="utf8") as file:
      data = json.load(file) 
  id = str(update.message.chat.id)
  data[id]['hints'] -= 1
  if data[id]['game']:
    script_city = data[id]['used_cities'][-1]
    script_last_letter = get_last_letter(script_city)
    letter_cities = [city for city in init_cities if city[0]==script_last_letter and city not in data[id]['used_cities']]
    if letter_cities:
      update.message.reply_text(letter_cities[:2])
  update.message.reply_text('Help!')


def game_command(update: Update, _: CallbackContext) -> None:
  """Send a message when the command /game is issued."""
  with open('data.json', encoding="utf8") as file:
      data = json.load(file) 
  id = str(update.message.chat.id)
  data[id]['game'] = True 
  data[id]['used_cities'] = []
  script_city = random.choice(init_cities)
  data[id]['used_cities'].append(script_city)
  with open('data.json', 'w', encoding="utf8") as file:
    json.dump(data, file)
  update.message.reply_text('Send a message with the name of the city of Russia on the last letter')
  update.message.reply_text(script_city)


def stop_command(update: Update, _: CallbackContext) -> None:
  """Send a message when the command /stop is issued."""
  with open('data.json', encoding="utf8") as file:
      data = json.load(file)
  id = str(update.message.chat.id)
  data.id.game = False
  with open('data.json', 'w', encoding="utf8") as file:
    json.dump(data, file)
  update.message.reply_text('The game was stoped..')


def game(update: Update, _: CallbackContext) -> None:
  """Send a message when get message and game==True."""
  with open('data.json', encoding="utf8") as file:
      data = json.load(file) 
  id = str(update.message.chat.id)
  if data[id]['game']:
    script_city = data[id]['used_cities'][-1]
    user_city = update.message.text
    if user_city in init_cities:
      if user_city not in data[id]['used_cities']:
        data[id]['used_cities'].append(user_city)
        winner_chance = random.randint(1, 20)
        if winner_chance == 7:
          update.message.reply_text(f'Поздравяю, это победа!')
          update.message.reply_text(f'Чтобы сыграть еще раз, напишите /game')
          return
        script_last_letter = get_last_letter(script_city)
        if user_city[0] == script_last_letter:
          last_letter = get_last_letter(user_city)
          letter_cities = [city for city in init_cities if city[0]==last_letter and city not in data[id]['used_cities']]
          if letter_cities:
            script_city = random.choice(letter_cities)
            data[id]['used_cities'].append(script_city)
            update.message.reply_text(script_city)
            with open('data.json', 'w', encoding="utf8") as file:
              json.dump(data, file)
          else:
            update.message.reply_text(f'Поздравяю, это безоговорочная победа!')
            update.message.reply_text(f'Чтобы сыграть еще раз, напишите /game')    
        else:
          update.message.reply_text(f'Нужен город на букву {script_last_letter}')
      else:
        update.message.reply_text(f'Этот город уже был')  
    else:
        update.message.reply_text(f'Такого города нет в России')      


def get_last_letter(word):
  last_letter = ''
  i = -1
  last_letter = word[i].title()
  while last_letter in ['Ы', 'Ь', 'Ъ', 'Й']:
    i += -1
    last_letter = word[i].title()  
  return last_letter


def main() -> None:
  token = input()
  updater = Updater(token)
  dispatcher = updater.dispatcher
  dispatcher.add_handler(CommandHandler("start", start))
  dispatcher.add_handler(CommandHandler("help", help_command))
  dispatcher.add_handler(CommandHandler("game", game_command))
  dispatcher.add_handler(CommandHandler("stop", stop_command))
  dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, game))
  updater.start_polling()
  updater.idle()


if __name__ == '__main__':
  main()
