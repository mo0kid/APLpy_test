import os

import aplpy
from astropy.io import fits
import matplotlib.pyplot as plt


def isolate_image_extension(fits_file, extension):
    """
        Saves the data + header of the specified extension as
        new FITS file

        input
        ------
        fits_file: file path to FITS image
        extension: Number of HDU extension containing the image data
    """

    header = fits.getheader(fits_file, extension)
    data = fits.getdata(fits_file, extension)

    fits.writeto('%s_image.fits' % fits_file.rstrip('.fits'), data, header)


# Get user input
input_r = input("Enter red channel FITS source file: ")
input_g = input("Enter green channel FITS source file: ")
input_b = input("Enter blue channel FITS source file: ")
v_min = input("Enter v_min (eg. 0.0): ")
v_max = input("Enter v_max (eg. 100.0 ")
exponent = input("Enter exponent (eg. 0.45): ")
input_north = input("rotate north up? (yes|no): ")

if input_north.lower() in ["yes", "y"]:
    north = True
else:
    north = False

stretch = 'power'

# Get data from FITS header
hdul = fits.open(input_r)
target = hdul[0].header["targname"]         # Standard astronomical catalog name for target
source = hdul[0].header["telescop"]         # Telescope used to acquire the data
out_file = hdul[0].header["targprop"]       # Proposer's name for the target
red_filter = hdul[0].header["filter"]       # Name of the filter element used
hdul = fits.open(input_g)
green_filter = hdul[0].header["filter"]
hdul = fits.open(input_b)
blue_filter = hdul[0].header["filter"]

# Create new FITS files containing only the image extension
for exposure in [input_r, input_g, input_b]:
    isolate_image_extension(exposure, 1)

# Set rgb_cube filenames
image_r = input_r[:-5]+'_image.fits'
image_g = input_g[:-5]+'_image.fits'
image_b = input_b[:-5]+'_image.fits'
image_cube = out_file+'_cube.fits'

# Combine FITS files into *_cube.fits
aplpy.make_rgb_cube([
        image_r,
        image_g,
        image_b],
        image_cube,
        north=north)

# Tidy up _image.fits files
os.remove(image_r)
os.remove(image_g)
os.remove(image_b)

# Stretch image_data and make .png
aplpy.make_rgb_image(
        out_file+'_cube.fits',
        out_file+'.png',
        vmin_r=float(v_min),
        vmin_g=float(v_min),
        vmin_b=float(v_min),
        vmax_r=float(v_max),
        vmax_g=float(v_max),
        vmax_b=float(v_max),
        stretch_r=stretch,
        stretch_g=stretch,
        stretch_b=stretch,
        exponent_r=float(exponent),
        exponent_b=float(exponent),
        exponent_g=float(exponent),)

# Create figure from .png
fig = aplpy.FITSFigure(out_file+'.png', hdu=0)

# Construct title
title = (out_file+"_cube.fits\n"
         + source
         + " | "
         + target
         + " | v_min:"
         + v_min
         + "  v_max:"
         + v_max
         + " stretch:"
         + stretch
         + " exp:"
         + exponent
         + " north:"
         + str(north)
         + "\n"
         + "r: "
         + red_filter
         + "    g: "
         + green_filter
         + "    b: "
         + blue_filter
         + "\n")

print(title)
fig.set_title(title)

fig.show_rgb()

plt.savefig(out_file+"_fig.png")
plt.show()
