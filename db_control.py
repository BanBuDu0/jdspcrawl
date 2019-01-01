import pymongo
import sys
import spir


class Item:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.price = 0
        self.seller = ''
        # self.img = ''


def connectDB():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['spider']
    col = db['spider']
    return col


def insert(d: Item):
    connectDB().insert_one(d.__dict__)


def finddata():
    cn = connectDB()
    data1 = cn.find({}, {'_id': 0})
    for i in data1:
        yield i


def best():
    i = finddata()
    next(i)
    return next(i)

def minPrice():
    i = finddata()
    row = next(i)
    while True:
        try:
            temp = next(i)
            if temp["price"] < row["price"]:
                row = temp
        except StopIteration:
            return row


def showall():
    i = finddata()
    while True:
        try:
            print(next(i))
        except StopIteration:
            sys.exit()


def insertList():
    goods = '电脑'
    url = 'http://search.jd.com/Search?keyword={}&enc=utf-8'.format(goods)
    r = spir.getHTML(url)
    for i in range(30):
        item = Item()
        item = spir.crawl(r, item, i)
        j = item.name.find('<')
        while j != -1:
            rear = item.name.find('>') + 1
            item.name = item.name[: j] + item.name[rear:]
            j = item.name.find('<')
        insert(item)


if __name__ == '__main__':
    # insertList()
    showall()
