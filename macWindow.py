import drawerFunctions, os, random
from PIL import Image
from pathlib import Path

def drawMacWindow(image, icon, title, path_to_font, shadow = True):
    """
    image = Path to image

    icon = Path to icon

    title = string for window title

    font_path = Path to your font (Use helvetica or I'll kill you)

    shadow = Boolean if you want to surround with shadow
    """
    
    #defining sizes
    border = 0
    titleBarH = 64

    maxImgSize = 1750

    image = drawerFunctions.openImageAsPNG(image)

    if image.width > maxImgSize or image.height > maxImgSize:
        image = drawerFunctions.resizeToFit(image, maxImgSize)
    MAX_W, MAX_H = image.width + border*2, image.height + titleBarH + border

    #full window
    window, draw = drawerFunctions.backgroundPNG(MAX_W, MAX_H)
    draw = drawerFunctions.drawRectangle(draw, 0, 0, MAX_W, MAX_H, rectangleColor = backgroundColor)


    #title bar
    x, y = MAX_W, titleBarH
    titleBar, draw = drawerFunctions.backgroundPNG(x, y)
    draw = drawerFunctions.drawRectangle(draw, 0, 0, x, y, rectangleColor = "rgb(28, 28, 28)")

    font = drawerFunctions.fontDefiner(path_to_font, 25)
    titleX, titleY = drawerFunctions.getSize(title, font)
    x, y = int(MAX_W/2 - titleX/2), int(titleBarH/2 - titleY/2 + 2)
    draw = drawerFunctions.drawText(x, y, draw, title, "rgb(255,255,255)", font)
    
    #paste button
    icon = drawerFunctions.openImage("icon.png")
    titleBar = drawerFunctions.pasteItem(titleBar, icon, x-8-icon.size[0], int(titleBarH/2 - icon.size[1]/2))
    buttons = drawerFunctions.openImage("buttons.png")
    x, y = 25, int(titleBarH/2 - buttons.height/2)
    titleBar = drawerFunctions.pasteItem(titleBar, buttons, x, y)
    window = drawerFunctions.pasteItem(window, titleBar, 0,0)
    
    
    x, y = border, int(titleBarH)
    window = drawerFunctions.pasteItem(window, image, x, y)
    window = drawerFunctions.roundCorners(window, 15)

    if shadow:
        backgroundImage = drawerFunctions.backgroundPNG(MAX_W*2, MAX_H*2)[0]

        shadow = drawerFunctions.drawShadow(window, offset = 10)
        x, y = drawerFunctions.centerItem(backgroundImage.width, backgroundImage.height, shadow)
        backgroundImage = drawerFunctions.pasteItem(backgroundImage, shadow, x, y)

        x, y = drawerFunctions.centerItem(backgroundImage.width, backgroundImage.height, window)
        backgroundImage = drawerFunctions.pasteItem(backgroundImage, window, x, y)
        
    return drawerFunctions.cropToRealSize(backgroundImage)

