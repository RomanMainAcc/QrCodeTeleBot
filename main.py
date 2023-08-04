import telebot
import pyqrcode
import os
from PIL import Image
from pyzbar.pyzbar import decode
from io import BytesIO

bot = telebot.TeleBot(os.environ['TOKEN'])


def get_file_binary(file_id: str) -> bytes:
    file_info = bot.get_file(file_id)
    file_binary = bot.download_file(file_info.file_path)

    return file_binary


@bot.message_handler(commands=['start', 'help'])
def starter(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id, "Hello, send me the text and I will generate a qr code")


@bot.message_handler(content_types=['text'])
def text_to_qr(message: telebot.types.Message) -> None:
    qr_code = pyqrcode.create(message.text)
    buffer = BytesIO()
    qr_code.png(buffer, scale=6)
    buffer.seek(0)
    bot.send_photo(message.chat.id, photo=buffer)


@bot.message_handler(content_types=['photo'])
def qr_to_text(message: telebot.types.Message) -> None:
    photo_id = message.photo[-1].file_id
    qr_code_binary = get_file_binary(photo_id)

    qr_code_img = Image.open(BytesIO(qr_code_binary))

    decoded_objects = decode(qr_code_img)

    if decoded_objects:
        qr_text = decoded_objects[0].data.decode('utf-8')
        bot.reply_to(message, f'Text encoded in a QR code: {qr_text}')
    else:
        bot.reply_to(message, "QR code was not recognized or image not found.")


if __name__ == "__main__":
    bot.polling(none_stop=True)
