from PIL import Image, ImageFilter
from pillow_heif import HeifImagePlugin

image = Image.open(Path("test.heic"))
image.save("output.heic", exif=None, xmp=None)