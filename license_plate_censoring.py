import sys
import os
from typing import List, Tuple
from PIL import Image, ImageDraw
from openalpr import Alpr

Coordinate = Tuple[int, int]
Polygon = List[Coordinate]

residing_directory: str = os.path.dirname(os.path.realpath(__file__))


def get_regions_occupied_by_license_plates(image_path: str, model_region: str="eu") -> List[Polygon]:
    openalpr_recognizer = Alpr(model_region, "/usr/local/etc/openalpr/openalpr.conf",
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
                                                                     regions: List[Polygon],
                                                                     fill_color=(0, 0, 0),
                                                                     ) -> None:
    im = Image.open(open_path)

    draw = ImageDraw.Draw(im)
    for region in regions:
        draw.polygon(region, fill=fill_color)

    im.save(save_path, "PNG")


def censor_picture_and_save_to_new_location(open_path: str, save_path: str, fill_color=(0, 0, 0)) -> None:
    fill_regions_in_picture_with_black_and_save_to_a_new_destination(open_path, save_path,
                                                                     get_regions_occupied_by_license_plates(open_path),
                                                                     fill_color)


if __name__ == '__main__':
    DEEP_PINK = (255, 20, 147)

    for image_name in os.listdir(os.path.join(residing_directory, "trio-images", "tensorflow_detected_images")):
        old_path: str = os.path.join(residing_directory, "trio-images", image_name)
        new_path: str = os.path.join(residing_directory, 'censored_license_plate_pictures', image_name)

        censor_picture_and_save_to_new_location(old_path, new_path, DEEP_PINK)
