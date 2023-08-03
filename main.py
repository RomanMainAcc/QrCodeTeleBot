import telebot
import pyqrcode
from PIL import Image
from pyzbar.pyzbar import decode

bot = telebot.TeleBot('6046831990:AAGMjVSRxnL_WX9IdfVcMLgjyoUcIjmSBYg')

qr_code_filename = 'qr_code.png'


@bot.message_handler(commands=['start', 'help'])
def starter(message):
    bot.send_message(message.chat.id, "Hello, send me the text and I will generate a qr code")


@bot.message_handler(content_types=['text'])
def text_to_qr(message):
    qr_code = pyqrcode.create(message.text)
    qr_code.png(qr_code_filename, scale=6)

    with open(qr_code_filename, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(content_types=['photo'])
def qr_to_text(message):
    photo = message.photo[-1].file_id
    qr_code_info = bot.get_file(photo)
    qr_code_file = bot.download_file(qr_code_info.file_path)

    with open(qr_code_filename, 'wb') as file:
        file.write(qr_code_file)

    decoded_objects = decode(Image.open(qr_code_filename))

    if decoded_objects:
        qr_text = decoded_objects[0].data.decode('utf-8')
        bot.reply_to(message, f'Text encoded in a QR code: {qr_text}')
    else:
        bot.reply_to(message, "QR code was not recognized or image not found.")


bot.polling(none_stop=True)
