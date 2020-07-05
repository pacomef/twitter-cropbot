from PIL import Image
import requests
from io import BytesIO
import random as r
import os.path
import sys

sys.stdout.flush()


def crop(path):
    print("[-] Crop started")
    file = get_file(path)
    pixels = file.width * file.height
    left, top, right, bottom = color_breaker(file)
    image_final = process(file, left, top, right - left, bottom - top)
    new_pixels = image_final.width * image_final.height
    return save(image_final), pixels - new_pixels


def save(image):
    while "not found a correct id":
        str_id = str(r.randint(0, 999999))
        if not os.path.isfile("image/n" + str_id + ".png"):
            break
    path = "image/n" + str_id + ".png"
    image.save(path, format="PNG")
    print("[+] Well outputed n" + str_id + ".png", flush=True)
    return path


def process(file, xstart, ystart, xlen, ylen):
    sizing = (xstart, ystart, xlen, ylen)
    print("[-] New dimensions : " + str(sizing), flush=True)
    return file.crop(box=sizing)


def get_file(path, ver=True):
    if "http" not in path:
        return Image.open(path)
    response = requests.get(path, verify=ver)
    return Image.open(BytesIO(response.content))


def get_color(img, x, y):
    r, g, b = img.getpixel((x, y))
    return [r, g, b]


def color_breaker(img, step=10):
    left_array = [get_break_left(img, step, round(img.height / 4)), get_break_left(img, step, round(img.height / 2)),
                  get_break_left(img, step, round(img.height / 4 * 3))]
    top_array = [get_break_top(img, step, round(img.width / 4)), get_break_top(img, step, round(img.width / 2)),
                 get_break_top(img, step, round(img.width / 4 * 3))]
    right_array = [get_break_right(img, step, round(img.height / 4)), get_break_right(img, step, round(img.height / 2)),
                  get_break_right(img, step, round(img.height / 4 * 3))]
    bottom_array = [get_break_bottom(img, step, round(img.width / 4)), get_break_bottom(img, step, round(img.width / 2)),
                 get_break_bottom(img, step, round(img.width / 4 * 3))]
    return min(left_array), min(top_array), min(right_array), min(bottom_array)


def get_break_top(img, step, xplace):
    step_breakedy = 0
    final_breaky = 0
    past_set = [0, 0, 0]
    current_set = [0, 0, 0]
    ylen = round(img.height / 2)
    for y in range(0, ylen, step):
        current_set = get_color(img, xplace, y)
        if y == 0:
            past_set = current_set
            continue
        if current_set != past_set:
            step_breakedy = y
            break
        else:
            past_set = current_set
        if y == ylen - step:
            return ylen
    past_set = [0, 0, 0]
    for y in range(step_breakedy - step, step_breakedy):
        current_set = get_color(img, xplace, y)
        if y == step_breakedy - step:
            past_set = current_set
            continue
        if current_set != past_set:
            if y >= step:
                final_breaky = y + round(step / 2)
            else:
                final_breaky = y
            break
        else:
            past_set = current_set
    return final_breaky


def get_break_left(img, step, yplace):
    step_breakedx = 0
    final_breakx = 0
    past_set = [0, 0, 0]
    current_set = [0, 0, 0]
    xlen = round(img.width / 2)
    for x in range(0, xlen, step):
        current_set = get_color(img, x, yplace)
        if x == 0:
            past_set = current_set
            continue
        if current_set != past_set:
            step_breakedx = x
            break
        else:
            past_set = current_set
        if x == xlen - step:
            return xlen
    past_set = [0, 0, 0]
    for x in range(step_breakedx - step, step_breakedx):
        current_set = get_color(img, x, yplace)
        if x == step_breakedx - step:
            past_set = current_set
            continue
        if current_set != past_set:
            if x >= step:
                final_breakx = x + round(step / 2)
            else:
                final_breakx = x
            break
        else:
            past_set = current_set
    return final_breakx


def get_break_bottom(img, step, xplace):
    step_breakedy = 0
    final_breaky = 0
    past_set = [0, 0, 0]
    current_set = [0, 0, 0]
    ylen = round(img.height / 2)
    for y in range(img.height - 1, ylen - 1, step * -1):
        current_set = get_color(img, xplace, y)
        if y == 0:
            past_set = current_set
            continue
        if current_set != past_set:
            step_breakedy = y
            break
        else:
            past_set = current_set
        if y == ylen - step:
            return ylen
    past_set = [0, 0, 0]
    for y in range(step_breakedy, step_breakedy - step, -1):
        current_set = get_color(img, xplace, y)
        if y == step_breakedy - step:
            past_set = current_set
            continue
        if current_set != past_set:
            if y <= img.height - step:
                final_breaky = y + round(step / 2)
            else:
                final_breaky = y
            break
        else:
            past_set = current_set
    return final_breaky


def get_break_right(img, step, yplace):
    step_breakedx = 0
    final_breakx = 0
    past_set = [0, 0, 0]
    current_set = [0, 0, 0]
    xlen = round(img.width / 2)
    for x in range(img.width - 1, xlen - 1, step * -1):
        current_set = get_color(img, x, yplace)
        if x == 0:
            past_set = current_set
            continue
        if current_set != past_set:
            step_breakedx = x
            break
        else:
            past_set = current_set
        if x == xlen - step:
            return xlen
    past_set = [0, 0, 0]
    for x in range(step_breakedx, step_breakedx - step, -1):
        current_set = get_color(img, x, yplace)
        if x == step_breakedx - step:
            past_set = current_set
            continue
        if current_set != past_set:
            if x <= img.width - step:
                final_breakx = x + round(step / 2)
            else:
                final_breakx = x
            break
        else:
            past_set = current_set
    return final_breakx