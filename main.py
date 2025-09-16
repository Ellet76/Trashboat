import pygame as pg
pg.init()

window = pg.display.set_mode((640, 640))
pg.display.set_caption("Trash boat")
window_width = window.get_width()
window_height = window.get_height()

#colors
blue = (0, 64, 128)
white = (255, 255, 255)
dark_blue = (0, 50, 110)
black = (0, 0, 0)

#font
score_font = pg.font.Font("arial")
text_font = pg.font.Font("times new roman")
score = 0

#ritar ut brädet
def draw_board():
    for i in range(window_width):
        pg.draw.line(window, (0, 50, 110), (i * 40, 0), (i * 40, window_height))
    for i in range(window_height):
        pg.draw.line(window, (0, 50, 110), (0, i * 40), (window_width, i * 40))
    
    pg.draw.rect(window, (124,124,124), (0,0, 640, 40))
    pg.draw.rect(window, (124,124,124), ((0,560, 640, 560)))
    

run = True
while run:
    pg.display.update()

    window.fill(blue)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            run = False
    draw_board()






