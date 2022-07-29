import pygame


def main():
    """Main function to run Uno as a pygame"""
    pygame.init()
    logo = pygame.image.load('assets/Deck.png')
    pygame.display.set_icon(logo)
    pygame.display.set_caption('Uno')

    pygame.display.set_mode((320, 480))

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == '__main__':
    main()
