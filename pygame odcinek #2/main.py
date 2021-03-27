import pygame
from random import randint

pygame.init()
window = pygame.display.set_mode((1280, 720))


class Player:
    def __init__(self):
        self.x_cord = 0  # współrzędna x
        self.y_cord = 0  # współrzędna y
        self.image = pygame.image.load("gracz.png")  # wczytuje grafikę
        self.width = self.image.get_width()  # szerokość
        self.height = self.image.get_height()  # wysokość
        self.speed = 4  # prędkość
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def tick(self, keys):  # wykonuje się raz na powtórzenie pętli
        if keys[pygame.K_w]:
            self.y_cord -= self.speed
        if keys[pygame.K_a]:
            self.x_cord -= self.speed
        if keys[pygame.K_s]:
            self.y_cord += self.speed
        if keys[pygame.K_d]:
            self.x_cord += self.speed

        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self):
        window.blit(self.image, (self.x_cord, self.y_cord))


class Cash:
    def __init__(self):
        self.x_cord = randint(0, 1280)
        self.y_cord = randint(0, 720)
        self.image = pygame.image.load("banknot.png")
        self.width = self.image.get_width()  # szerokość
        self.height = self.image.get_height()  # wysokość
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def tick(self):
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self):
        window.blit(self.image, (self.x_cord, self.y_cord))


def main():
    run = True
    player = Player()
    clock = 0
    score = 0
    banknotes = []
    background = pygame.image.load("tło.png")
    while run:
        clock += pygame.time.Clock().tick(60) / 1000  # maksymalnie 60 fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # jeśli gracz zamknie okienko
                run = False
        keys = pygame.key.get_pressed()
        if clock >= 2:
            clock = 0
            banknotes.append(Cash())

        player.tick(keys)
        for banknote in banknotes:
            banknote.tick()

        for banknote in banknotes:
            if player.hitbox.colliderect(banknote.hitbox):
                banknotes.remove(banknote)
                score += 1

        window.blit(background, (0, 0))  # rysowanie tła
        player.draw()
        for banknote in banknotes:
            banknote.draw()
        pygame.display.update()

    print(score)


if __name__ == "__main__":
    main()
