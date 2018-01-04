import os
from typing import List

from license_plate_censoring import get_regions_occupied_by_license_plates

from joblib import Parallel, delayed


def image_contains_a_license_plate(file_path: str) -> bool:
    return len(get_regions_occupied_by_license_plates(file_path)) > 0


residing_directory: str = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    car_picture_file_names: List[str] = os.listdir(os.path.join(residing_directory, 'trio-images'))

    results: List[bool] = Parallel(n_jobs=-2, verbose=11)(
        delayed(image_contains_a_license_plate)(os.path.join(residing_directory, 'trio-images', file_name)) for
        file_name in car_picture_file_names
    )

    license_plate_image_file_names: List[str] = [image_file_name for is_car, image_file_name in
                                                 zip(results, car_picture_file_names) if is_car]

    print(license_plate_image_file_names)

    open(os.path.join(residing_directory, 'openalpr_detected_images.txt'), 'w').write(
        '\n'.join(license_plate_image_file_names))
