from tkinter import *

import tkinter as tk

from math import *

import numpy as np

 

#Klass för objekten. Den behöver inte ärva några attribut.

class Body():

    #Konstruktor

    def __init__(self, can_bredd, can_höjd, namn):

        #Storleksfaktor och distans från "kameran"

        self.scale = 750

        self.distance = 8

        #Hur mycket objekten ska förstoras.

        self.factor = 0

        #De färger som objekten kan ha. Objekts sidor har olika färger.

        self.colors = ['blue', 'cyan', 'yellow', 'red', 'orange', 'purple']

        #Objektets namn

        self.namn = namn

 

        #Bredd och höjd på fönstret som öppnas

        self.can_bredd, self.can_höjd = can_bredd, can_höjd

        # "Kamerans" position i koordinatform. Är inte projecerade.

        self.camera_point = [[0, 0, 8]]

        #Hur mycket ojektet är förskjutet i sid- och höjd- och djupled.

        self.x_offset = 0

        self.y_offset = 0

        self.z_offset = 0

        #Om objektet är aktivt. Exempelvis om muspekaren hoovrar över.

        self.active = False

       

        #Objektets punkter. Är inte projecerade.

        self.cube_vertices = [

            #Mittpunkt är sist i listan.

            [-1,-1,-1], #0

            [1,-1,-1],  #1

            [1,1,-1],   #2

            [-1,1,-1],  #3

            [-1,-1,1],  #4

            [1,-1,1],   #5

            [1,1,1],    #6

            [-1,1,1],   #7

            [-1,0,0],   #8 - Center point (Yellow side)

            [0,0,-1],   #9 - Center point (Blue side)

            [1,0,0],   #10 - Center point (Right side)

            [0,-1,0],  #11 - Center point (Top side)

            [0,1,0],   #12 - Center point (Top side)

            [0,0,1],   #13 - Center point (Top side)

            [0,0,0],   #15 - Center point

 

 

        #objektets culling-punkter i koordinatform, inte projecerade.. Alltså punkterna som sitter smått förskjutet på varje objektets sida som används för att avgöra om sidan ska "ritas" av programmet eller inte.

        ]

        self.cube_culling_points = [

            [-1.01,0,0, 8], # 0 - Culling point to vertice 8

            [0,0,-1.01, 9], # 1 - Culling point to vertice 9

            [1.01,0,0, 10], # 2 - Culling point to vertice 10

            [0,-1.01,0, 11],# 3 - Culling point to vertice 11

            [0,1.01,0, 12], # 4 - Culling point to vertice 12

            [0,0,1.01, 13],

        #Objektets kanter i koordinatform, inte projecerade.

        ]

        self.cube_edges = [

                                                                                  [0, 1], #Vertex 0 to Vertex 1

                                                                                  [1, 2], #Vertex 1 to Vertex 2

                                                                                  [2, 3], #Vertex 2 to Vertex 3

                                                                                  [3, 0], #...

                                                                                  [4, 5],

                                                                                  [5, 6],

                                                                                  [6, 7],

                                                                                  [7, 4],

                                                                                  [0, 4],

                                                                                  [1, 5],

                                                                                  [2, 6],

                                                                                  [3, 7],

            [8, 9]

                                                      ]

        #Objektets sidor i koordinatform, inte projecerade.

        self.cube_sides = [

            [3,0,1,2, 1],

            [0,3,7,4, 0],

            [1,0,4,5, 3],

            [3,2,6,7, 4],

            [4,5,6,7, 5],

            [2,1,5,6, 2]

           

        ]

        #Vilka vinkal som objektet är roterade.

        self.angle_x = 0

        self.angle_y = 0

        self.angle_z = 0

        #Lista med objektets roterade punkter med avseende på vinklarna. Inte projecerade.

        self.rotated_points, self.rotated_culling_points = [],[]

        #Lista med objektets punkter som är projecerade.

        self.projected_points = []

 

    #Roterar med avseende på vinkeln kring x-axeln.

    def rotation_x(self, angle):

        rad = radians(angle)

        return [

            [1, 0, 0],

            [0, cos(rad), -sin(rad)],

            [0, sin(rad), cos(rad)]

        ]

    def rotation_y(self, angle): #Roterar med avseende på vinkeln kring y-axeln.

        rad = radians(angle)

        return [

            [cos(rad), 0, sin(rad)],

            [0, 1,0],

            [-sin(rad), 0, cos(rad)]

        ]

    def rotation_z(self, angle): #Roterar med avseende på vinkeln kring z-axeln.

        rad = radians(angle)

        return [

            [cos(rad), -sin(rad), 0],

            [sin(rad), cos(rad), 0],

            [0, 0, 1]

        ]

    #Transofmerar punkter. Alltså förskjutning i sid- och höjdled.

    def transformation_matrix(self, dx, dy, dz):

        return [

            [1, 0, 0, dx],

            [0, 1, 0, dy],

            [0, 0, 1, dz],

            [0, 0, 0, 2]

        ]

   

    

    #Projecerar koordinater. Alltså omvandlar objektets egna koordinater till koordinater relativa till "världen".

    def project_a_point(self, x, y, z):

        if z >= 8:

            z =7.999

        self.factor = self.scale / (self.distance - z)

        px = x * self.factor + self.can_bredd / 2

        py = y * self.factor + self.can_höjd / 2

        return [px, py]

    #Beräknar vinkeln på ett objekts sida. Används för att avgöra om sidan ska "ritas" av programmet.

    def cull(self, culling_point, point):

        x1 = point[0] - culling_point[0]

        y1 = point[1] - culling_point[1]

        z1 = point[2] - culling_point[2]

 

        x2 = self.camera_point[0][0] - culling_point[0]

        y2 = self.camera_point[0][1] - culling_point[1]

        z2 = self.camera_point[0][2] - culling_point[2]

       

        v1 = [x1, y1, z1]

        v2 = [x2, y2, z2]

        abs_v1 = sqrt(x1 ** 2 + y1 ** 2 + z1 ** 2)

        abs_v2 = sqrt(x2 ** 2 + y2 ** 2 + z2 ** 2)

       

        temp =  np.dot(v1, v2)

 

        if np.dot(v1, v2) / (abs_v1 * abs_v2) >= 1:

            temp = (abs_v1 * abs_v2) - 0.1

        elif np.dot(v1, v2) / (abs_v1 * abs_v2) <= -1 and np.dot(v1, v2) < 0:

            temp = (abs_v1 * abs_v2) - 0.1

            pass

        elif np.dot(v1, v2) / (abs_v1 * abs_v2) <= -1 and (abs_v1 * abs_v2) < 0:

            temp =(abs_v1 * abs_v2) + 0.1

 

        angle = acos(temp / (abs_v1 * abs_v2))

        angle = degrees(angle)

   

        return angle

    #Uppdaterar objektets koordinater.

    def update(self):

        self.rotated_points, self.rotated_culling_points = self.project_body()

        self.projected_points = [self.project_a_point(x, y, z) for x, y, z in self.rotated_points]

 

 

    #Gör alla rotationer och projektioner.

    def project_body(self):

        self.rotated_points = []

        self.rotated_culling_points = []

        for point in self.cube_vertices:

            self.rotated_points.append(self.rotera_med_avseende_på_kamera(point))

 

        for point in self.cube_culling_points:

            temp = [point[0], point[1], point[2]]

            self.rotated_culling_points.append(self.rotera_med_avseende_på_kamera(temp))

       

        four_by_one_matrices_1 = []

        four_by_one_matrices_2 = []

       

        for i in range(len(self.rotated_points)):

            self.rotated_points[i] = (self.transomfera_med_avseende_på_kamera(self.rotated_points[i]))

        for i in range(len(self.rotated_culling_points)):

            self.rotated_culling_points[i] = (self.transomfera_med_avseende_på_kamera(self.rotated_culling_points[i]))

        return self.rotated_points, self.rotated_culling_points

    #Transformerar.

    def transomfera_med_avseende_på_kamera(self, punkt):

        p1 = punkt[0]

        p2 = punkt[1]

        p3 = punkt[2]

               

        four_by_one_matrices_1 = []

       

        four_by_one_matrices_1.append([p1, p2 ,p3, 1])

       

        transformerad_punkt = np.dot(self.transformation_matrix(self.x_offset, self.y_offset, self.z_offset), four_by_one_matrices_1[0])

        pt1 = transformerad_punkt[0]

        pt2 = transformerad_punkt[1]

        pt3 = transformerad_punkt[2]

       

        return pt1, pt2, pt3

   

    #Roterar med avseende på kamerarn.

    def rotera_med_avseende_på_kamera(self, punkt):

        x2 = punkt[0] + self.x_offset

        y2 = punkt[1] + self.y_offset

        z2 = punkt[2] + (self.z_offset - 8)

       

        z_rot = np.dot([x2, y2, z2], self.rotation_z(self.angle_z))

        y_rot = np.dot(z_rot, self.rotation_y(self.angle_y))

        x_rot = np.dot(y_rot, self.rotation_x(self.angle_x))

 

        x_rot[0] -= self.x_offset

        x_rot[1] -= self.y_offset

        x_rot[2] -= (self.z_offset - 8)

 

        return x_rot

#Klass för "världen". Alltså utrymmet där objekten existerar relativt till varandra.

class Root(Tk):

    def __init__(self):

        #Ärver attribut från Tkinter.

        super().__init__()

        #Gränssnittets titel och status.

        self.title('Slutuppgift')

        self.state('zoomed')

        #Färg på objekts som är muspekaren hoovrar över.

        self.hover_färg = 'cyan'

        #Vinklar på kameran.

        self.camera_angle_x = 0

        self.camera_angle_y = 0

        self.camera_angle_z = 0

        #Initierar gränssnittet där objekten kan ritas ut.

        self.canvas = Canvas(self,bg='#ffffff')

        self.canvas.pack(fill = 'both', expand = 1)

        #Uppdaterar gränssnittet.

        self.canvas.update()

        #Lista med objekt.

        self.bodies = []

        #Objekt nummer 1 är aktivt från början.

        self.active_body = 1

        #Lista med knappar.

        self.buttons = []

        #Initerar knapparna med deras funktion och lägger till i listan.

        self.button1 = tk.Button(self,text = "Avmarkera allt.", command = self.avmarkera)

        self.button2 = tk.Button(self, text = "Radera objekt", command = self.radera_objekt)

        self.button3 = tk.Button(self, text = 'Lägg till objekt', command = self.skapa_objekt)

        self.button_markera_alla = tk.Button(self, text = 'Markera allt.', command = self.markera_allt)

        self.button_omstart = tk.Button(self, text = 'Omstart', command = self.omstart)

        self.buttons.extend([self.button_markera_alla, self.button1, self.button2, self.button3, self.button_omstart])

        for i in range(len(self.buttons)):

            self.buttons[i].place(x = i * 120 + (self.canvas.winfo_width() // 2 - 100), y = 100)

       

    #Ritar ut alla objekt.

    def draw(self):

        self.canvas.delete('all')

        #self.canvas.create_polygon(0, 400,  0, self.canvas.winfo_height(), self.canvas.winfo_width(), self.canvas.winfo_height(),self.canvas.winfo_width(), 400, fill='darkgray')

        for i in range(len(self.bodies) - 1):

            if self.bodies[i].factor > self.bodies[i+1].factor and self.bodies[i].namn != 'grund':

                self.bodies.insert(i+1, self.bodies.pop(i))

           

            if self.bodies[i].namn == 'grund':

                self.bodies.insert(0, self.bodies.pop(i))

       

        for body in self.bodies:

            body.update()

            #Triangles

            color = 0

           

            for side in body.cube_sides:

                if body.cull(body.rotated_culling_points[side[-1]], body.rotated_points[body.cube_culling_points[side[-1]][3]]) >= 90:

                    p1 = body.projected_points[side[0]]

                    p2 = body.projected_points[side[1]]

                    p3 = body.projected_points[side[2]]

                    if len(side) > 4:

                        p4 = body.projected_points[side[3]]

                        if body.namn != 'grund':

                            self.canvas.create_polygon(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], p4[0], p4[1], fill=body.colors[color])

                    else:

                        self.canvas.create_polygon(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], fill=body.colors[color])

                    for item in self.bodies:

                        if body.active:

                            self.canvas.create_oval(body.projected_points[-1][0] - 10, body.projected_points[-1][1] - 10, body.projected_points[-1][0] + 10, body.projected_points[-1][1]+ 10, fill='black')

                    if body.namn == 'grund':

                        for i in range(3, len(body.projected_points[5:]), 2):

                            self.canvas.create_line(body.projected_points[i][0], body.projected_points[i][1],body.projected_points[i-1][0], body.projected_points[i-1][1])

                color += 1 if color < len(body.colors) - 1 else 0

 

       

        

            self.canvas.create_text(body.projected_points[-1][0], body.projected_points[-1][1] + 16, text = f'({round(body.projected_points[-1][0], None)}, {round(body.projected_points[-1][1], None)})')

        for body in self.bodies:

            if body.namn == 'kub_1':

                self.canvas.create_text(110, 50, font = ('Comic Sans MS', 12), text= f'camera: {sin(radians(self.camera_angle_y))}°')

                self.canvas.create_text(110, 70, font = ('Comic Sans MS', 12), text= f'camera: {self.camera_angle_y}°')

                self.canvas.create_text(110, 90, font = ('Comic Sans MS', 12), text= f'body y: {sin(radians(body.angle_y))}°')

                self.canvas.create_text(110, 110, font = ('Comic Sans MS', 12), text= f'body y: {body.angle_y}°')

                self.canvas.create_text(110, 130, font = ('Comic Sans MS', 12), text= f'body x: {sin(radians(body.angle_x))}°')

                self.canvas.create_text(110, 150, font = ('Comic Sans MS', 12), text= f'body x: {body.angle_x}°')

                self.canvas.create_text(110, 170, font = ('Comic Sans MS', 12), text= f'body z: {sin(radians(body.angle_z))}°')

                self.canvas.create_text(110, 190, font = ('Comic Sans MS', 12), text= f'body z: {body.angle_z}°')

                self.canvas.create_text(110, 220, font = ('Comic Sans MS', 12), text= f'offset z: {body.factor}°')

            if body.namn == 'kub_2':

                self.canvas.create_text(110, 250, font = ('Comic Sans MS', 12), text= f'offset z: {body.factor}°')

 

        self.canvas.create_text(110, 280, font = ('Comic Sans MS', 12), text= f'offset z: {self.bodies[-1].namn}°')

 

 

 

       

    #Återställer programmet om den knappen trycks på.

    def omstart(self):

        self.bodies = []

        self.snabbval_grund()

        self.camera_angle_x, self.camera_angle_y, self.camera_angle_z = 0,0,0

        self.draw()

    #Undersöker vilka tangenter som tryckts på och ändrar sedan på de aktiva objektens vinklar och position.

    def animate_cube(self, event):

        for body in self.bodies:

            if body.active:

                char = event.char

                if char == 'w':

                    body.angle_x -= 1

                    self.camera_angle_x = body.angle_x

                elif char == 't':

                    pass

 

                elif char == 's':

                    body.angle_x += 1

                    self.camera_angle_x = body.angle_x

                   

                elif char == 'd':

                    body.angle_y -= 1

                    self.camera_angle_y = body.angle_y

                   

                elif char == 'a':

                    body.angle_y += 1

                    self.camera_angle_y = body.angle_y

                   

                elif char == ' ':

                    body.angle_z += 1

                elif char == 'm':

                    body.angle_z -= 1

               

                elif char == 'Up':

                    body.x_offset += 0.1

                elif event.keysym == 'Right':

                    body.x_offset -=  cos(radians(self.camera_angle_y)) * 0.1

                    body.z_offset += sin(radians(self.camera_angle_y)) * 0.1

                elif event.keysym == 'Up':

                    body.y_offset += 0.1

 

                elif event.keysym == 'Left':

                    body.x_offset += cos(radians(self.camera_angle_y)) * 0.1

                    body.z_offset -= sin(radians(self.camera_angle_y)) * 0.1

                elif event.keysym == 'Down':

                    body.y_offset -= 0.1

                elif event.char == 'z':

                    body.z_offset -=  cos(radians(self.camera_angle_y)) * 0.1

                    body.x_offset -= sin(radians(self.camera_angle_y)) * 0.1

        self.draw()

    #Ändrar färg på objekt som muspekaren hoovrar över.

    def hover(self, mus_koordinat):

        if self.rayCast(mus_koordinat)[0]:

            for body in self.bodies:

                body.colors = ['blue', 'cyan', 'yellow', 'red', 'orange', 'purple']

            self.rayCast(mus_koordinat)[1].colors = [self.hover_färg]

        self.draw()

    #Gör objekt aktiva om de klickas på med muspekaren. Raderar objekt om den knappen tryckts på.

    def klicka_på_objekt(self):

        for body in self.bodies:

            body.active = False

            if body.colors[0] == 'cyan':

                    body.active = True

            elif body.colors[0] == 'red':

                self.bodies.remove(body)

                self.button2.config(bg = '#f0f0f0')

            body.colors = ['blue', 'cyan', 'yellow', 'red', 'orange', 'purple']

 

 

    #Kallar på "klicka_på_objekt" och återställer hoover-färgen.

    def mus_tryck(self):

        vänster_klick = True

        self.klicka_på_objekt()

        self.hover_färg = 'cyan'

        self.draw()

 

    #Matematiskt undersöker om muspekaren position är mot- eller medurs orienterat jämfört med något objekts sida.

    def counterClockwise(self, a, b, c):

        x_diff_1 = b[0] - a[0]

        x_diff_2 = c[0] - a[0]

 

        if x_diff_1 == 0:

            x_diff_1 += 0.01

        if x_diff_2 == 0:

            x_diff_2 += 0.01

        k_värde_ab = (b[1] - a[1]) / (x_diff_1)

        k_värde_ac = (c[1] - a[1]) / (x_diff_2)

        return k_värde_ab < k_värde_ac

    #Använder ray-casting för att undersöka om muspekarens position är inom ett objekt. Utnyttjar ovan metod.

    def rayCast(self, mouse_coordinate):

        count = 0

        for body in self.bodies:

            body.update()

            for side in body.cube_sides:

                p1, p2, p3 = body.projected_points[side[0]], body.projected_points[side[1]], body.projected_points[side[2]]

                if len(side) > 3:

                    p4 = body.projected_points[side[3]]

                    linjer = [[p1, p2], [p1, p4], [p3, p2], [p3, p4]]

                    for linje in linjer:

                        if self.counterClockwise(linje[0], linje[1], [0, mouse_coordinate[1]]) != self.counterClockwise(linje[0], linje[1], mouse_coordinate) and self.counterClockwise([0, mouse_coordinate[1]], mouse_coordinate, linje[0]) != self.counterClockwise([0, mouse_coordinate[1]], mouse_coordinate, linje[1]):

                            return [True, body]

                elif len(side) <= 3:

                    p4 = [(p3[0]-p1[0]) // 2, (p3[1]-p1[0]) // 2]

                    linjer = [[p1, p2], [p1, p4], [p3, p2], [p3, p4]]

                    for linje in linjer:

                        if self.counterClockwise(linje[0], linje[1], [0, mouse_coordinate[1]]) != self.counterClockwise(linje[0], linje[1], mouse_coordinate) and self.counterClockwise([0, mouse_coordinate[1]], mouse_coordinate, linje[0]) != self.counterClockwise([0, mouse_coordinate[1]], mouse_coordinate, linje[1]):

                            return [True, body]

        return [False, None]

    #Avmarkerar alla objekt. Alltså gör dem inaktiva.

    def avmarkera(self):

        for body in self.bodies:

            body.colors = ['blue', 'cyan', 'yellow', 'red', 'orange', 'purple']

        self.draw()

    #Raderar objekt som klickas på.

    def radera_objekt(self):

        self.avmarkera()

        self.hover_färg = 'red'

        self.button2.config(bg = '#656565')

    #Skapar skuggor. Används inte i programmet då metoden inte är färdigställd.

    def skuggor(self):

        grund = Body(self.canvas.winfo_width(), self.canvas.winfo_height(), 'skugga')

       

        punkter = [

            [-3, 9, -3],#0

            [-3, 9, 3],   #1

            [3, 9, -3], #2

            [3, 9, 3],    #3

        ]

        punkter.append([0, 9, 0])

 

 

        kanter = [

            [0, 1],

            [0, 2],

            [1, 3],

            [2, 3]

        ]

       

        sidor = [

            [0, 1, 3, 2, 0]

        ]

       

        culling_punkter = [

            [0, 8.9, 0, -1]

        ]

       

        grund.cube_edges = kanter

        grund.cube_sides = sidor

        grund.cube_vertices = punkter

        grund.cube_culling_points = culling_punkter

        grund.colors = ['darkgray']

        grund.z_offset = 0.1

        grund.active = True

        self.bodies.append(grund)

    #Skapar objekt beroende på vilken knapp som i programmet tryckts på.

    def skapa_objekt(self):

        b3 = self.button3

        button3_1 = tk.Button(self, text = 'Kub', command = self.snabbval_kub)

        button3_2 = tk.Button(self, text = 'Pyramid', command = self.snabbval_pyramid)

        button3_3 = tk.Button(self, text = 'Grund', command = self.snabbval_grund)

        button3_4 = tk.Button(self, text = 'Vägg', command = self.snabbval_vägg)

 

        button3_1.place(x = b3.winfo_x() + b3.winfo_width() // 2, y = b3.winfo_y() + 30)

        button3_2.place(x = b3.winfo_x() + b3.winfo_width() // 2, y = b3.winfo_y() + 57)

        button3_3.place(x = b3.winfo_x() + b3.winfo_width() // 2, y = b3.winfo_y() + 84)

        button3_4.place(x = b3.winfo_x() + b3.winfo_width() // 2, y = b3.winfo_y() + 111)

 

       

        self.buttons.extend([button3_1, button3_2, button3_3])

    #Skapar och lägger till en kub i programmet.

    def snabbval_kub(self):

        self.bodies.append(Body(self.canvas.winfo_width(), self.canvas.winfo_height(), f'ny_kropp_{len(self.bodies) + 1}'))

        self.bodies[-1].scale = 750

    #Skapar och lägger till en vägg i programmet.

    def snabbval_vägg(self):

        vägg = Body(self.canvas.winfo_width(), self.canvas.winfo_height(), f'ny_kropp_{len(self.bodies) + 1}')

        punkter = [

            #Mittpunkt sist i listan.

            [-0.2,-1,-4], #0

            [0.2,-1,-4],  #1

            [0.2,1,-4],   #2

            [-0.2,1,-4],  #3

            [-0.2,-1,1],  #4

            [0.2,-1,1],   #5

            [0.2,1,1],    #6

            [-0.2,1,1],   #7

            [-0.2,0,0],   #8 - Center point (Yellow side)

            [0,0,-4],   #9 - Center point (Blue side)

            [0.2,0,0],   #10 - Center point (Right side)

            [0,-1,0],  #11 - Center point (Top side)

            [0,1,0],   #12 - Center point (Top side)

            [0,0,1],   #13 - Center point (Top side)

            [0,0,0],   #15 - Center point

 

 

 

        ]

        culling_punkter = [

            [-0.21,0,0, 8], # 0 - Culling point to vertice 8

            [0,0,-4.01, 9], # 1 - Culling point to vertice 9

            [0.21,0,0, 10], # 2 - Culling point to vertice 10

            [0,-1.01,0, 11],# 3 - Culling point to vertice 11

            [0,1.01,0, 12], # 4 - Culling point to vertice 12

            [0,0,1.01, 13],

 

        ]

        kanter = [

                                                                                  [0, 1], #Vertex 0 to Vertex 1

                                                                                  [1, 2], #Vertex 1 to Vertex 2

                                                                                  [2, 3], #Vertex 2 to Vertex 3

                                                                                  [3, 0],

                                                                                  [4, 5],

                                                                                  [5, 6],

                                                                                  [6, 7],

                                                                                  [7, 4],

                                                                                  [0, 4],

                                                                                  [1, 5],

                                                                                  [2, 6],

                                                                                  [3, 7],

            [8, 9]

                                                      ]

 

        sidor = [

            [3,0,1,2, 1],

            [0,3,7,4, 0],

            [1,0,4,5, 3],

            [3,2,6,7, 4],

            [4,5,6,7, 5],

            [2,1,5,6, 2]

           

        ]

        vägg.cube_vertices = punkter

        vägg.cube_sides = sidor

        vägg.cube_culling_points = culling_punkter

        vägg.cube_edges = kanter

        vägg.colors = ['blue', 'cyan', 'orange', 'red', 'yellow', 'purple']

 

        self.bodies.append(vägg)

        #self.bodies[-1].scale = 750

        self.buttons[-1].config(bg='black')

        self.buttons[-1].destroy()

        self.buttons[-2].destroy()

        self.buttons[-3].destroy()

 

        for i in range(2):

            self.buttons.pop()

    #Skapar och lägger till en pyramid i programmet.

    def snabbval_pyramid(self):

        pyramid = Body(self.canvas.winfo_width(), self.canvas.winfo_height(), f'ny_kropp_{len(self.bodies) + 1}')

        punkter = [

            [0, -1, 0], #0

            [-1, 1, -1],#1

            [-1, 1, 1], #2

            [1, 1, -1], #3

            [1, 1, 1],  #4

            [0.49, 0, 0], #5 Mittpunkt höger

            [-0.49, 0, 0],#6 Mittpunkt vänster

            [0, 0, 0.49], #7 Mittpunkt fram

            [0, 0, -0.49],#8 Mittpunkt bak

            [0, 1, 0]    #9 Mittpunkt ned

        ]

       

        kanter = [

            [0, 1],

            [0, 2],

            [0, 3],

            [0, 4],

            [1, 2],

            [1, 3],

            [2, 4],

            [3, 4]

        ]

       

        sidor = [

            [0, 2, 1, 1],

            [1, 0, 3, 3],

            [0, 2, 4, 2],

            [0, 3, 4, 0],

            [2, 1, 3, 4, 4]

        ]

        culling_punkter = [

            [0.51, -0.01, 0, 5],

            [-0.51, -0.01, 0, 6],

            [0, -0.01, 0.51, 7],

            [0, -0.01, -0.51, 8],

            [0, 1.01, 0, 9]   

        ]

        pyramid.cube_vertices = punkter

        pyramid.cube_sides = sidor

        pyramid.cube_culling_points = culling_punkter

        pyramid.cube_edges = kanter

        pyramid.colors = ['blue', 'cyan', 'orange', 'red', 'yellow', 'purple']

       

        self.bodies.append(pyramid)

        self.buttons[-1].config(bg='black')

        self.buttons[-1].destroy()

        self.buttons[-2].destroy()

        for i in range(2):

            self.buttons.pop()

 

    #Skapar och lägger till en grund i programmet.

    def snabbval_grund(self):

        grund = Body(self.canvas.winfo_width(), self.canvas.winfo_height(), 'grund')

       

        punkter = [

            [-30, 10, -30],#0

            [-30, 10, 30],   #1

            [30, 10, -30], #2

            [30, 10, 30],    #3

        ]

        for i in range(0,33, 2):

            punkter.extend([[-30 + 2 * i, 10, -30]])

            punkter.extend([[-30 + 2 * i, 10, 30]])

        punkter.append([0, 10, 8])

 

 

        kanter = [

            [0, 1],

            [0, 2],

            [1, 3],

            [2, 3]

        ]

       

        sidor = [

            [0, 1, 3, 2, 0]

        ]

       

        culling_punkter = [

            [0, 9.99, 8, -1]

        ]

       

        grund.cube_edges = kanter

        grund.cube_sides = sidor

        grund.cube_vertices = punkter

        grund.cube_culling_points = culling_punkter

        grund.colors = ['gray']

        grund.z_offset = 0.1

        self.bodies.insert(0, grund)

        self.draw()

    #Markerar alla objekt.

    def markera_allt(self):

        for body in self.bodies:

                body.active = True

        self.draw()

 

#Kallar på animate_cube varje gång programmet uppdateras.

def check_event(event):

    root.animate_cube(event)

#För att kunna kombinera "control"-tangenten med andra tangenten.

def control(event):

    for body in root.bodies:

        body.z_offset +=  cos(radians(root.camera_angle_y)) * 0.1

        body.x_offset += sin(radians(root.camera_angle_y)) * 0.1

    root.draw()

#Kallar på hoover-metoden och skickar med muspekarens koordinater som argument.

def mouse(event):

    root.hover([event.x, event.y])

#Kallar på mus_tryck.

def mus_tryck(event):

    root.mus_tryck()

#Main-programmet. Loopas med Tkinters mainloop.

if __name__ == '__main__':

    root = Root()

    root.bind('<KeyPress>', check_event)

    root.bind('<Control-Key-z>', control)

    root.bind('<Motion>', mouse)

    root.bind('<Button-1>', mus_tryck)

    root.mainloop()

 

 

 

#Problem med ineffektiv matrismultiplicering. Byttes ut till en importerad funktion med Numpy.

'''def multiply_matrices(self, m1, m2):

    product = []

    k = 0

    for i in range(len(m2)):

        sum = 0

        for j in range(len(m1)):

            sum += round(m1[j], 3) * round(m2[j][i], 3)

            print('Sum: ', sum)

        product.append(sum)

    print('P: ',product)

    print('Len P: ', len(product))

    return product

                '''