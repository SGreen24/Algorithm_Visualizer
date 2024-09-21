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

    FONT = pygame.font.SysFont('roboto', 30)
    LARGE_FONT = pygame.font.SysFont('roboto', 40)

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
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

    sorting = draw_info.FONT.render("I - Insertion | S - Selection | B - Bubble | M - Merge | Q - Quick | H - Heap", 1,
                                    draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 75))

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions=None, clear_bg=False):
    if color_positions is None:
        color_positions = {}
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD,
                      draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.board_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.board_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.board_width, draw_info.height))

        if clear_bg:
            pygame.display.update()


# Create our random list of values
def generate_starting_list(n, min_val, max_val):
    # O(n) - Each value is generated randomly once for each element
    lst = [random.randint(min_val, max_val) for _ in range(n)]
    return lst


# Bubble Sort - Time complexity: O(n^2)
def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    # O(n) for outer loop
    for i in range(len(lst) - 1):
        # O(n) for inner loop, making it O(n^2) in total
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]  # O(1) - Single swap operation
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True

    return lst


# Insertion Sort - Time complexity: O(n^2)
def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    # O(n) for the outer loop
    for i in range(1, len(lst)):
        current = lst[i]
        # O(n) in the worst case when each element has to be compared (so O(n^2) total)
        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]  # O(1) - Single assignment
            i -= 1
            lst[i] = current  # O(1)
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst


# Merge Sort - Time complexity: O(n log n)
def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst

    # Merging step - O(n)
    def merge(start, mid, end):
        left = lst[start:mid + 1]  # O(k) - where k is the size of left
        right = lst[mid + 1:end + 1]  # O(k) - where k is the size of right

        i = j = 0
        k = start
        while i < len(left) and j < len(right):  # O(k)
            if (left[i] <= right[j] and ascending) or (left[i] >= right[j] and not ascending):
                lst[k] = left[i]
                i += 1
            else:
                lst[k] = right[j]
                j += 1
            draw_list(draw_info, {k: draw_info.GREEN}, True)
            k += 1
            yield True

        while i < len(left):  # O(k)
            lst[k] = left[i]
            draw_list(draw_info, {k: draw_info.GREEN}, True)
            i += 1
            k += 1
            yield True

        while j < len(right):  # O(k)
            lst[k] = right[j]
            draw_list(draw_info, {k: draw_info.GREEN}, True)
            j += 1
            k += 1
            yield True

    # Recursive step - O(log n)
    def merge_sort_recursive(start, end):
        if start >= end:
            return

        mid = (start + end) // 2
        yield from merge_sort_recursive(start, mid)  # O(log n) depth of recursion
        yield from merge_sort_recursive(mid + 1, end)
        yield from merge(start, mid, end)  # O(n) per level of recursion

    yield from merge_sort_recursive(0, len(lst) - 1)


# Quick Sort - Time complexity: O(n log n) average, O(n^2) worst case
def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst

    # Partition step - O(n)
    def partition(low, high):
        pivot = lst[high]
        i = low - 1

        for j in range(low, high):  # O(n) to scan the partition
            if (lst[j] <= pivot and ascending) or (lst[j] >= pivot and not ascending):
                i += 1
                lst[i], lst[j] = lst[j], lst[i]  # O(1)
                draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
                yield True

        lst[i + 1], lst[high] = lst[high], lst[i + 1]  # O(1) swap with pivot
        draw_list(draw_info, {i + 1: draw_info.GREEN, high: draw_info.RED}, True)
        yield True
        return i + 1

    # Recursive step - O(log n) on average
    def quick_sort_recursive(low, high):
        if low < high:
            pi = yield from partition(low, high)  # O(n) per partition
            yield from quick_sort_recursive(low, pi - 1)  # O(log n) recursive depth
            yield from quick_sort_recursive(pi + 1, high)

    yield from quick_sort_recursive(0, len(lst) - 1)


# Heap Sort - Time complexity: O(n log n)
def heapify(draw_info, n, i, ascending=True):
    lst = draw_info.lst
    largest = i  # O(1)
    left = 2 * i + 1  # O(1)
    right = 2 * i + 2  # O(1)

    if ascending:
        if left < n and lst[left] > lst[largest]:  # O(1) comparison
            largest = left
        if right < n and lst[right] > lst[largest]:  # O(1)
            largest = right
    else:
        if left < n and lst[left] < lst[largest]:  # O(1)
            largest = left
        if right < n and lst[right] < lst[largest]:  # O(1)
            largest = right

    if largest != i:
        lst[i], lst[largest] = lst[largest], lst[i]  # O(1)
        draw_list(draw_info, {i: draw_info.GREEN, largest: draw_info.RED}, True)
        yield True
        yield from heapify(draw_info, n, largest, ascending)  # O(log n) depth of recursion


# Heap Sort Implementation - O(n log n)
def heap_sort(draw_info, ascending=True):
    lst = draw_info.lst
    n = len(lst)

    # Build heap - O(n)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(draw_info, n, i, ascending)

    # Extract elements from heap - O(n log n)
    for i in range(n - 1, 0, -1):
        lst[i], lst[0] = lst[0], lst[i]  # O(1)
        draw_list(draw_info, {i: draw_info.GREEN, 0: draw_info.RED}, True)
        yield True
        yield from heapify(draw_info, i, 0, ascending)  # O(log n)


# Selection Sort - Time complexity: O(n^2)
def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst
    n = len(lst)

    # O(n) outer loop
    for i in range(n):
        min_index = i
        # O(n) inner loop, making the overall complexity O(n^2)
        for j in range(i + 1, n):
            if (lst[j] < lst[min_index] and ascending) or (lst[j] > lst[min_index] and not ascending):
                min_index = j

            draw_list(draw_info, {j: draw_info.RED, min_index: draw_info.GREEN}, True)
            yield True

        # O(1) swap
        lst[i], lst[min_index] = lst[min_index], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, min_index: draw_info.RED}, True)
        yield True


# Main Function to Run the Program
def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_generator = None

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = board_info(800, 600, lst)

    pygame.display.update()

    while run:
        clock.tick(120)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algorithm_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False

            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False

            # Sorting algorithm options
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algorithm_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algorithm_name = "Bubble Sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algorithm_name = "Merge Sort"
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algorithm_name = "Quick Sort"
            elif event.key == pygame.K_h and not sorting:
                sorting_algorithm = heap_sort
                sorting_algorithm_name = "Heap Sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algorithm_name = "Selection Sort"

    pygame.quit()


if __name__ == "__main__":
    main()
