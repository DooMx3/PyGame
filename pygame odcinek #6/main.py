import pygame
from math import floor

pygame.init()
window = pygame.display.set_mode((1280, 720))


class Physic:
    def __init__(self, x, y, width, height, acc, max_vel):
        self.x_cord = x  # współrzędna x
        self.y_cord = y  # współrzędna y
        self.hor_velocity = 0  # prędkość w poziomie
        self.ver_velocity = 0  # prędkość w pionie
        self.acc = acc  # przyspieszenie
        self.max_vel = max_vel  # maksymalna prędkość
        self.width = width  # szerokość
        self.height = height  # wysokość
        self.previous_x = x
        self.previous_y = y
        self.jumping = False  # czy skacze
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def physic_tick(self, beams):
        self.ver_velocity += 0.7
        self.x_cord += self.hor_velocity
        self.y_cord += self.ver_velocity
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)  # odświeżanie hitboxa
        for beam in beams:
            if beam.hitbox.colliderect(self.hitbox):  # cofanie obiektu do miejsca z poprzedniej klatki
                if self.x_cord + self.width >= beam.x_cord + 1 > self.previous_x + self.width:  # kolizja z prawej strony
                    self.x_cord = self.previous_x
                    self.hor_velocity = 0
                if self.x_cord <= beam.x_cord + beam.width - 1 < self.previous_x:  # kolizja z lewej strony
                    self.x_cord = self.previous_x
                    self.hor_velocity = 0
                if self.y_cord + self.height >= beam.y_cord + 1 > self.previous_y + self.height:  # kolizja z dołu
                    self.y_cord = self.previous_y
                    self.ver_velocity = 0
                    self.jumping = False
                if self.y_cord <= beam.x_cord + beam.width - 1 < self.previous_y:  # kolizja z góry
                    self.y_cord = self.previous_y
                    self.ver_velocity = 0

        self.previous_x = self.x_cord
        self.previous_y = self.y_cord


class Player(Physic):
    def __init__(self):
        self.stand_img = pygame.image.load('John/stand.png')  # normalna grafika
        width = self.stand_img.get_width()  # szerokość
        height = self.stand_img.get_height()  # wysokość
        super().__init__(0, 540, width, height, 0.5, 5)
        self.jump_img = pygame.image.load('John/jump.png')  # grafika skoku
        self.walk_right_img = [pygame.image.load(f'John/walk/klatka0{x}.png') for x in range(1, 7)]  # animacja chodzenia
        self.walk_left_img = [pygame.transform.flip(pygame.image.load(f'John/walk/klatka0{x}.png'), True, False) for x in range(1, 7)]
        self.walk_index = 0

    def tick(self, keys, beams):  # wykonuje się raz na powtórzenie pętli
        self.physic_tick(beams)
        if keys[pygame.K_a] and self.hor_velocity > self.max_vel * -1:
            self.hor_velocity -= self.acc
        if keys[pygame.K_d] and self.hor_velocity < self.max_vel:
            self.hor_velocity += self.acc
        if keys[pygame.K_SPACE] and self.jumping is False:
            self.ver_velocity -= 15
            self.jumping = True
        if not (keys[pygame.K_d] or keys[pygame.K_a]):
            if self.hor_velocity > 0:
                self.hor_velocity -= self.acc
            elif self.hor_velocity < 0:
                self.hor_velocity += self.acc

    def draw(self):
        if self.jumping:
            window.blit(self.jump_img, (self.x_cord, self.y_cord))
        elif self.hor_velocity != 0:
            if self.hor_velocity > 0:
                window.blit(self.walk_right_img[floor(self.walk_index)], (self.x_cord, self.y_cord))
            elif self.hor_velocity < 0:
                window.blit(self.walk_left_img[floor(self.walk_index)], (self.x_cord, self.y_cord))
            self.walk_index += 0.4
            if self.walk_index > 5:
                self.walk_index = 0
        else:
            window.blit(self.stand_img, (self.x_cord, self.y_cord))


class Beam:
    def __init__(self, x, y, width, height):
        self.x_cord = x
        self.y_cord = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, (128, 128, 128), self.hitbox)


def main():
    run = True
    player = Player()
    clock = 0
    background = pygame.image.load("polana.png")
    beams = [
        Beam(10, 650, 1000, 40),
        Beam(600, 550, 20, 100),
    ]
    while run:
        clock += pygame.time.Clock().tick(60) / 1000  # maksymalnie 60 fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # jeśli gracz zamknie okienko
                run = False
        keys = pygame.key.get_pressed()

        player.tick(keys, beams)

        window.blit(background, (0, 0))  # rysowanie tła

        player.draw()
        for beam in beams:
            beam.draw(window)
        pygame.display.update()


if __name__ == "__main__":
    main()
