from game import *

pygame.init()
resolution = (1280, 720)
window = pygame.display.set_mode(resolution)


def level_one():
    run = True
    pause = False
    pause_image = pygame.font.Font.render(pygame.font.SysFont("", 96), "Pauza", True, (255, 255, 255))
    player = Player()
    ghost = Ghost(300, 100)
    background = Background()
    clock = 0
    beams = [
        Beam(0, 690, 5000, 40),
        Beam(900, 600, 30, 120),
    ]
    while run:
        clock += pygame.time.Clock().tick(60) / 1000  # maksymalnie 60 fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # jeśli gracz zamknie okienko
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause = not pause
        keys = pygame.key.get_pressed()

        if pause:
            window.blit(pause_image, (500, 300))
            pygame.display.update()
            continue

        player.tick(keys, beams)
        ghost.tick(beams, player)
        background.tick(player)

        background.draw(window)
        player.draw(window, background.width)
        ghost.draw(window, background.x_cord)
        for beam in beams:
            beam.draw(window, background.x_cord)
        pygame.display.update()


def main():
    run = True
    clock = 0
    background = pygame.image.load('main menu/menu_background.png')
    play_button = Button(515, 500, "main menu/play_button")
    textinput = TextInput(470, 350, 250, 80, placeholder="wpisz login")
    while run:
        clock += pygame.time.Clock().tick(60) / 1000  # maksymalnie 60 fps
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:  # jeśli gracz zamknie okienko
                run = False
        content = textinput.tick(clock, events)
        if content is not None:
            print(f"użytkownik wprowadził wiadomość: {content}")
        if play_button.tick():
            level_one()

        window.blit(background, (0, 0))
        play_button.draw(window)
        textinput.draw(window)
        pygame.display.update()


if __name__ == "__main__":
    main()
