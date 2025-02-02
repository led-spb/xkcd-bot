import os
import requests
import schedule
bot_token = os.environ.get('BOT_TOKEN')


def heres():
    req = requests.get("https://xkcd.ru/random", verify=True)
    print(req.url)

    content = req.text
    start = content.find('<img border=0 src="') + len('<img border=0 src="')
    end = content.find('"', start)

    start_text = content.find('<div class="comics_text">')+len('<div class="comics_text">')
    end_text = content.find('<', start_text)


    picture_url = content[start:end]
    print(picture_url)
    message_url = content[start_text:end_text]
    req1 = requests.get(picture_url, verify=True)
    return [req1.content, message_url]


def send_text(id, text):
    message = {
        'chat_id': id,
        'text': text,
    }
    res = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage", data=message
    )
    #res.raise_for_status()
    print(res.text)


def get_udates(offset):
    res = requests.get(f"https://api.telegram.org/bot{bot_token}/getUpdates",
                       {'offset': offset, 'timeout': 60}
    )
    res.raise_for_status()
    return res.json()



def send_photo(id):
    con = heres()
    photo = con[0]
    text = con[1]
    message = {
        'chat_id': id,
        'caption': text
    }

    res = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendPhoto", data=message, files={'photo': photo}
    )
    #res.raise_for_status()s
    print(res.text)

last_update_id = 0
while True:
    updates = get_udates(last_update_id+1)
    updates = updates['result']

    if len(updates) > 0:
        for i in updates:
            last_update_id = i['update_id']
        message = i['message']['text']
        id = i['message']['chat']['id']
        if(message == '/send'):
            send_photo(id)
    #    send_photo()

#schedule.every().day.at("07:30").do(send_photo)
#schedule.every().day.at("18:56").do(send_photo)#
#schedule.every().day.at("20:00").do(send_photo)
#while True:
#    schedule.run_pending()
