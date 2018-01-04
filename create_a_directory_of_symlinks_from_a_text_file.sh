#!/bin/sh

filename="$1"
filename_without_extension="${filename%.*}"

BASEDIR="$(pwd)"

trio_images_directory="${BASEDIR}/trio-images"
symlinked_images_directory="${trio_images_directory}/${filename_without_extension}"

mkdir $symlinked_images_directory

while read -r line
do
    image="$line"

    actual_image_location="${trio_images_directory}/${image}"
    symlink_location="${symlinked_images_directory}/${image}"

    ln -s "$actual_image_location" "$symlink_location"
done < "$filename"
