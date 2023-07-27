import pygame

pygame.init()


class Player:
    def __init__(self):
        self.hitbox = pygame.Rect(32, 32, 150, 150)

    def move(self, cx, cy, obstacles):
        if cx != 0:
            self.move_in_driection(cx, 0, obstacles)
        if cy != 0:
            self.move_in_driection(0, cy, obstacles)

    def move_in_driection(self, cx, cy, obstacles):
        self.hitbox.x += cx
        self.hitbox.y += cy

        for ob in obstacles:
            if self.hitbox.colliderect(ob.hitbox):
                if cx > 0:
                    self.hitbox.right = ob.hitbox.left
                if cx < 0:
                    self.hitbox.left = ob.hitbox.right
                if cy > 0:
                    self.hitbox.bottom = ob.hitbox.top
                if cy < 0:
                    self.hitbox.top = ob.hitbox.bottom

    def draw(self, window):
        pygame.draw.rect(window, (255, 0, 0), self.hitbox)


class Wall:
    def __init__(self, x, y):
        self.hitbox = pygame.Rect(x, y, 200, 200)

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.hitbox)


COLOR = (34, 103, 214)
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("Moja Gra")
clock = pygame.time.Clock()

player = Player()
walls = [
    Wall(400, 300),
]

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player.move(-4, 0, walls)
    if keys[pygame.K_d]:
        player.move(4, 0, walls)
    if keys[pygame.K_w]:
        player.move(0, -4, walls)
    if keys[pygame.K_s]:
        player.move(0, 4, walls)

    screen.fill(COLOR)
    player.draw(screen)
    for wall in walls:
        wall.draw(screen)

    pygame.display.flip()

pygame.quit()
