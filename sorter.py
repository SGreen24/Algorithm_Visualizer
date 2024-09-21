import pygame
import random

pygame.init()


# Information on the board we'll use on Pygame
class board_info:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE

    # Grey gradients for our numbers in graph
    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    # Fonts we want for our program (Integrate nicer fonts later):

    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    # Padding on the sides and top of our program

    SIDE_PAD = 100
    TOP_PAD = 150

    # Width, Height and Starting List we wanna sort
    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        # Sets the board we'll be using
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sorting Algorithm Visualizer!")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.board_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.board_height = round((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info):
    # Fills the background with our white color from before in board_info
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1,
                                     draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 45))

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info):
    lst = draw_info.lst

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.board_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.board_height

        # we have indices 0,1,2 (from the gray gradients)
        color = draw_info.GRADIENTS[i % 3]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.board_width, draw_info.height))


# Creates our random list of values
def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


# Runs the program
def main():
    run = True

    # Regulates how long the game will run
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    # Start without sorting, ascending order by default
    sorting = False
    ascending = True

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = board_info(800, 600, lst)

    pygame.display.update()

    while run:
        clock.tick(60)  # 60 fps

        draw(draw_info)

        # Returns all the events in the last loop
        for event in pygame.event.get():

            # event.type allows us to exit out of our program
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            # Where the fun begins!!!

            # Press Space to generate a random list
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False

            # Press space to start sorting
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False

    pygame.quit()


if __name__ == "__main__":
    main()
