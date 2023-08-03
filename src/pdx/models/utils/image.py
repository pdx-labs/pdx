from base64 import b64decode
from io import BytesIO


def decode_base64_to_display(base64_string):
    try:
        from PIL import Image
    except ImportError:
        raise ImportError("""
                        Pillow is required to display base64 images.\n
                        Install using `pip install pillow`
                        """)

    image_data = b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    return image


def format_response(base_string, input, decode_format=True):
    if input == 'url':
        return base_string
    elif input == 'b64_json':
        if decode_format:
            image_bytes = b64decode(base_string)
            return image_bytes
        else:
            return base_string
    # elif input == 'image':
    #     image = decode_base64_to_display(base_string)
    #     return image
    else:
        raise ValueError(f"Invalid format: {input}")


def _image(image_data: bytes):
    from IPython.display import display
    try:
        from PIL import Image
    except ImportError:
        raise ImportError("""
                        Pillow is required to display base64 images.\n
                        Install using `pip install pillow`
                        """)
    image_file = f"{'zero'}-{0}.png"
    with open(image_file, mode="wb") as png:
        png.write(image_data)
    image = Image.open(BytesIO(image_data))
    display(image)
