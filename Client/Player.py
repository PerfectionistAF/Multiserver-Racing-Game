from pygame import sprite, image, transform
from Protocols import GameSnapshot

class Player(sprite.Sprite):
    def __init__(self, id:int) -> None:
        sprite.Sprite.__init__(self)
        self.id = id
        self.sprite = image.load("./Sprites/Car"+str(self.id)+".png").convert()
        self.sprite = transform.scale(self.sprite, (20,20))
        self.image = self.sprite
        self.rect = self.image.get_rect()
        self.deg:int = 0

    def update(self, input : GameSnapshot) -> None:
        x,y,deg = input[self.id]
        if deg != self.deg:
            self.deg = deg
            self.image = transform.rotate(self.sprite, deg)
            self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
