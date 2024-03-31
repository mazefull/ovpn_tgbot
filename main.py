import paramiko
import os
import telebot
import json
import random
import time

auto_restart = True

with open("credentials.json", "r", encoding="utf-8") as fh:
    data= json.load(fh)


host = data["vps"]["host"] #ip
user = data["vps"]["user"] #login
secret = data["vps"]["secret"] #pswd
port = data["vps"]["port"]
bot_api = data["tbot"]["API"]
admin_id = data["tbot"]["admin_id"]

bot = telebot.TeleBot(bot_api)

def newvpn(client_name):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)
    comm = f'MENU_OPTION="1" CLIENT="{client_name}" PASS="1" ./openvpn-install.sh'
    stdin, stdout, stderr = client.exec_command(comm)
    data = stdout.read() + stderr.read()
    print(data)
    client.close()
    getprofile(client_name)

def getprofile(client_name):
    if os.path.exists('ovpn_profiles'):
        pass
    else:
        os.system('mkdir ovpn_profiles')
    transport = paramiko.Transport((host, port))
    transport.connect(username=user, password=secret)
    sftp = paramiko.SFTPClient.from_transport(transport)
    remotepath = f'{client_name}.ovpn'
    localpath = f'ovpn_profiles\{client_name}.ovpn'
    sftp.get(remotepath, localpath)
    sftp.close()
    transport.close()

def check_id(userid):
    return str(userid) == admin_id


@bot.message_handler(commands=['start'])
def start_message(message):
    if check_id(message.chat.id) is True:
        profile_name = random.randint(1,165)
        newvpn(str(profile_name))
        file_to_send = open(f"ovpn_profiles\{profile_name}.ovpn")
        bot.send_document(message.chat.id, file_to_send)
    else:
        pass


def run():
    print(f' Пытаемся перезапуститься')
    os.system('C:\\Users\\*****\\venv\\Scripts\\python.exe C:\\Users\\*****\\main.py')

def texept():
    if auto_restart == True:
        try:
            bot.enable_save_next_step_handlers(delay=2)
            bot.load_next_step_handlers()
            bot.polling(none_stop=True)
        except:
            print('Отправляем Alert в ПУ mazefull')
            try:
                bot.send_message(admin_id, f"Падение bot.polling .\n Инициирован перезапуск")
            except:
                print(f'Невозможно отправить Alert в ПУ')
            print('Ждём 5 секунд')
            time.sleep(5)
            run()
    else:
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.polling(none_stop=True)

texept()
