import os
import errno
import requests
from pathlib import Path
from urllib.parse import urlparse, unquote


payload = {'start_date': '2022-04-01',
            'end_date': '2022-04-01', #Взял интервал по одному дню
            'api_key': 'ql1pnWkzzifmIEKTQkbLse2beYOMOToFbmNYCYQL'}

url_apod = 'https://api.nasa.gov/planetary/apod'

url_epic = 'https://api.nasa.gov/EPIC/api/natural?api_key=ql1pnWkzzifmIEKTQkbLse2beYOMOToFbmNYCYQL'


def get_extension(url):
    ext = (
        os.path.splitext(
            os.path.split(
                urlparse(
                    unquote(url)
                ).path
            )[-1]
        )[-1]
    )[1:]
    return ext


def download_img_to_folder(url, path, n):
    filename = f'{path}/spacex{n}.{get_extension(url)}'
    response = requests.get(url)
    response.raise_for_status()
    if not os.path.exists(path):
        try:
            path.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            if error.errno != errno.EEXIST:
                raise
    with open(filename, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch(list_of_links, path):
    for n, link in enumerate(list_of_links, start=1):
        download_img_to_folder(link, path, n)


def list_of_apod(url, payload):
    response = requests.get(url, params=payload)
    response.raise_for_status()
    list_of_links = []
    for apod in response.json():
        list_of_links.append(apod.get('url'))
    return list_of_links


def list_of_epic(url):
    response = requests.get(url)
    response.raise_for_status()
    list_of_epic = []
    for i in response.json():
        y = i['date'][:4]
        m = i['date'][5:7]
        d = i['date'][8:10]
        img = i['image']
        list_of_epic.append(
            f'https://api.nasa.gov/EPIC/archive/natural/{y}/{m}/{d}/png/{img}.png?api_key=DEMO_KEY'
        )
    lists = list_of_epic[:1] #Взял срез по первому элементу списка
    return lists


def main():
    path_for_apod = Path('./images/apod')
    path_for_epic = Path('./images/epic')
    
    for n, link in enumerate(list_of_apod(url_apod, payload), start=1):
        fetch_spacex_last_launch(
            list_of_apod(url_apod, payload),
            path_for_apod
        )
    
    for n, link in enumerate(list_of_epic(url_epic), start=1):
        fetch_spacex_last_launch(
            list_of_epic(url_epic),
            path_for_epic
        )
    

if __name__ == '__main__':
    main()
