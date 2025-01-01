from PIL import Image
from PIL import ImageFont, ImageDraw


WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)


def render_char(char: str):
    image = Image.new("RGBA", (5, 5), BLACK)
    usr_font = ImageFont.FreeTypeFont("fonts/cg-pixel/cg-pixel-4x5.ttf", 5)
    d_usr = ImageDraw.Draw(image)
    d_usr.fontmode = "1"  # this apparently sets (anti)aliasing.
    d_usr.text((0, 0), char, WHITE, font=usr_font)
    return image


def render_text(char: str):
    image = Image.new("RGBA", (128, 5), BLACK)
    usr_font = ImageFont.FreeTypeFont("fonts/cg-pixel/cg-pixel-4x5.ttf", 5)
    d_usr = ImageDraw.Draw(image)
    d_usr.fontmode = "1"  # this apparently sets (anti)aliasing.
    d_usr.text((0, 0), char, WHITE, font=usr_font)
    return image


def main():
    for x in range(65, 65+26):
        img = render_char(chr(x))
        print(any([img.getpixel((3, x)) == WHITE for x in range(5)]))
    #     img.save(f'{x}.png', 'png')
    # image = render_text('ASK ME ABOUT SPACE ROBOTICS')
    # image.save('space_robotics.png', 'png')


if __name__ == '__main__':
    main()