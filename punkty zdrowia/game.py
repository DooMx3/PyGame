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
        self.gravity = 0.7

    def physic_tick(self, beams):
        self.ver_velocity += self.gravity
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


class Health:
    def __init__(self, max_health=100):
        self.health = max_health
        self.max_health = max_health  # ilość punktów życia
        self.alive = True  # czy obiekt żyje
        self.last_dmg = 0  # czas od ostatnich obrażeń

    def health_tick(self, delta_tm):
        self.last_dmg += delta_tm

    def dealt_damage(self, damage, hit_speed):
        if self.last_dmg > hit_speed:
            self.health -= damage
            self.last_dmg = 0
            if self.health <= 0:
                self.health = 0
                self.alive = False

    def draw_health(self, win, x, y, max_width, height):
        percent_width = self.health / self.max_health
        width = round(max_width * percent_width)
        if self.health > 30:
            color = (30, 255, 30)
        else:
            color = (255, 30, 30)
        pygame.draw.rect(win, (30, 30, 30), (x, y, max_width, height))
        pygame.draw.rect(win, color, (x, y, width, height))


class Button:
    def __init__(self, x_cord, y_cord, file_name):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.button_image = pygame.image.load(f"{file_name}.png")
        self.hovered_button_image = pygame.image.load(f"{file_name}_hovered.png")
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.button_image.get_width(),
                                  self.button_image.get_height())

    def tick(self):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                return True

    def draw(self, window):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            window.blit(self.hovered_button_image, (self.x_cord, self.y_cord))
        else:
            window.blit(self.button_image, (self.x_cord, self.y_cord))


class TextInput:
    def __init__(self, x, y, width, height, maxlen=-1, placeholder="", password=False):
        self.x_cord = x
        self.y_cord = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Calibri", 48)
        self.text = ""
        self.font_image = pygame.font.Font.render(self.font, self.text, True, (0, 0, 0))
        self.placeholder = placeholder
        self.placeholder_img = pygame.font.Font.render(self.font, placeholder, True, (100, 100, 100))
        self.maxlen = maxlen
        self.active = False
        self.cursor = pygame.rect.Rect(self.x_cord + 5, self.y_cord + 15, 2, 50)
        self.cursor_vis = True
        self.password = password

    def tick(self, clock, events):
        for event in events:
            if event.type == pygame.KEYDOWN:  # jeśli jakiś klawisz naciśnięty
                if event.key == pygame.K_RETURN:  # jeśli enter kliknięty
                    return self.text
                elif event.key == pygame.K_BACKSPACE:  # jeśli backspace kliknięty
                    self.text = self.text[:-1]  # usuwa ostatni znak
                elif len(self.text) < self.maxlen or self.maxlen == -1:
                    if self.active and event.unicode.isprintable():
                        self.text += event.unicode
                self.font_image = pygame.font.Font.render(self.font, self.text, True, (0, 0, 0))
                text_x = self.font_image.get_width()
                self.cursor = pygame.rect.Rect(self.x_cord + 5 + text_x, self.y_cord + 15, 2, 50)

        if round(clock) % 2 == 0:  # kursor miga co sekundę
            self.cursor_vis = True
        else:
            self.cursor_vis = False

        if pygame.mouse.get_pressed(3)[0]:  # jeśli lewy przycisk myszy klinięty
            if pygame.rect.Rect(self.x_cord, self.y_cord,  # jeśli kliknięto na pole
                                self.width, self.height).collidepoint(pygame.mouse.get_pos()):
                self.active = True
            else:  # jeśli kliknięto poza polem
                self.active = False

    def draw(self, win):
        pygame.draw.rect(win, (4, 207, 222),
                         (self.x_cord - 4, self.y_cord - 4, self.width + 8, self.height + 8),
                         border_radius=20)
        pygame.draw.rect(win, (255, 255, 255),
                         (self.x_cord, self.y_cord, self.width, self.height),
                         border_radius=20)
        if self.text:  # jeśli użytkownik coś wpisał
            if self.password:  # jeśli typ pola to hasło
                text = len(self.text) * '*'  # zastąp tekst gwiazdkami
            else:  # typ pole to nie hasło
                text = self.text
            self.font_image = pygame.font.Font.render(self.font, text, True, (0, 0, 0))
            win.blit(self.font_image, (self.x_cord + 5, self.y_cord + 15))
        else:  # jeśli pole tekstowe jest puste
            win.blit(self.placeholder_img, (self.x_cord + 5, self.y_cord + 15))

        if self.cursor_vis:
            pygame.draw.rect(win, (90, 90, 90), self.cursor)


class Player(Physic, Health):
    def __init__(self):
        self.stand_right_img = pygame.image.load('John/stand.png')  # normalna grafika
        self.stand_left_img = pygame.transform.flip(pygame.image.load('John/stand.png'), True, False)
        width = self.stand_right_img.get_width()  # szerokość
        height = self.stand_right_img.get_height()  # wysokość
        Health.__init__(self, 100)
        Physic.__init__(self, 0, 540, width, height, 0.5, 5)
        self.jump_right_img = pygame.image.load('John/jump.png')  # grafika skoku
        self.jump_left_img = pygame.transform.flip(pygame.image.load('John/jump.png'), True, False)  # grafika skoku
        self.walk_right_img = [pygame.image.load(f'John/walk/klatka0{x}.png') for x in
                               range(1, 7)]  # animacja chodzenia
        self.walk_left_img = [pygame.transform.flip(pygame.image.load(f'John/walk/klatka0{x}.png'), True, False) for x
                              in range(1, 7)]  # animacja chodzenia
        self.walk_index = 0
        self.direction = 1

    def tick(self, keys, beams, delta_tm):  # wykonuje się raz na powtórzenie pętli
        self.physic_tick(beams)
        self.health_tick(delta_tm)
        if not self.alive:
            return
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

        self.draw_health(win, x_screen, self.y_cord - 15, self.width, 10)

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


class Ghost(Physic):
    def __init__(self, x, y):
        self.image = pygame.image.load("ghost.png")
        width, height = self.image.get_size()

        super().__init__(x, y, width, height, 1, 3)
        self.gravity = 0.2

    def go_left(self):
        if -self.hor_velocity < self.max_vel:
            self.hor_velocity -= self.acc

    def go_right(self):
        if self.hor_velocity < self.max_vel:
            self.hor_velocity += self.acc

    def go_up(self):
        if -self.ver_velocity < self.max_vel:
            self.ver_velocity -= self.gravity + self.acc

    def tick(self, beams, player):
        self.physic_tick(beams)
        if self.hitbox.colliderect(player.hitbox):
            player.dealt_damage(20, 0.5)  # zadaj dwadzieścia obrażeń
        elif not self.hitbox.colliderect(player.hitbox):
            if self.y_cord > player.y_cord + 15:
                self.go_up()
            if self.x_cord > player.x_cord:
                self.go_left()
            elif self.x_cord < player.x_cord:
                self.go_right()
            if abs(self.x_cord - player.x_cord) > 40:
                h = pygame.rect.Rect(self.x_cord - 15, self.y_cord + 20, self.width+30, self.height - 25)
                for beam in beams:
                    if h.colliderect(beam.hitbox):
                        self.go_up()
                        break
            if randint(0, 20) == 15:
                self.go_up()
                self.go_up()
            if randint(0, 20) == 15:
                self.go_left()
                self.go_left()
            if randint(0, 20) == 15:
                self.go_right()
                self.go_right()

    def draw(self, win, world_x):
        win.blit(self.image, (self.x_cord + world_x, self.y_cord))


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
