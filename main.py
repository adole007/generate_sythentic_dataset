import json
import os
import xml.etree.ElementTree as ET

from xml.dom.minidom import Document
from PIL import Image, ImageDraw
from pathlib import Path

from grid_params import GridParams
from random_file_list import RandomFileList

IMAGE_EXT = '.png'


def create_out_dir(path, error_msg):
    new_dir = Path(path)
    if not new_dir.is_dir():
        os.makedirs(path)
    if not new_dir.is_dir():
        raise ValueError(error_msg)


def calculate_offset(grid_params, x, y, img):
    # find grid centre
    centre_x, centre_y = grid_params.grid_centre(x, y)

    # offset by half image width and height to centre image
    centre_x -= img.size[0] / 2
    centre_y -= img.size[1] / 2

    # add random offset
    offset_x, offset_y = grid_params.random_offset()
    centre_x += offset_x
    centre_y += offset_y

    return int(round(centre_x)), int(round(centre_y))


class BoundBox:
    def __init__(self, name, left=0, top=0, right=0, bottom=0):
        self.name = name
        self.left = min(left, right)
        self.top = min(top, bottom)
        self.right = max(right, right)
        self.bottom = max(top, bottom)

    def width(self):
        return self.right - self.left

    def height(self):
        return self.bottom - self.top

    def normalize(self, x_min, y_min, x_max, y_max):
        self.left = max(self.left, x_min)
        self.top = max(self.top, y_min)
        self.right = min(self.right, x_max)
        self.bottom = min(self.bottom, y_max)


def get_bound_box(xml_file):
    tree = ET.parse(xml_file)
    obj = tree.find('./object')
    bbox = obj.find('./bndbox')
    bound_box = BoundBox(obj.find('./name').text,
                         int(bbox.find('./xmin').text),
                         int(bbox.find('./ymin').text),
                         int(bbox.find('./xmax').text),
                         int(bbox.find('./ymax').text))
    return bound_box


def draw_grid(grid_params, random_img_list):
    # Create new grey scale image of the appropriate size (defaults to black background)
    img = Image.new('L', grid_params.image_size())

    # Build grid x by y
    bounds = []
    for x_pos in range(0, grid_params.grid.count_x):
        for y_pos in range(0, grid_params.grid.count_y):
            # Randomly cover grid
            if grid_params.fill_cell():
                # Get random source character
                img_path = random_img_list.random_path()
                src = Image.open(img_path, 'r').convert('L')

                # Crop to character bounds
                pre, ext = os.path.splitext(img_path)
                xml_file = pre + '.xml'
                bound_box = get_bound_box(xml_file)
                src = src.crop((bound_box.left, bound_box.top, bound_box.right, bound_box.bottom))

                # Randomly resize
                w, h = grid_params.random_size(src.size[0], src.size[1])
                src = src.resize((w, h), Image.ANTIALIAS)

                # Randomly offset from centre of cell
                x_off, y_off = calculate_offset(grid_params, x_pos, y_pos, src)

                new_bounds = BoundBox(bound_box.name, x_off, y_off, x_off + w, y_off + h)
                new_bounds.normalize(0, 0, img.size[0], img.size[1])
                bounds.append(new_bounds)

                # Draw character
                mask = src
                src = Image.new('L', src.size, color=255)
                img.paste(src, (x_off, y_off), mask)
    return img, bounds


def get_grid_params(file_path):
    with open(file_path, 'r') as in_file:
        in_str = in_file.read()
    params = json.loads(in_str)
    grids = []
    for param in params:
        grids.append(GridParams.from_dict(param))
    return grids


def create_and_append(doc, name, parent, text=None):
    child = doc.createElement(name)
    parent.appendChild(child)
    if text is not None:
        child.appendChild(doc.createTextNode(text))
    return child


def create_xml_doc(out_path, out_file, img_size, depth):
    doc = Document()
    annotation = create_and_append(doc, 'annotation', doc)
    create_and_append(doc, 'folder', annotation, 'characterset')
    create_and_append(doc, 'filename', annotation, out_file)
    create_and_append(doc, 'path', annotation, out_path)
    source = create_and_append(doc, 'source', annotation)
    create_and_append(doc, 'database', source, 'JapaneseData')
    size = create_and_append(doc, 'size', annotation)
    create_and_append(doc, 'width', size, str(img_size[0]))
    create_and_append(doc, 'height', size, str(img_size[1]))
    create_and_append(doc, 'depth', size, str(depth))
    create_and_append(doc, 'segmented', annotation, str(0))
    return doc, annotation


def append_bounds(doc, annotation, bounds):
    obj = create_and_append(doc, 'object', annotation)
    create_and_append(doc, 'name', obj, bounds.name)
    #print(bounds.name[:][:])
    create_and_append(doc, 'pose', obj, 'Unspecified')
    create_and_append(doc, 'truncated', obj, str(0))
    create_and_append(doc, 'difficult', obj, str(0))
    bnd_box = create_and_append(doc, 'bndbox', obj)
    create_and_append(doc, 'xmin', bnd_box, str(bounds.left))
    create_and_append(doc, 'ymin', bnd_box, str(bounds.top))
    create_and_append(doc, 'xmax', bnd_box, str(bounds.right))
    create_and_append(doc, 'ymax', bnd_box, str(bounds.bottom))


def render_bounds(grid_params, grid, bounds, out_name):
    if grid_params.show_bounds:
        grid = grid.convert('RGB')
        d = ImageDraw.Draw(grid)
        for bound in bounds:
            d.rectangle([bound.left, bound.top, bound.right, bound.bottom], outline=(0, 255, 0), width=1)
            d.text((bound.left, bound.top), bound.name, fill=(255,255,255))

        grid.save(os.path.join(grid_params.out_dir, 'bounds_' + out_name))


def main():
    grid_params_list = get_grid_params('grid_params.json')

    for grid_params in grid_params_list:
        create_out_dir(grid_params.out_dir, 'Could not create output directory')
        random_img_list = RandomFileList(grid_params.root_dir, '**/*.png', True)
        for repeat in range(0, grid_params.repeat):
            # generate grid image
            grid, bounds = draw_grid(grid_params, random_img_list)

            # Save grid
            out_name = grid_params.gen_image_name(IMAGE_EXT, repeat)
            out_file = os.path.join(grid_params.out_dir, out_name)
            grid.save(out_file)
            doc, annotation = create_xml_doc(grid_params.out_dir, out_name, grid.size, 1)

            for bound in bounds:
                append_bounds(doc, annotation, bound)
               

            pre, ext = os.path.splitext(out_file)
            with open(pre + '.xml', 'wb+') as f:
                f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))

            render_bounds(grid_params, grid, bounds, out_name)


if __name__ == "__main__":
    main()