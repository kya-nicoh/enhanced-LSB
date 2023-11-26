from PIL import Image
import pillow_heif
import numpy as np

pillow_heif.register_heif_opener()

im = Image.open("HEIC/image.heic")  # do whatever need with a Pillow image
im = im.rotate(13)
im.save(f"rotated_image.heic", quality=90)


# if pillow_heif.is_supported("HEIC/image.heic"):
#     heif_file = pillow_heif.open_heif("HEIC/image.heic", convert_hdr_to_8bit=False)
#     print("image size:", heif_file.size)
#     print("image mode:", heif_file.mode)
#     print("image data length:", len(heif_file.data))
#     print("image data stride:", heif_file.stride)


if pillow_heif.is_supported("HEIC/image.heic"):
    heif_file = pillow_heif.open_heif("HEIC/image.heic")
    np_array = np.asarray(heif_file)