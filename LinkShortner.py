import requests

def getShortUrl(url):
    apiurl = "https://miniurl.io/api?api=a4bf1fee8f898fea3b542f1130def4d5467d14ec&url=%s&format=text" %url
    return  (str(requests.request('GET', apiurl).text))

if __name__ == '__main__':
    print(getShortUrl("www.facebook.com"))