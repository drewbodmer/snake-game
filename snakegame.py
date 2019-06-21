"""
 Simple snake example.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

"""
from random import randint

import pygame

# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the width and height of each snake segment
segment_width = 15
segment_height = 15
# Margin between each segment
segment_margin = 3

# Set initial speed
x_change = segment_width + segment_margin
y_change = 0


class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of the snake. """
    direction = "RIGHT"

    # -- Methods
    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(WHITE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_direction(self):
        return self.direction

    def set_direction(self, newdir):
        self.direction = newdir


# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])

# Set the title of the window
pygame.display.set_caption('Snake Example')

allspriteslist = pygame.sprite.Group()

# Create an initial snake
snake_segments = []
for i in range(15):
    x = 400 - (segment_width + segment_margin) * i
    y = 30
    segment = Segment(x, y)
    snake_segments.append(segment)
    allspriteslist.add(segment)
clock = pygame.time.Clock()
done = False

food = Segment(randint(-22, 22) * 18 + 400, randint(-16, 17) * 18 + 300)
allspriteslist.add(food)

eaten = False
direction = "R"

inc_length = 0
while not done:
    if eaten:
        food = Segment(randint(-20, 20) * 18 + 400, randint(-15, 15) * 18 + 300)
        allspriteslist.add(food)
        eaten = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Set the speed based on the key pressed
        # We want the speed to be enough that we move a full
        # segment, plus the margin.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = (segment_width + segment_margin) * -1
                y_change = 0
                direction = "L"
            if event.key == pygame.K_RIGHT:
                x_change = (segment_width + segment_margin)
                y_change = 0
                direction = "R"
            if event.key == pygame.K_UP:
                x_change = 0
                y_change = (segment_height + segment_margin) * -1
                direction = "U"
            if event.key == pygame.K_DOWN:
                x_change = 0
                y_change = (segment_height + segment_margin)
                direction = "D"

    # Figure out where new segment will be
    x = snake_segments[0].rect.x + x_change
    y = snake_segments[0].rect.y + y_change
    segment = Segment(x, y)
    segment.set_direction(direction)

    if x < 0 or x > 800 or y < 0 or y > 600:
        done = True

    for s in snake_segments:
        if s.rect.x == x and s.rect.y == y:
            done = True

    if snake_segments[0].rect.x == food.rect.x and food.rect.y == snake_segments[0].rect.y:
        eaten = True
        allspriteslist.remove(food)
        inc_length = 0

    if not eaten and inc_length > 3:
        # Get rid of last segment of the snake only if food isnt eaten
        # .pop() command removes last item in list
        old_segment = snake_segments.pop()
        allspriteslist.remove(old_segment)

    inc_length += 1
    # print(len(snake_segments))
    print(inc_length)
    # Insert new segment into the list
    snake_segments.insert(0, segment)
    allspriteslist.add(segment)

    # -- Draw everything
    # Clear screen
    screen.fill(BLACK)

    allspriteslist.draw(screen)

    # Flip screen
    pygame.display.flip()

    # Pause
    clock.tick(10)

pygame.quit()
