import requests
import bs4
import os


def add_in_file(title):
    print("In add_in_file()")
    try:
        with open('index.txt', 'a') as index:
            index.seek(0)
            index.writelines(title + "\n")
            print("Title Added Successfully")
    except Exception as e:
        print("Error in index adding: ", e)


def search_in_file(title):
    
    print("In search_in_file()")
    try:
        if title in open('Songs/index.txt', 'r').read():
            return True
        else:
            return False
    except Exception as e:
        print("Error in index searching : ", e)


def top(time):
    url = 'http://mymp3song.guru/topdownload/' + time
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    req = requests.get(url, headers=headers)
    # req = requests.get(url)
    bs = bs4.BeautifulSoup(req.text, 'lxml')
    print(bs)
    link = bs.select('.fileName')
    for i in link:
        print("In top() for")
        url = "http://mymp3song.guru" + i.get('href')
        title = url.split("/")
        name = title[-1].strip() + ".mp3"
        print("\nSong Name : {}".format(name))
        print("Song Page Link : {}".format(url))
        if search_in_file(name):
            print("Already Downloaded")
        else:
            song_page(url, name)
    print(url)


def song_page(url, name):
    print("In song_page()")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    req = requests.get(url, headers=headers)
    # req = requests.get(url)
    bs = bs4.BeautifulSoup(req.text, 'lxml')
    link = bs.select('.dwnLink2')
    if len(link) == 0:
        link = bs.select('.dwnLink4')
    if len(link) == 0:
        link = bs.select('.dwnLink')
    for i in link:
        url = "http://mymp3song.guru" + i.get('href')
        print("Download Link : {}".format(url))
        song_download(url, name)
    print("")


def song_download(url, name):
    print("In song_download()")
    if not os.path.exists("Songs"):
        os.mkdir('Songs')
        os.chdir('Songs')
    else:
        os.chdir('Songs')
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        req = requests.get(url, headers=headers)
        # req = requests.get(url, stream=True)
        with open(name + ".mp3", "wb") as f:
            f.write(req.content)
            print("Downloaded Successfully")
            add_in_file(name)
    except Exception as e:
        print("Error in download", e)
    finally:
        os.chdir('../')


def setup():
    print("In setup()")
    file_path = "Songs/"
    directory = os.path.dirname(file_path)
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    file_path = "Songs/index.txt"
    if(not os.path.exists(file_path)):
        open(file_path,'w')


setup();
top('today')
top('all')
