import pygame
from math import floor
from random import randint

resolution = (1280, 720)


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


class Button:
    def __init__(self, x_cord, y_cord, file_name):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.button_image = pygame.image.load(f"{file_name}.png")
        self.hovered_button_image = pygame.image.load(f"{file_name}_hovered.png")
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.button_image.get_width(), self.button_image.get_height())

    def tick(self):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                return True

    def draw(self, window):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            window.blit(self.hovered_button_image, (self.x_cord, self.y_cord))
        else:
            window.blit(self.button_image, (self.x_cord, self.y_cord))


class Player(Physic):
    def __init__(self):
        self.stand_right_img = pygame.image.load('John/stand.png')  # normalna grafika
        self.stand_left_img = pygame.transform.flip(pygame.image.load('John/stand.png'), True, False)
        width = self.stand_right_img.get_width()  # szerokość
        height = self.stand_right_img.get_height()  # wysokość
        super().__init__(0, 540, width, height, 0.5, 5)
        self.jump_right_img = pygame.image.load('John/jump.png')  # grafika skoku
        self.jump_left_img = pygame.transform.flip(pygame.image.load('John/jump.png'), True, False)  # grafika skoku
        self.walk_right_img = [pygame.image.load(f'John/walk/klatka0{x}.png') for x in range(1, 7)]  # animacja chodzenia
        self.walk_left_img = [pygame.transform.flip(pygame.image.load(f'John/walk/klatka0{x}.png'), True, False) for x in range(1, 7)]  # animacja chodzenia
        self.walk_index = 0
        self.direction = 1

    def tick(self, keys, beams):  # wykonuje się raz na powtórzenie pętli
        self.physic_tick(beams)
        if keys[pygame.K_a] and self.hor_velocity > self.max_vel * -1:
            self.hor_velocity -= self.acc
        if keys[pygame.K_d] and self.hor_velocity < self.max_vel:
            self.hor_velocity += self.acc
        if keys[pygame.K_SPACE] and self.jumping is False:
            self.ver_velocity -= 15
            self.jumping = True
        if self.hor_velocity > 0:
            self.direction = 1
        elif self.hor_velocity < 0:
            self.direction = 0
        if not (keys[pygame.K_d] or keys[pygame.K_a]):
            if self.hor_velocity > 0:
                self.hor_velocity -= self.acc
            elif self.hor_velocity < 0:
                self.hor_velocity += self.acc

    def draw(self, win, background_width):
        if background_width - resolution[0] / 2 > self.x_cord >= resolution[0] / 2:
            x_screen = resolution[0] / 2
        elif self.x_cord >= background_width - resolution[0] / 2:
            x_screen = self.x_cord - background_width + resolution[0]
        else:
            x_screen = self.x_cord

        if self.jumping:
            if self.direction == 0:
                win.blit(self.jump_left_img, (x_screen, self.y_cord))
            elif self.direction == 1:
                win.blit(self.jump_right_img, (x_screen, self.y_cord))
        elif self.hor_velocity != 0:
            if self.direction == 0:
                win.blit(self.walk_left_img[floor(self.walk_index)], (x_screen, self.y_cord))
            elif self.direction == 1:
                win.blit(self.walk_right_img[floor(self.walk_index)], (x_screen, self.y_cord))
            self.walk_index += 0.4
            if self.walk_index > 5:
                self.walk_index = 0
        else:
            if self.direction == 0:
                win.blit(self.stand_left_img, (x_screen, self.y_cord))
            elif self.direction == 1:
                win.blit(self.stand_right_img, (x_screen, self.y_cord))


class Beam:
    def __init__(self, x, y, width, height):
        self.x_cord = x
        self.y_cord = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self, win, background_x):
        pygame.draw.rect(win, (200, 200, 200), (self.x_cord + background_x, self.y_cord, self.width, self.height))


class Background:
    def __init__(self):
        self.x_cord = 0
        self.y_cord = 0
        self.image = pygame.image.load("las.png")
        self.width = self.image.get_width()

    def tick(self, player):
        if self.width - resolution[0] / 2 > player.x_cord >= resolution[0] / 2:
            self.x_cord = -player.x_cord + resolution[0] / 2
        elif player.x_cord >= self.width - resolution[0] / 2:
            self.x_cord = - self.width + resolution[0]
        else:
            self.x_cord = 0

    def draw(self, win):
        win.blit(self.image, (self.x_cord, self.y_cord))