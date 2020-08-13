import sys
import time
import telebot

bot = telebot.TeleBot(token=TOKEN)

# Dicionário deve ser atualizado sempre que um dispositivo novo é instalado
# e seu canal respectivo é criado. O mesmo para a lista available_devices.
devices = {
    device_id: channel_link,
}

users = {
    0: devices.keys()
}

available_devices = [device_id]

id_name = {
    device_id: device_name,
}

def find_at(msg):
    for text in msg:
        if '@' in text:
            return text

# Comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
    "Olá! Para ter acesso aos canais com atualizações sobre os ambientes, envie /join @device_id.\n\n"+
    "Para acessar uma lista com seus dispositivos cadastrados, envie /mydevices.")

# Comando /join
@bot.message_handler(commands=['join'])
def at_answer(message):
    if message.text is not None and '@' in message.text:
        texts = message.text.split(' ')
        at_text = find_at(texts)

        # Retorna o link para o canal desejado se o device_id for válido.
        if at_text[1:] in available_devices:
            bot.reply_to(message,
            "Acesse o canal: {}".format(devices[at_text[1:]]))

            # Se o usuário não está cadastrado, inclui-o no dictionary users.
            if message.from_user.id not in users:
                users[message.from_user.id] = []

            # Inclui o device aos disponíveis ao usuário, caso ainda não esteja
            # cadastrado.
            if at_text[1:] not in users[message.from_user.id]:
                users[message.from_user.id].append(id_name[at_text[1:]])
                f = open('users.txt', 'a')
                f.write("{}".format(message.from_user.id)+" {}".format(users[message.from_user.id])+"\n")
                f.close()
            print(users[message.from_user.id])
        else:
            bot.reply_to(message,
            "Este dispositivo não existe. Tente novamente.")
    else:
        bot.reply_to(message,
        "Por favor, inclua @device_id ao fim do comando.")


@bot.message_handler(commands=['mydevices'])
def at_answer(message):
    if message.from_user.id not in users.keys() or users[message.from_user.id] == []:
        bot.reply_to(message, "Você não possui dispositivos cadastrados.")
    else:
        bot.reply_to(message,
    "Seus dispositivos cadastrados são: {}".format(users[message.from_user.id]))
    print(users.keys())

@bot.message_handler(commands=['quit'])
def at_answer(message):
    users[message.from_user.id] = []
    bot.reply_to(message, "ok!")
    print(users[message.from_user.id])

# loop eterno
while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)
