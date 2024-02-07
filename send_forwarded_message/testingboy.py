from pprint import pprint

from quart import Quart, request, jsonify
from telegram import Bot
import tracemalloc
import asyncio

app = Quart(__name__)

# Replace 'YOUR_GROUP_CHAT_ID' with the chat ID of your group.
group_chat_id = '-100sslslls'
# bot token from bot father
bot = "Token"


@app.route('/webhook', methods=['POST'])
async def webhook():
    data = await request.get_json()
    if 'message' in data:
        message = data['message']
        chat_id = message['chat']['id']
        bot_type = message['chat']['type']
        text = message.get('text', '')

        if bot_type != 'supergroup':
            if 'document' in message:
                document = message['document']['file_id']
                await bot.send_document(chat_id=group_chat_id, document=document, caption=f'{text}')
            elif 'video' in message:
                video = message['video']['file_id']
                await bot.send_video(chat_id=group_chat_id, video=video, caption=f'{text}')
            elif 'photo' in message:
                photo = message['photo'][-1][
                    'file_id']  # Use the last element in the 'photo' array for the highest resolution
                await bot.send_photo(chat_id=group_chat_id, photo=photo, caption=f'{text}')
            elif 'audio' in message:
                audio = message['audio']['file_id']
                await bot.send_audio(chat_id=group_chat_id, audio=audio, caption=f'{text}')
            else:
                # Handle other types of messages (e.g., text)
                await bot.send_message(chat_id=group_chat_id, text=f'{text}')

    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    asyncio.run(app.run_task())
    tracemalloc.start()
