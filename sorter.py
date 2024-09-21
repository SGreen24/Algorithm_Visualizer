import pygame
import random
import math

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

    FONT = pygame.font.SysFont('roboto', 30)
    LARGE_FONT = pygame.font.SysFont('roboto', 40)

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
        self.board_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, sorting_algorithm_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{sorting_algorithm_name} - {'Ascending' if ascending else 'Descending'}", 1,
                                        draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1,
                                     draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 45))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 75))

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD,
                      draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.board_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.board_height

        # we have indices 0,1,2 (from the gray gradients)
        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.board_width, draw_info.height))

        if clear_bg:
            pygame.display.update()


# Creates our random list of values
def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    # Bubble Sort operation
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            # Comparing values hare - checks ascending in first conditional and descending in the second
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]  # Swapping values in the array

                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)

                # Generator yield
                yield True  # We call this EVERY TIME a swap occurs
                # It's going to pause, but store the current state of our function
                # So the next time, it starts where it ran the last time... think
                # of this as a autosave function!

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

    # We can change this to whatever we want, in this case were doing bubble
    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_generator = None

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = board_info(800, 600, lst)

    pygame.display.update()

    while run:
        clock.tick(120)  # 60 fps

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algorithm_name, ascending)

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
