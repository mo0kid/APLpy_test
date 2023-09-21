import aplpy
from astropy.io import fits
import matplotlib.pyplot as plt

subject = 'NGC3256'
source = 'JWST'
v_min = 0.0
v_max = 100.0
stretch = 'power'
exponent = 0.45
north = False


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


# Create new FITS files containing only the image extension
for exposure in [
        'jw01328-o012_t019/jw01328-o012_t019_nircam_clear-f335m_i2d.fits',
        'jw01328-o012_t019/jw01328-o012_t019_nircam_clear-f200w_i2d.fits',
        'jw01328-o012_t019/jw01328-o012_t019_nircam_clear-f150w_i2d.fits']:
    isolate_image_extension(exposure, 1)

# Combine FITS files into *_cube.fits
aplpy.make_rgb_cube([
        'jw01328-o012_t019/jw01328-o012_t019_nircam_clear-f335m_i2d_image.fits',
        'jw01328-o012_t019/jw01328-o012_t019_nircam_clear-f200w_i2d_image.fits',
        'jw01328-o012_t019/jw01328-o012_t019_nircam_clear-f150w_i2d_image.fits'],
        'jw01328-o012_t019_cube.fits',
        north=north)

# Stretch image_data and make .png
aplpy.make_rgb_image(
        'jw01328-o012_t019_cube.fits',
        'jw01328-o012_t019.png',
        vmin_r=v_min,
        vmin_g=v_min,
        vmin_b=v_min,
        vmax_r=v_max,
        vmax_g=v_max,
        vmax_b=v_max,
        stretch_r=stretch,
        stretch_g=stretch,
        stretch_b=stretch,
        exponent_r=exponent,
        exponent_b=exponent,
        exponent_g=exponent,)

# Create figure from .png
fig = aplpy.FITSFigure('jw01328-o012_t019.png', hdu=0)

# Construct title
title = (subject
         + " "
         + source
         + "    v_min:"
         + str(v_min)
         + "  v_max:"
         + str(v_max)
         + " stretch:"
         + stretch
         + " exp:"
         + str(exponent)
         + " north:"
         + str(north))

print(title)
fig.set_title(title)

fig.show_rgb()

plt.show()
