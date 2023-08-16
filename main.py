import requests
import time

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
BOT_TOKEN = '6540646281:AAH59RuDybvhwJJPimQ_gSxReJZ-3NHMq5Q'
# Замените 'SOURCE_CHANNEL_ID' на ID канала, с которого нужно переписывать посты
SOURCE_CHANNEL_ID = '@-1001737811659'
# Замените 'DESTINATION_CHANNEL_ID' на ID вашего канала, на который нужно пересылать посты
DESTINATION_CHANNEL_ID = '@-1001171121404'

# Простая функция замены слов в тексте
def replace_words(text):
    replacements = {
        'кот': 'собака',
        'машина': 'велосипед',
        'дом': 'замок'
        # Добавьте свои замены по желанию
    }
    
    for word, replacement in replacements.items():
        text = text.replace(word, replacement)
    
    return text

def get_updates(offset=None):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'
    params = {'offset': offset}
    response = requests.get(url, params=params)
    return response.json()

def send_text_message(chat_id, text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    params = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, params=params)
    return response.json()

def send_photo_message(chat_id, file_id, caption=''):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
    params = {'chat_id': chat_id, 'photo': file_id, 'caption': caption}
    response = requests.post(url, params=params)
    return response.json()

def forward_post(source_message_id):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/forwardMessage'
    params = {'chat_id': DESTINATION_CHANNEL_ID, 'from_chat_id': SOURCE_CHANNEL_ID, 'message_id': source_message_id}
    response = requests.post(url, params=params)
    return response.json()

def main():
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates['result']:
            if 'message' in update and 'text' in update['message']:
                text = update['message']['text']
                replaced_text = replace_words(text)  # Заменяем слова в тексте
                send_text_message(DESTINATION_CHANNEL_ID, replaced_text)  # Отправляем измененный текст на ваш канал
            if 'message' in update and 'forward_from_chat' in update['message']:
                source_message_id = update['message']['forward_from_message_id']
                forwarded_message = update['message']['forward_from_message']
                if 'photo' in forwarded_message:
                    photo = forwarded_message['photo'][-1]
                    photo_id = photo['file_id']
                    caption = forwarded_message.get('caption', '')
                    send_photo_message(DESTINATION_CHANNEL_ID, photo_id, caption)  # Отправляем фото на ваш канал
                forward_post(source_message_id)  # Переписываем пост на ваш канал
            offset = update['update_id'] + 1
        time.sleep(1)

if __name__ == '__main__':
    main()
