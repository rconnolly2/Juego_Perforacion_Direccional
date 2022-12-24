import pygame
import math

class Perforacion:
    def __init__(self, dimension_ventana: tuple, color_tierra: tuple, color_cielo: tuple, titulo_ventana: str):
        self.dimension_ventana = dimension_ventana
        self.color_tierra = color_tierra
        self.color_cielo = color_cielo
        self.titulo_ventana = titulo_ventana
        self.pantalla = None
        self.running = True
        self.postaladro = [50, 240]
        self.angulo_prueba = 0
        self.angulo_taladro = 0
        self.taladro = pygame.image.load("taladro.png")
        self.taladro_vector = pygame.Vector2(6, 0)
        self.clock = pygame.time.Clock()
        self.lista_puntos_camino = []
        self.direccion = 1
        self.tierra_img = pygame.image.load("tierra.png")
        self.hdd_img = pygame.image.load("hdd.png")
        self.hdd_pos = (0, 150)

    def Inicio_Juego(self):
        pygame.display.set_caption(self.titulo_ventana)

        try:
            self.pantalla = pygame.display.set_mode(self.dimension_ventana)
        except:
            print("Error: parametro dimension_ventana no es valido al crear el objeto")

    

    def Dibujar_Fondo(self, pantalla):
        #Primero dibujamos la tierra:
        pantalla.blit(self.tierra_img, (0, 250))
        #Luego el lago encima de la tierra
        pygame.draw.ellipse(pantalla, (0, 45, 243), (((self.dimension_ventana[0]/2)-(200/2)), (self.dimension_ventana[1]/2-70), 200, 150))
        #Ahora el cielo:
        try:
            pygame.draw.rect(pantalla, self.color_cielo, (0, 0, self.dimension_ventana[0], self.dimension_ventana[1]/2))
        except:
            print("Error: parametro color_cielo no es valido al crear el objeto")

        #Dibujamos el hdd:
        pantalla.blit(self.hdd_img, self.hdd_pos)


    def Rotar_Centro(imagen, angulo, x, y):
        imagen_rotada = pygame.transform.rotate(imagen, angulo)
        nuevo_rect = imagen_rotada.get_rect(center = imagen.get_rect(center = (x, y)).center)

        return imagen_rotada, nuevo_rect

    def Pintar_Camino(self, lista_de_puntos, pantalla):
        
        iterador = 0
        for puntos in lista_de_puntos:
            x = puntos[0]
            y = puntos[1]
            if iterador == 0:
                None
            
            else:
                xfinal = lista_de_puntos[iterador-1][0]
                yfinal = lista_de_puntos[iterador-1][1]
                pygame.draw.line(pantalla, (255, 0, 0), (x, y), (xfinal, yfinal), 2)
                

            iterador = iterador+1
            

    def Bucle_Juego(self):
        while self.running == True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.running = False

                #Miramos si se presiona q si se presiona invertimos la rotacion:
                if evento.type == pygame.KEYUP:
                    self.direccion = self.direccion*-1

            #Pintamos fondo:
            self.Dibujar_Fondo(self.pantalla)

            if self.angulo_taladro > 6.28:
                self.angulo_taladro = 0
            self.angulo_taladro = self.angulo_taladro+0.057*self.direccion
            #nuevo_vector = self.taladro_vector.rotate(self.angulo_taladro) Funcion vector
            nuevo_vector = [None, None]
            nuevo_vector[0] = (((self.taladro_vector[0]*math.cos(self.angulo_taladro)) - (self.taladro_vector[1]*math.sin(self.angulo_taladro))))
            nuevo_vector[1] = (((self.taladro_vector[0]*math.sin(self.angulo_taladro)) + (self.taladro_vector[1]*math.cos(self.angulo_taladro))))


            print(nuevo_vector)
            #self.postaladro[0] += 1
            if self.postaladro[0] >= 400:
                self.postaladro[0] = 1

            if self.angulo_prueba > 360:
                self.angulo_prueba = 0

            self.postaladro[0] = self.postaladro[0]  + nuevo_vector[0]
            self.postaladro[1] = self.postaladro[1] + nuevo_vector[1]

            #Añadimos nueva posicion de camino a nustra lista de puntos del camino :
            self.lista_puntos_camino.append([self.postaladro[0], self.postaladro[1]])

            #self.pantalla.fill(self.color_tierra)

            #Pìnto lista camino:
            self.Pintar_Camino(self.lista_puntos_camino, self.pantalla)

            # Añadimos un grado cada llamada
            self.angulo_prueba = self.angulo_prueba + 1.6*self.direccion
            #Añadimos mas angulo para que parezca una escavadora:

            # Almacenamos la imagen rotada en una nueva imagen ya que sino se distorsiona
            taladro_rot = pygame.transform.rotate(self.taladro, self.angulo_prueba+(28.6*self.direccion))
            rect_taladro_rot = taladro_rot.get_rect()
            pygame.Surface.set_colorkey (taladro_rot, [105,255,0])
            self.pantalla.blit(taladro_rot, (self.postaladro[0]-(rect_taladro_rot.width/2), self.postaladro[1]-(rect_taladro_rot.height/2)))
            
            pygame.display.flip()
            self.clock.tick(15)
            

        #Limpiando pygame
        pygame.quit()
        



juego = Perforacion((500, 500), (155, 102, 72), (208, 253, 255), "Juego perforacion direccional")
juego.Inicio_Juego()
juego.Bucle_Juego()