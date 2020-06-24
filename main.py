from PIL import Image

TARGET_PATH = './captcha.gif'
RED = 220
GRAY = 227
WHITE = 255


def to_plain_gif(gif):
    plain_gif = Image.new('P', gif.size, 255)

    for x in range(gif.size[1]):
        for y in range(gif.size[0]):
            pixel = gif.getpixel((y, x))
            if pixel == RED or pixel == GRAY:
                plain_gif.putpixel((y, x), 0)

    return plain_gif


def get_letters(plain_gif):
    inletter, foundletter = False, False
    start, end = 0, 0
    letters = []

    for y in range(plain_gif.size[0]):
        for x in range(plain_gif.size[1]):
            pixel = plain_gif.getpixel((y, x))
            if pixel != WHITE:
                inletter = True

        if not foundletter and inletter:
            foundletter = True
            start = y
        if foundletter and not inletter:
            foundletter = False
            end = y
            letters.append((start, end))

        inletter = False

    return letters


def crop(letters, plain_gif):
    count = 0
    for letter in letters:
        letter_gif = plain_gif.crop((letter[0], 0, letter[1], plain_gif.size[1]))
        letter_gif.save('./crop/%s.gif' % count)

        count += 1


gif = Image.open(TARGET_PATH)
# 8位像素模式
gif.convert('P')
plain_gif = to_plain_gif(gif)

letters = get_letters(plain_gif)

crop(letters, plain_gif)
