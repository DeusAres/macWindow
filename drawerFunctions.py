from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

def openImage(image):
    
    return Image.open(image)

def openImageAsJPG(image):

    return Image.open(image).convert("RGB")

def openImageAsPNG(image):

    return Image.open(image).convert("RGBA")
#---------------------------------------#

def backgroundPNG(MAX_W, MAX_H, backgroundColor = None):
    background = Image.new("RGBA", (MAX_W, MAX_H), color = backgroundColor)
    draw = ImageDraw.Draw(background)

    return background, draw

#---------------------------------------#

def backgroundJPG(MAX_W, MAX_H, backgroundColor):
    background = Image.new("RGB", (MAX_W, MAX_H), backgroundColor)
    draw = ImageDraw.Draw(background)

    return background, draw

#---------------------------------------#

def pasteItem(background, item, x, y):
    background.paste(item, (x,y), item)

    return background
    
#---------------------------------------#

def resize(image, x, y, resample = Image.LANCZOS):
    image = image.resize((x, y), resample = resample)

    return image

#---------------------------------------#

def resizeToFit(image, sizeToFit, resample = Image.LANCZOS):
    x, y = image.width, image.height
    if x > y:
        y = int(y * sizeToFit / x)
        x = sizeToFit
    else:
        x = int(x * sizeToFit / y)
        y = sizeToFit
    
    return resize(image, x, y, resample = resample)

#---------------------------------------#

def cropImage(image, tupla):
    image = image.crop(tupla)

    return image

def cropToRealSize(image):
    tupla = image.getbbox()
    image = cropImage(image, tupla)
    
    return image

#---------------------------------------#

def flip(image):
    image = ImageOps.flip(image)

    return image

def mirror(image):
    image = ImageOps.mirror(image)

    return image

#---------------------------------------#

def fontDefiner(fontPath, fontSize):
    path = fontPath
    font = ImageFont.truetype(str(path), size = fontSize)

    return font

#---------------------------------------#

def centerItem(MAX_W, MAX_H, item):
    x, y = int((MAX_W - item.width)/2), int((MAX_H - item.height)/2)

    return x,y

#---------------------------------------#

def drawText(x, y, draw, message, fontColor, font):
    draw.text((x, y), message, fill = fontColor, font = font)

    return draw

#---------------------------------------#

def centerSingleLineText(MAX_H, MAX_W, font, fontColor, message, draw):
    x, y = font.getsize(message)
    x = (MAX_H - x)/2
    y = (MAX_W - y)/2
    draw = draw.text((x,y), message, fill = fontColor, font = font)
    return draw
    
#---------------------------------------#

def centerMultipleLineText(MAX_H, MAX_W, font, fontColor, message, draw):
    line_dimensions = [draw.textsize(line, font=font) for line in message]
    offset = (MAX_H - sum(h for w, h in line_dimensions)) // 2

    current_h = offset
    for line, (w, h) in zip(message, line_dimensions):
        draw.text(((MAX_W - w) // 2, current_h), line, fill = fontColor, font=font)
        current_h += h
    
    return draw

#---------------------------------------#

def roundCorners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

#---------------------------------------

def roundCornersAngles(im, rad, angles):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size

    if 1 in angles: alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0)) #1angolo sinistro sopra
    if 2 in angles: alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0)) #2angolo destro sopra
    if 3 in angles: alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad)) #3angolo destro sotto
    if 4 in angles: alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad)) #4angolo sinistro sotto
    im.putalpha(alpha)
    return im

#---------------------------------------

def drawRectangle(draw, x1, y1, x2, y2, rectangleColor = None, outline = None, width = 1):
    draw.rectangle([x1, y1, x2, y2], fill = rectangleColor, outline = outline, width = width)
    
    return draw


#---------------------------------------

def rotate(img, angle, expand = True):
    img = img.rotate(angle, resample= Image.BILINEAR, expand = expand)
    return img

#---------------------------------------------------------------------------------------------------------------------------#

def inverseColor(color):
    rgbNumber = ""
    rgb = []
    for char in color:
        if char.isdigit():
            rgbNumber += char
        if char == ',' or char == ')':
            rgb.append(int(rgbNumber))
            rgbNumber = ""
    r, g, b = rgb[0], rgb[1], rgb[2]
    inverseRGB = 'rgb(' + str(255 - r) + ',' + str(255 - g) + ',' + str(255 - b) + ')'
    return inverseRGB

#---------------------------------------------------------------------------------------------------------------------------#

def replaceColor(image, colorToReplace = None, replaceColor = None):
    import numpy as np
    def parser(color):
        color = str(color)
        rgbNumber = ""
        rgb = []
        for char in color:
            if char.isdigit():
                rgbNumber += char
            if char == ',' or char == ')':
                rgb.append(int(rgbNumber))
                rgbNumber = ""
        r, g, b = rgb[0], rgb[1], rgb[2]
        return  r, g, b
        
    data = np.array(image)
    r, g, b, a = data.T
    if colorToReplace == None: #replace all pixels
        data[..., :-1] = (parser(replaceColor))
        image = Image.fromarray(data)
    else: #replace single color
        rr, gg, bb = parser(colorToReplace)
        colorToReplace = (r == rr) & (g == gg) & (b == bb)
        data[..., :-1][colorToReplace.T] = (parser(replaceColor))
        image = Image.fromarray(data)
    
    return image

#---------------------------------------------------------------------------------------------------------------------------#

import numpy as np
import colorsys

rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)

def shift_hue(arr, hout):
    r, g, b, a = np.rollaxis(arr, axis=-1)
    h, s, v = rgb_to_hsv(r, g, b)
    h = hout
    r, g, b = hsv_to_rgb(h, s, v)
    arr = np.dstack((r, g, b, a))
    return arr

def shiftColors(image, hue):
    """
    Colorize PIL image `original` with the given
    `hue` (hue within 0-360); returns another PIL image.
    """
    img = image.convert('RGBA')
    arr = np.array(np.asarray(img).astype('float'))
    new_img = Image.fromarray(shift_hue(arr, hue/360.).astype('uint8'), 'RGBA')

    return new_img

#---------------------------------------------------------------------------------------------------------------------------#
def hslToRgb(H, S, L):
    import math
    S, L =  S/100, L/100
    C = (1.0 - abs(2.0*L - 1.0)) * S
    X = C*(1 - abs((H/60)%2 - 1.0))
    M = L - C/2

    if H >= 0 and H < 60 : rgb = [C,X,0]
    if H >= 60 and H < 120 : rgb = [X,C,0]
    if H >= 120 and H < 180: rgb = [0,C,X]
    if H >= 180 and H < 240: rgb = [0,X,C]
    if H >= 240 and H < 300: rgb = [X,0,C]
    if H >= 300 and H < 360: rgb = [C,0,X]

    r, g, b = rgb[0]+M, rgb[1]+M, rgb[2]+M
    return (int(r*255), int(g*255), int(b*255))


#---------------------------------------------------------------------------------------------------------------------------#

def getSize(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)
#---------------------------------------------------------------------------------------------------------------------------#
def drawShadow(image, background=0xffffff, offset = 20, radius = 30):
    
    canvasB, canvasD = backgroundPNG(image.size[0] + offset*20, image.size[1] + offset*20)
    alpha = image.getchannel('A')
    shadow = Image.new('RGBA', image.size, color = "rgb(0,0,0)")
    shadow.putalpha(alpha)
  
    shadow = resize(shadow, shadow.size[0] + int(offset/2), shadow.size[1] + int(offset/2))
    
    x,y = centerItem(canvasB.width, canvasB.height, shadow)
    x,y = x+25, y+30
    canvasB = pasteItem(canvasB, shadow, x, y)
    canvasB = canvasB.filter(ImageFilter.GaussianBlur(radius = radius))
    return canvasB

#---------------------------------------------------------------------------------------------------------------------------#
def blurImage(image, radius):

    image = image.filter(ImageFilter.GaussianBlur(radius = radius))
    return image

#---------------------------------------------------------------------------------------------------------------------------#
def calculateLuminance(image):
    image = image.resize((100, 100), resample = Image.BICUBIC)
    arr = np.array(image)

    R, G, B = 0.2126, 0.7152, 0.0722
    import sys
    np.set_printoptions(threshold=False)
    arr = arr[arr[:, :, 3]>0]

    luminance_total = 0
    total_num_sum = 0

    for x in arr:
        luminance_total += int(x[0]*R + x[1]*G + x[2]*B)
        total_num_sum += 1


    luminance = int(luminance_total/total_num_sum/255*100)
    print(luminance)
    if luminance > 40: 
        return 10
    else:
        return 94
    
#---------------------------------------------------------------------------------------------------------------------------#