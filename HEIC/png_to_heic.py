from PIL import Image

def convert_png_to_heic(input_path, output_path):
    # Open the PNG image
    image = Image.open(input_path)

    # Save the image in HEIC format
    image.save(output_path, format="HEIC")

# Example usage
input_png_path = "HEIC\HEIC-Profilepic.heic"
output_heic_path = "HEIC\HEIC-Profilepic.heic"

convert_png_to_heic(input_png_path, output_heic_path)
