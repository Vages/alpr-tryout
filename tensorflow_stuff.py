import os
import subprocess
from time import time
from typing import Set, List

from joblib import Parallel, delayed

residing_directory: str = os.path.dirname(os.path.realpath(__file__))
car_synonym_sets: Set[str] = set(
    [line.strip() for line in open(os.path.join(residing_directory, 'synsets_related_to_cars.txt'))]
)


def is_image_of_a_car(image_file_path: str) -> bool:
    result: subprocess.CompletedProcess = subprocess.run(
        [
            "python", os.path.join(residing_directory, "models/tutorials/image/imagenet/classify_image.py"),
            "--image_file=%s" % image_file_path
        ],
        stdout=subprocess.PIPE)
    standard_output: str = result.stdout.decode('utf-8')
    image_synonym_sets: Set[str] = set([line.split(" (")[0] for line in standard_output.strip().split('\n')])
    return not image_synonym_sets.isdisjoint(car_synonym_sets)


if __name__ == '__main__':
    image_directory = os.path.join(residing_directory, 'trio-images')
    trio_image_file_names: List[str] = \
        [f for f in os.listdir(image_directory) if os.path.isfile(os.path.join(image_directory, f))]

    a = time()
    is_car_image_results: List[bool] = Parallel(n_jobs=-2, verbose=11)(
        delayed(is_image_of_a_car)(os.path.join(residing_directory, 'trio-images', image_file_name)) for image_file_name
        in trio_image_file_names)
    car_image_file_names: List[str] = [image_file_name for is_car, image_file_name in
                                       zip(is_car_image_results, trio_image_file_names) if is_car]
    b = time()
    print(b - a)

    open(os.path.join(residing_directory, 'tensorflow_detected_images.txt'), 'w').write(
        '\n'.join(car_image_file_names))
