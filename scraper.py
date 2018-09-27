import bs4 as bs
import urllib2 as ur
from multiprocessing import Pool as ThreadPool
import csv
import codecs
import time

def page_getter(url):
    pages = []
    req = ur.Request(url, headers={'User-Agent':'Magic Browser'})
    sauce = ur.urlopen(req).read()
    soup = bs.BeautifulSoup(sauce,'lxml')
    links = soup.find('div',class_='arrange arrange--baseline')
    for link in links:
        try:
            anchor = link.find('a').get('href')
            pages.append(url)
            pages.append('https://www.yelp.com' + anchor)
        except:
            pass
    print 'Page Retrieval completed'

    return pages
def rest_getter(url):
    res = []
    for i in url:
        req = ur.Request(i, headers={'User-Agent':'Magic Browser'})
        sauce = ur.urlopen(req).read()
        soup = bs.BeautifulSoup(sauce,'lxml')
        links = soup.find_all('a',class_='biz-name js-analytics-click')
        for link in links:
            res.append('https://www.yelp.com' + link.get('href'))
    print 'Restaraunt retrieval completed'
    return res
def rest_info(url):
    req = ur.Request(url, headers={'User-Agent':'Magic Browser'})
    sauce = ur.urlopen(req).read()
    soup = bs.BeautifulSoup(sauce,'lxml')
    try:
        title = soup.find('h1',class_='biz-page-title embossed-text-white shortenough').text.strip()
        address = soup.find('address').text.strip()
        with codecs.open(r'Info/Restaraunts.csv','a',encoding='utf-8') as f:
            fieldnames = ['Name','Address','Url']
            thewriter = csv.DictWriter(f,fieldnames)
            thewriter.writerow({'Name': title, 'Address': address,'Url': url})
    except:
        pass

def main():
    print 'Running.....'
    beg_time = time.time()
    with open(r'Info/Restaraunts.csv','w+') as f:
        fieldnames=['Name','Address','Url']
        thewriter = csv.DictWriter(f, fieldnames)
        thewriter.writeheader()

    pages = page_getter('https://www.yelp.com/search?cflt=restaurants&find_loc=San+Francisco%2C+CA')
    restaraunts = rest_getter(pages)
    pool = ThreadPool(4)
    print 'Parse has begun'
    results = pool.map(rest_info,restaraunts)
    pool.close()
    pool.join()
    print 'Parse has been completed'
    print '--------------Time taken is',time.time()-beg_time,' Seconds-----------'
if __name__== '__main__':
    main()
