import sys
from typing import List, Tuple

from PIL import Image, ImageDraw

from openalpr import Alpr

Coordinate = Tuple[int, int]
Polygon = List[Coordinate]


def get_regions_occupied_by_license_plates(image_path: str) -> List[Polygon]:
    openalpr_recognizer = Alpr("us", "/usr/local/etc/openalpr/openalpr.conf",
                               "/usr/local/Cellar/openalpr/HEAD-de93f21_1/share/openalpr/runtime_data/")

    if not openalpr_recognizer.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)

    results = openalpr_recognizer.recognize_file(image_path)

    license_plate_regions = [result['coordinates'] for result in results['results']]
    license_plate_regions_as_tuples = [[(point['x'], point['y']) for point in region] for region in
                                       license_plate_regions]

    openalpr_recognizer.unload()  # release memory

    return license_plate_regions_as_tuples


def fill_regions_in_picture_with_black_and_save_to_a_new_destination(open_path: str,
                                                                     save_path: str,
                                                                     regions: List[Polygon]
                                                                     ) -> None:
    im = Image.open(open_path)

    draw = ImageDraw.Draw(im)
    for region in regions:
        draw.polygon(region, fill=(0, 0, 0))

    im.save(save_path, "PNG")


if __name__ == '__main__':
    extracted_regions: List[Polygon] = get_regions_occupied_by_license_plates("./pa2013invertcar.jpg")
    fill_regions_in_picture_with_black_and_save_to_a_new_destination("./pa2013invertcar.jpg", './drawtest.png',
                                                                     extracted_regions)
