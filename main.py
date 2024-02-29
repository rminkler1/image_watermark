import tkinter as tk
from tkinter import filedialog, simpledialog, colorchooser, StringVar, Label, OptionMenu, Button

import matplotlib.pyplot as plt
from PIL import Image, ImageFont, ImageDraw

application_window = tk.Tk()
result = None


def get_image(file_name):
    uploaded_image = Image.open(file_name).convert("RGBA")
    return uploaded_image


def add_watermark(base_image, image_text, text_pos, op, color):
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
    draw.text((x, y), image_text, fill=(color[0], color[1], color[2], op), font=font, anchor=anchor)
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


def my_choice_box(choicelist):
    global result

    def buttonfn():
        global result
        result = var.get()
        choicewin.quit()

    choicewin = tk.Tk()
    choicewin.resizable(False, False)
    choicewin.title("ChoiceBox")

    Label(choicewin, text="Select an item:").grid(row=0, column=0, sticky="W")

    var = StringVar(choicewin)
    var.set("No data")  # default option
    popupMenu = OptionMenu(choicewin, var, *choicelist)
    popupMenu.grid(sticky="W", row=1, column=0)

    Button(choicewin, text="Done", command=buttonfn).grid(row=2, column=0)
    choicewin.mainloop()
    return result


# positions
positions = ["top_right", "bot_right", "top_left", "bot_left", "center"]

# prompt for image
image_filename = None
while not image_filename:
    image_filename = filedialog.askopenfilename(parent=application_window,
                                                title="Please select an image file (.jpg .png .tif .tiff .gif):",
                                                filetypes=[("Image files", ".jpg .png .tif .tiff .gif")])

# prompt for text
watermark_text = None
while not watermark_text:
    watermark_text = simpledialog.askstring("Watermark text", "What text would you like to embed?")

# prompt for opacity
opacity = None
while not opacity:
    opacity = simpledialog.askinteger("Opacity", "Watermark opacity 0 - 100",
                                      minvalue=0, maxvalue=100)

# prompt for color (default to white)
rgb_color = colorchooser.askcolor(parent=application_window,
                                  initialcolor=(255, 255, 255))

# prompt for watermark position
position_selection = None
while position_selection not in positions:
    position_selection = my_choice_box(positions)

image = get_image(image_filename)
watermarked_image = add_watermark(image, watermark_text, position_selection, opacity, rgb_color[0], )

# open the photo viewer
watermarked_image.show()
plt.imshow(image)
