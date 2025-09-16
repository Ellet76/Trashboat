import pygame as pg
pg.init()

window = pg.display.set_mode((640, 640))
pg.display.set_caption("Trash boat")

blue = (0, 64, 128)
window.fill(blue)


run = True
while run:
    pg.display.update()
    window.fill(blue)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            run = False
    pg.draw.rect(window, (124,124,124), (0,0, 640, 40))
    pg.draw.rect(window, (124,124,124), ((0,560, 640, 560)))



