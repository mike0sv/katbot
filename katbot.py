import json
import re
import time

import bs4
import requests
import telepot
import heroku

heroku.app.run(port=80w)

token = open('token', 'r').read().strip()
bot = telepot.Bot(token)

search_url = 'http://kat.cr/search'
sorting_param = '/?field=seeders&order=desc'


def get_first_magnet(query):
    query = re.sub('/', '', query)  # TODO parsing
    res = requests.get(search_url + '/' + query + sorting_param)
    soup = bs4.BeautifulSoup(res.content, 'lxml')
    table = soup.find('table', {'id': 'mainSearchTable'}).find('table', {'class': 'data'}).find_all('tr')
    for tr in table:
        if 'id' in tr.attrs and tr.attrs['id'].startswith('torrent'):
            name_tag = tr.find('div', {'class': 'none'})
            params = json.loads(re.sub("'", '"', name_tag.attrs['data-sc-params']))
            name = re.sub('\%20', ' ', params['name'])  # TODO decoding

            magnet = tr.find('a', {'title': 'Torrent magnet link'}).attrs['href']
            link = 'https:' + tr.find('a', {'title': 'Download torrent file'}).attrs['href']
            try:
                link = link.split('?')[0]
            except:
                pass
            return name, link, magnet


def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        try:
            for out in get_first_magnet(msg['text']):
                bot.sendMessage(chat_id, out)
        except:
            # TODO send error message
            raise


def main():
    bot.message_loop(handle_message)
    while 1:
        time.sleep(10)


if __name__ == '__main__':
    main()
