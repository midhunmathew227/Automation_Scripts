import requests

def telegram_bot(bot_message):
    bot_token = '5119253303:AAFacw7KuJCK1dMxGtA9CWLE9I8dvcQeRqE'
    bot_chat_id = '422860978'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chat_id + \
        '&parse_mode=MarkdownV2&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

telegram_bot("Hello, User")


#Notes:
# 1. Create a new bot from @BotFather
# 2. Notedown the bot_token you get from @BotFather
# 3. Send a message to the new generated bot
# 4. Go to this URL
#    https://api.telegram.org/bot<bot_token>/getUpdates
# 5. Notedown the chat_id
# 6. All Set.
