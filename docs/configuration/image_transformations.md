# Image Transformations

Input images can be pre-processed using a variety of transformations.

## Masking

Masking with a square or circle is currently supported. The mask will automatically be created based on the user input diameter, which should be a decimal proportion of the total image height. For example `mask = square` and `diameter = 0.9` will create a mask centered on the input image with a total height and width of 90% of the input.
