# Image Grid

Generate grid of images with perturbations

# Setup Python

Python version is 3.7. Moving to 2.7 should be straightforward though.

The project has a Pipfile to handle dependencies. To install follow instructions here:

https://docs.pipenv.org/en/latest/install/

Or you can use PyCharm:

https://www.jetbrains.com/help/pycharm/pipenv.html

Alternatively, just install the following dependencies:

Pillow
jsons

# Data Set

The code just requires a directory full of images to generate the grids. I used the mnist data set in png form to test
it out. You can download from here if you want to experiment without pointing at your main data set yet.

https://github.com/myleott/mnist_png.git
 
# Grid Configuration

The grid generation is configured through a json file (grid_params.json). The example has 3 grids. Each grid
setup has the following:

```json
{
    "coverage": 1.0,
    "grid": {
      "cell_height": 29,
      "cell_width": 29,
      "count_x": 16,
      "count_y": 32
    },
    "offset_max": 0.0,
    "offset_min": 0.0,
    "repeat": 5,
    "root_dir": "/media/chris/2F9A7F5065B666F1/mnist_png/mnist_png/training",
    "scale_max": 1.0,
    "scale_min": 1.0
  } 
```

- coverage - the fraction of grid cells that will contain an image. Value is 0.0 (no coverage) - 1.0 (full coverage)
- grid - describes grid characteristics
  * cell_height - count of pixels for the height of each cell
  * cell_width - count of pixels for the width of each cell
  * count_x - horizontal count of cells
  * count_y - vertical count of cells
- offset_max - maximum offset in the cell as a fraction of the cell size. Valid values run from 0.0 (no offsets) to any value (although values that are too high will push image out of the grid)
- offset_min - minimum offset in the cell as a fraction of the cell size. In combination with offset_max this describes the random number range to offset the image in the grid cell by
- repeat - how many images to create with these characteristics
- root_dir - directory containing images to be included as candidates for the grid
- scale_max - maximum value to scale image by.
- scale_min - minimum value to scale image by. In combination with scale_max, defines the scale range.

The above configuration generates the following image

![alt text](grid_16_32_29_29_1.0_1.0_1.0_0.0_0.0_0.png "One of the output images from the above configuration")

4x4 example with small images relative to cell and large perturbation and scale ranges

```json
{
    "coverage": 0.9,
    "grid": {
      "cell_height": 96,
      "cell_width": 96,
      "count_x": 4,
      "count_y": 4
    },
    "offset_max": 0.5,
    "offset_min": 0.0,
    "repeat": 5,
    "root_dir": "/media/chris/2F9A7F5065B666F1/mnist_png/mnist_png/training",
    "scale_max": 1.8,
    "scale_min": 0.1
  }
```

Above 4x4 configuration creates images like the following:

![alt text](grid_4_4_96_96_0.9_0.1_1.8_0.0_0.5_0.png "Example 4 x 4 high coverage but small images")

8x12 example output with smaller offset and scale ranges

```json
{
    "coverage": 0.8,
    "grid": {
      "cell_height": 48,
      "cell_width": 48,
      "count_x": 8,
      "count_y": 12
    },
    "offset_max": 0.3,
    "offset_min": 0.0,
    "repeat": 5,
    "root_dir": "/media/chris/2F9A7F5065B666F1/mnist_png/mnist_png/training",
    "scale_max": 1.5,
    "scale_min": 0.5
  }
```

Above 8x12 configuration creates images like the following:

![alt text](grid_8_12_48_48_0.8_0.5_1.5_0.0_0.3_0.png "Example 8 x 12")