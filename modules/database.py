from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.music_auto
def insertStuff():
    score = db.score
    data = {
        'name':'Beethoven5',
        'pages':['page1', 'page2', 'page3']
    }
    result = score.insert_one(data)
    print('One post: {0}'.format(result.inserted_id))


if __name__ == '__main__':
    insertStuff()