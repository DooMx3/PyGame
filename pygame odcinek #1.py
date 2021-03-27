import pygame

pygame.init()
window = pygame.display.set_mode((800, 600))

x = 70
y = 50
player = pygame.rect.Rect(x, y, 100, 100)  # tworzy prostokąt

run = True
while run:
    pygame.time.Clock().tick(60)  # maksymalnie 60 fps
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # jeśli gracz zamknie okienko
            run = False

    keys = pygame.key.get_pressed()

    speed = 5
    if keys[pygame.K_RIGHT]:  # czy strzałka w prawo jest naciskana
        x += speed
    if keys[pygame.K_LEFT]:  # strzałka w lewo
        x -= speed
    if keys[pygame.K_UP]:  # strzałka w górę
        y -= speed
    if keys[pygame.K_DOWN]:  # strzałka w dół
        y += speed

    player = pygame.rect.Rect(x, y, 100, 100)

    window.fill((24, 164, 240))  # rysowanie tła
    pygame.draw.rect(window, (20, 200, 20), player)  # rysowanie gracza
    pygame.display.update()
