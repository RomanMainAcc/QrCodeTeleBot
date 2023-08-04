import telebot
import pyqrcode
import config
import requests
from PIL import Image
from pyzbar.pyzbar import decode
from io import BytesIO

bot = telebot.TeleBot(config.TOKEN)


def download_file_to_pillow(file_id: str) -> Image.Image:
    qr_code_info = bot.get_file(file_id)
    qr_code_url = f"https://api.telegram.org/file/bot{config.TOKEN}/{qr_code_info.file_path}"

    response = requests.get(qr_code_url)
    response.raise_for_status()

    buffer = BytesIO(response.content)

    return Image.open(buffer)


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
    qr_code_img = download_file_to_pillow(photo_id)

    decoded_objects = decode(qr_code_img)

    if decoded_objects:
        qr_text = decoded_objects[0].data.decode('utf-8')
        bot.reply_to(message, f'Text encoded in a QR code: {qr_text}')
    else:
        bot.reply_to(message, "QR code was not recognized or image not found.")


if __name__ == "__main__":
    bot.polling(none_stop=True)
