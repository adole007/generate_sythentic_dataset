import random

from random_file_list import RandomFileList

# Some defaults

# Root directory for images
# I used mnist set from https://github.com/myleott/mnist_png.git
ROOT_DIR ="C:/Users/coaaa2/Desktop/1000_cl/dataset/com_new_20_160"
#ROOT_DIR = 'E:/Users/coaaa2/Documents/original_dataset'

# Pixel size of each grid square
GRID_WIDTH = 48
GRID_HEIGHT = 48

# Number of grid squares in x and y
GRID_COUNT_X = 8
GRID_COUNT_Y = 12

# Random scale range 50% - 150%
SCALE_MIN = 0.5
SCALE_MAX = 1.5

# 50% coverage
COVERAGE = 0.8

# Random offset range (fraction of grid width)
OFFSET_MIN = 0.0
OFFSET_MAX = 0.3

# Repeat count
REPEAT = 5


def get_sign():
    return 1.0 if random.random() < 0.5 else -1.0


class Grid:
    def __init__(self, cell_width, cell_height, count_x, count_y):
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.count_x = count_x
        self.count_y = count_y

    @staticmethod
    def from_dict(dict):
        return Grid(dict['cell_width'], dict['cell_height'], dict['count_x'], dict['count_y'])

    @staticmethod
    def from_default():
        return Grid(GRID_WIDTH, GRID_HEIGHT, GRID_COUNT_X, GRID_COUNT_Y)

    def width(self):
        return self.count_x * self.cell_width

    def height(self):
        return self.count_y * self.cell_height


class GridParams:
    def __init__(self, root_dir, out_dir, repeat, grid, scale_min, scale_max, coverage, offset_min, offset_max,
                 show_bounds):
        self.root_dir = root_dir
        self.out_dir = out_dir
        self.repeat = repeat
        self.grid = grid
        self.scale_min = scale_min
        self.scale_max = scale_max
        self.coverage = coverage
        self.offset_min = offset_min
        self.offset_max = offset_max
        self.show_bounds = show_bounds

    @staticmethod
    def from_dict(dict):
        return GridParams(dict['root_dir'], dict['out_dir'], dict['repeat'], Grid.from_dict(dict['grid']),
                          dict['scale_min'], dict['scale_max'], dict['coverage'],
                          dict['offset_min'], dict['offset_max'], dict['show_bounds'])

    @staticmethod
    def from_defaults():
        return GridParams(ROOT_DIR, REPEAT, Grid.from_default(), SCALE_MIN, SCALE_MAX,
                          COVERAGE, OFFSET_MIN, OFFSET_MAX)

    def image_size(self):
        return self.grid.width(), self.grid.height()

    def fill_cell(self):
        return random.random() < self.coverage

    def random_offset(self):
        return random.uniform(self.offset_min, self.offset_max) * self.grid.cell_width * get_sign(), \
               random.uniform(self.offset_min, self.offset_max) * self.grid.cell_width * get_sign()

    def random_size(self, w, h):
        return int(float(w) * random.uniform(self.scale_min, self.scale_max)), \
               int(float(h) * random.uniform(self.scale_min, self.scale_max))

    def grid_centre(self, x_pos, y_pos):
        centre_x = (x_pos * self.grid.cell_width) + self.grid.cell_width / 2
        centre_y = (y_pos * self.grid.cell_height) + self.grid.cell_height / 2
        return centre_x, centre_y

    def gen_image_name(self, ext, rep):
        name = "grid_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}".format(self.grid.count_x, self.grid.count_y,
                                                           self.grid.cell_width, self.grid.cell_height,
                                                           self.coverage, self.scale_min, self.scale_max,
                                                           self.offset_min, self.offset_max, rep)
        return name + ext
