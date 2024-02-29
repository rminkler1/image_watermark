import matplotlib.pyplot as plt
from PIL import Image, ImageFont, ImageDraw


def get_image():
    uploaded_image = Image.open("images/IMAG0126-2.jpg").convert("RGBA")
    return uploaded_image


def add_watermark(base_image, image_text, text_pos, op):
    # convert opacity from 100 max to 255 max
    op = int(op * 2.55)

    watermark_image = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(watermark_image)
    w, h = base_image.size

    # set variables based on selected text position
    x, y, anchor, font_size = position_text(text_pos, w, h)

    # set font
    font = ImageFont.truetype("fonts/Arial.ttf", (font_size // 10))

    # add watermark
    draw.text((x, y), image_text, fill=(255, 255, 255, op), font=font, anchor=anchor)
    composite = Image.alpha_composite(base_image, watermark_image).convert("RGB")

    # save image file
    composite.save("output/image.jpg")

    # display image
    plt.subplot(1, 2, 2)
    plt.title("white text")
    plt.imshow(composite)
    return composite


def position_text(pos, width, height):
    _x, _y = (width // 2), (height // 2)
    if _x > _y:
        font_size = _y
    else:
        font_size = _x

    # set offset to pull text away from edge
    offset = _x // 20

    if pos == "center":
        anchor_point = "ms"

    elif pos == "top_left":
        anchor_point = "lt"
        _x = offset
        _y = _x

    elif pos == "bot_left":
        anchor_point = "lb"
        _x = offset
        _y = height - _x

    elif pos == "top_right":
        anchor_point = "rt"
        _y = offset
        _x = width - _y

    else:
        anchor_point = "rb"
        _y = height - offset
        _x = width - offset

    return _x, _y, anchor_point, font_size


# positions
positions = ["top_right", "bot_right", "top_left", "bot_left", "center"]
position = 1

# Opacity
opacity = 60

text = "© 2024 Robert Minkler"

image = get_image()
watermarked_image = add_watermark(image, text, positions[position], opacity)
# this open the photo viewer
watermarked_image.show()
plt.imshow(image)
