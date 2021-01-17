import pygame as pg
import cv2 as c


def empty(a):
    pass


path = 'Source/cap.mp4'
cap = c.VideoCapture(0)
w, h = 720, 480


pg.init()
length, width = int(0.8*1920), int(0.8*1080)
screen = pg.display.set_mode((int(length),int(width)),pg.RESIZABLE)

pg.display.set_caption('draw')
clock = pg.time.Clock()

pg.draw.rect(screen, (255, 0, 0), (length/100, width/100, length/100, width/100))
pg.draw.rect(screen, (0, 0, 0), (length*(1-1/100), width/100, length/100, width/100))

loop = True
press = False
color = (0, 50, 0)

while True:

    success, img = cap.read()
    if not success:
        break

    img = c.resize(img, (w, h))
    lower_color_bounds = (240, 200, 200)
    upper_color_bounds = (255,255,255)
    mask = c.inRange(img,lower_color_bounds,upper_color_bounds)
    mask_rgb = c.cvtColor(mask,c.COLOR_GRAY2BGR)
    imgGray = c.cvtColor(mask_rgb, c.COLOR_BGR2GRAY)


    _, thresh = c.threshold(imgGray, 200, 255, c.THRESH_BINARY_INV)

    cnts, hierarchy = c.findContours(thresh, c.RETR_TREE, c.CHAIN_APPROX_NONE)
    if len(cnts)> 1:
        cnt = sorted(cnts, key=c.contourArea)
        c1 = cnts[1]
        (cX,cY),radius = c.minEnclosingCircle(c1)
        cX = int(cX)
        cY = int(cY)
        radius = int(radius)
        c.circle(img,(cX,cY),radius,(0,255,0),2)
        c.drawContours(img, c1, -1, (0, 255, 0), 1)

        try:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    loop = False

    #         px, py = pg.mouse.get_pos()
            px = int(cX*2.3) -50
            py = int((cY*2) -300)
            if pg.mouse.get_pressed() == (1,0,0):
                # quit button
                if px < length/100 and py < width/100:
                    pg.quit()
                pg.draw.circle(screen, color, (px, py), 10, 10)
            if event.type == pg.MOUSEBUTTONUP:
                press == False
            pg.display.update()
            clock.tick(1000)
        except Exception as e:
            print(e)
            pg.quit()
pg.quit()
