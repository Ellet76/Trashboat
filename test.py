import pygame as pg
pg.init()


window_width = 640
window_height = 640
window = pg.display.set_mode((window_width, window_height))
pg.display.set_caption("Trash boat")

blue = (0, 64, 128)


def draw():
    window.fill(blue)


run = True
while run:
    draw()
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            run = False
    


