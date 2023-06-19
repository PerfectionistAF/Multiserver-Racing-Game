from pygame import sprite, image, transform, Color

from Protocols import GameSnapshot, COLORS


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
        self.color = Color(COLORS[self.id])

    def update(self, input: GameSnapshot) -> None:
        x, y, deg, score = input[self.id]
        if deg != self.deg:
            self.deg = deg
            self.image = transform.rotate(self.sprite, deg)
            self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.score = score
