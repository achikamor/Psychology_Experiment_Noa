import pygame
import math


def move_coords(angle, radius, coords):
    theta = math.radians(angle)
    return coords[0] + radius * math.cos(theta), coords[1] + radius * math.sin(theta)


def main():
    pygame.display.set_caption("Oribit")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    coords = 400, 200
    angle = 0
    rect = pygame.Rect(*coords, 20, 20)
    speed = 50
    next_tick = 500

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ticks = pygame.time.get_ticks()
        if ticks > next_tick:
            next_tick += speed
            angle += 1
            coords = move_coords(angle, 2, coords)
            rect.topleft = coords

        screen.fill((0, 0, 30))
        screen.fill((0, 150, 0), rect)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == '__main__':
    main()