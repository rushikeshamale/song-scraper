import requests
import bs4
import os


def add_in_file(title):
    try:
        with open('index.txt', 'a') as index:
            index.seek(0)
            index.writelines(title + "\n")
            print("Title Added Successfully")
    except Exception as e:
        print("Error in index adding: ", e)


def search_in_file(title):
    try:
        if title in open('Songs/index.txt', 'r').read():
            return True
        else:
            return False
    except Exception as e:
        print("Error in index searching : ", e)


def top(time):
    url = 'http://mymp3song.site/topdownload/' + time
    req = requests.get(url)
    bs = bs4.BeautifulSoup(req.text, 'lxml')
    link = bs.select('.fileName')
    for i in link:
        url = "http://mymp3song.site" + i.get('href')
        title = url.split("/")
        name = title[-1].strip() + ".mp3"
        print("\nSong Name : {}".format(name))
        print("Song Page Link : {}".format(url))
        if search_in_file(name):
            print("Already Downloaded")
        else:
            song_page(url, name)


def song_page(url, name):
    req = requests.get(url)
    bs = bs4.BeautifulSoup(req.text, 'lxml')
    link = bs.select('.dwnLink2')
    if len(link) == 0:
        link = bs.select('.dwnLink4')
    if len(link) == 0:
        link = bs.select('.dwnLink')
    for i in link:
        url = "http://mymp3song.site" + i.get('href')
        print("Download Link : {}".format(url))
        song_download(url, name)
    print("")


def song_download(url, name):
    if not os.path.exists("Songs"):
        os.mkdir('Songs')
        os.chdir('Songs')
    else:
        os.chdir('Songs')
    try:
        req = requests.get(url, stream=True)
        with open(name + ".mp3", "wb") as f:
            f.write(req.content)
            print("Downloaded Successfully")
            add_in_file(name)
    except Exception as e:
        print("Error in download", e)
    finally:
        os.chdir('../')


top('today')
top('yesterday')
top('week')
top('month')
top('all')
