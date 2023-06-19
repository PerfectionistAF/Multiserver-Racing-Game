from pygame import sprite, image, transform
import requests
from Protocols import GameSnapshot
import sqlite3

class Player(sprite.Sprite):
    def __init__(self, id: int) -> None:
        sprite.Sprite.__init__(self)
        self.id = id
        self.sprite = image.load('./Sprites/Car' + str(self.id) + '.png').convert()
        self.sprite = transform.scale(self.sprite, (20, 20))
        self.image = self.sprite
        self.rect = self.image.get_rect()
        self.deg = 0
        self.score = 0

    def update(self, input: GameSnapshot) -> None:
        x, y, deg, score = input[self.id]
        if deg != self.deg:
            self.deg = deg
            self.image = transform.rotate(self.sprite, deg)
            self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.score = score
        #SQLITE 3 DB
        db = sqlite3.connect('update.sqlite')
        db.execute('CREATE TABLE IF NOT EXISTS Client_Players(Server_ID INTEGER, Client_ID INTEGER, X INTEGER, Y INTEGER, DEGREE INTEGER)')
        db.execute("INSERT INTO Client_Players(Server_ID, Client_ID, X, Y, DEGREE) VALUES('1'", self.id.get(), x.get(), y.get(), deg.get())
        db.connection.commit()
        db.close()

        #request data from server
        #dnsUrl = "firrehab.org"
        '''runserverUrl = "http://127.0.0.1:8000/"
        r = requests.get(url=runserverUrl)#url = dnsUrl)
        data = r.json()
        #first 5 results per instance
        for i in range(5):
            x = data['results'][i]
            y = data['results'][i]
            deg = data['results'][i]
            score = data['results'][i]
            print("X_COORD:", x, "\n")
            print("Y_COORD:", y, "\n")
            print("DEGREE:", deg, "\n")
            print("SCORE:", score, "\n")'''
  
         


