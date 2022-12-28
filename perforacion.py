import pygame
import math
import random
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
        self.hdd_pos = (0, 150)
        #Fotograma animacion
        self.hdd_img = None
        self.fotograma = 0
        self.timer_animacion = 0
        #Obstaculos
        self.obstaculo_img = pygame.image.load("obstaculo.png")
        self.lista_pos_obstaculos = []
        self.obstaculos_visibles = []
        #Objetivo
        self.objetivo = pygame.image.load("goal.png")
        #Texto
        #Inicio de pygame para fuentes que lo requiere:
        pygame.init()
        self.fuente = pygame.font.Font(pygame.font.get_default_font(), 36)

    def Inicio_Juego(self):
        pygame.display.set_caption(self.titulo_ventana)

        try:
            self.pantalla = pygame.display.set_mode(self.dimension_ventana)
        except:
            print("Error: parametro dimension_ventana no es valido al crear el objeto")

        self.Crear_Obstaculos(self.pantalla, 10, self.lista_pos_obstaculos)

    def End_Screen(self, ganas: bool, pantalla):
        texto_ganas = "Has Ganado!"
        texto_pierdes = "Has Perdido!"
        pos_texto = (self.dimension_ventana[0]/2-120, self.dimension_ventana[0]/2) #Centro pantalla
        
        if ganas == False:
            pantalla.fill((255, 115, 115))
            text_surface = self.fuente.render(texto_pierdes, True, (0, 0, 0))
            #Dibujamos el texto en el centro de la pantalla:
            self.pantalla.blit(text_surface, pos_texto)
            pygame.display.flip()
            pygame.time.delay(1000)
            self.running = False
            return self.Bucle_Juego() #Volvemos a la funcion bucle para que se acabe el juego

        if ganas == True:
            pantalla.fill((202, 255, 115))
            text_surface = self.fuente.render(texto_ganas, True, (0, 0, 0))
            #Dibujamos el texto en el centro de la pantalla:
            self.pantalla.blit(text_surface, pos_texto)
            pygame.display.flip()
            pygame.time.delay(1000)
            self.running = False
            return self.Bucle_Juego() #Volvemos a la funcion bucle para que se acabe el juego

    def Taladro_Dentro_Lago(self, pos_taladro: list, centro_circulo: list, radio_circulo: int):
        """
        Esta funcion coge la posicion de taladro y el centro del circulo y si
        es inferior al radio del circulo radio_cirulo el juego se acaba

        pos_taladro => La posicion del taladro ej [x, y]

        centro_circulo => La posicion central del circulo ej [x, y]

        radio_circulo => El radio del circulo ej: 6

        """
        x1 = pos_taladro[0]
        y1 = pos_taladro[1]

        x2 = centro_circulo[0]
        y2 = centro_circulo[1]

        #Si el taladro entra al radio del circulo "colisiona" se acaba el juego
        if self.Distancia_Entre_2_Puntos(x1, y1, x2, y2) < radio_circulo:
            self.running = False

    def Imprimir_Objetivo(self, pantalla, imagen_objetivo, pos_taladro):
        pos_objetivo = [self.dimension_ventana[0]-100, self.dimension_ventana[1]/2-10]
        #Consigue el ancho del objetivo de la imagen
        ancho_objetivo = imagen_objetivo.get_rect().width
        
        #Primero Imprimimos el objetivo en la misma posicion:
        imagen_objetivo.set_colorkey((54,255,0))
        pantalla.blit(imagen_objetivo, (pos_objetivo[0], pos_objetivo[1]))

        #Ahora comprobamos si taladro colisiona con la imagen objetivo para ganar el juego:
        x1 = pos_taladro[0]
        y1 = pos_taladro[1]
        x2 = pos_objetivo[0]
        y2 = pos_objetivo[1]
        if x1 < x2 + ancho_objetivo and x1 > x2 and y1 < y2 + ancho_objetivo and y1 > y2:
            print("Final juego ganas")
            self.End_Screen(True, self.pantalla)

    def Taladro_Sale_Mapa(self, posicion_taladro):
        #Si el taladro sale de las Dimensiones del juego cierra izquierda y derecha:
        if posicion_taladro[0] < 0 or posicion_taladro[0] > self.dimension_ventana[0]:
            self.End_Screen(False, self.pantalla)
        
        #O de la tierra por arriba y por abajo:
        if posicion_taladro[1] > self.dimension_ventana[1] or posicion_taladro[1] < 240:
            self.End_Screen(False, self.pantalla)
            
    def Colision_Taladro(self, pos_taladro, lista_obstaculos_pos):
        x1 = pos_taladro[0]
        y1 = pos_taladro[1]
        #Miramos la distancia entre cada obstaculo y taladro si es inferior a 10
        for obstaculo in range(len(lista_obstaculos_pos)):
            x2 = lista_obstaculos_pos[obstaculo][0]
            y2 = lista_obstaculos_pos[obstaculo][1]
            ancho = self.obstaculo_img.get_width()

            if x1 >= x2 and x2 + ancho >= x1:
                #Colision alto
                if y1 >= y2 and y2 + ancho >= y1:
                    self.End_Screen(False, self.pantalla) #Pierdes pantalla

    def Distancia_Entre_2_Puntos(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def Imprimir_Obstaculo(self, pos_taladro: list, lista_pos_obstaculos: list, lista_obstaculos_detectados: list):
        """
        Esta funcion detecta si el pos_taladro=>Esta a una distancia de menos de 70 de
        lista_pos_obstaculos "Que han sido generados anteriormente" si es asi lo 
        añadimos a => lista_obstaculos_detectados

        Tambien esta funcion imprime en pantalla toda la lista lista_obstaculos_detectados
        Parametros:

        pos_taladro => es una lista con la posicion del taladro ej [x, y]

        lista_pos_obstaculos => es una lista con todos los obstaculos generados aleatoriamente

        lista_obstaculos_detectados => es una lista que tiene todos los obstaculos detectados por taladro ej [xy, xy, ...]


        """
        x1, y1 = pos_taladro
        for i in range(len(lista_pos_obstaculos)):
            x2, y2 = lista_pos_obstaculos[i]

            #Comprobamos si los dos puntos tienen una distance de menos de 70:
            #Si es asi añadimos a nuestra lista de obstaculos visibles

            if self.Distancia_Entre_2_Puntos(x1, y1, x2, y2) < 70:
                #Añdimos el elemento que esta cerca del taladro a nuestra lista de objetos visibles
                #Para luego imprimirlo por pantalla
                self.obstaculos_visibles.append(lista_pos_obstaculos[i])
                
        
        #Ahora imprimimos todos los obstaculos que hemos detectado anteriormente
        for a in range(len(lista_obstaculos_detectados)):

            #Imprimimos cada obs de la lista:
            pygame.Surface.set_colorkey (self.obstaculo_img, (54,255,0))
            self.pantalla.blit(self.obstaculo_img, lista_obstaculos_detectados[a])


    def Crear_Obstaculos(self, pantalla, numero_obstaculos, lista_pos_obstaculos):
        for obstaculo in range(numero_obstaculos):
            pos_obstaculo = [random.randint(0, self.dimension_ventana[0]), random.randint(270, self.dimension_ventana[0])]
            #Añadimos nuestra posicion aleatoria de alto entre 270 y 500 y ancho de 0 a 500
            lista_pos_obstaculos.append(pos_obstaculo)

    def Animacion_HDD(self, pantalla):
            if (self.fotograma >= 1 and self.fotograma <= 5):
                
                archivo = ("hdd" + str(self.fotograma) + ".png")
                self.hdd_img = pygame.image.load(archivo)
                self.hdd_img.set_colorkey((54, 255, 0))
                pantalla.blit(self.hdd_img, self.hdd_pos)
                self.fotograma = self.fotograma+1

                #Reseteamos timer:
                self.timer_animacion = 0

            else:
                self.fotograma = 1
                #Añadimos tick a timer:
                self.timer_animacion = self.timer_animacion+1

    def Dibujar_Fondo(self, pantalla):
        #Primero dibujamos la tierra:
        pantalla.blit(self.tierra_img, (0, 250))
        #Luego el lago encima de la tierra
        pygame.draw.circle(pantalla, (0, 45, 243), ((self.dimension_ventana[0]/2), (self.dimension_ventana[1]/2-70)), 140)
        #Ahora el cielo:
        try:
            pygame.draw.rect(pantalla, self.color_cielo, (0, 0, self.dimension_ventana[0], self.dimension_ventana[1]/2))
        except:
            print("Error: parametro color_cielo no es valido al crear el objeto")

        #Dibujamos el hdd:
        self.Animacion_HDD(self.pantalla)


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
                pygame.draw.line(pantalla, (255, 255, 255), (x, y), (xfinal, yfinal), 2)
                

            iterador = iterador+1

    def Pintar_Camino_De_Tierra(self, lista_de_puntos, pantalla):
        
        for puntos in lista_de_puntos:
            x = puntos[0]
            y = puntos[1]

            #Solo pintamos si esta a una altura menor de la tierra:
            #Que es si la posicion del taladro si es mayor que la mitad de la altura de ventana + 5
            if y > ((self.dimension_ventana[0]/2)+5):
                pygame.draw.circle(pantalla, (121, 84, 66), (x, y), 10)
                
            

    def Bucle_Juego(self):
        while self.running == True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.running = False

                #Miramos si se presiona cualquier tecla si se presiona invertimos la rotacion:
                if evento.type == pygame.KEYUP:
                    self.direccion = self.direccion*-1

            #Primero miramos si posicion de taladro sale del mapa si es asi cierra el juego:
            self.Taladro_Sale_Mapa(self.postaladro)

            #Pintamos fondo:
            self.Dibujar_Fondo(self.pantalla)
            self.Animacion_HDD(self.pantalla)

            #Imprimimos obstaculos
            self.Imprimir_Obstaculo(self.postaladro, self.lista_pos_obstaculos, self.obstaculos_visibles)
            
            #Imprimimos el objetivo para ganar el juego:
            self.Imprimir_Objetivo(self.pantalla, self.objetivo, self.postaladro)
            #Comprobamos que taladro colisiona con obstaculo si es asi cierra:
            self.Colision_Taladro(self.postaladro, self.lista_pos_obstaculos)

            #Comprobamos que taladro entra al lago si es asi se acaba el juego:
            self.Taladro_Dentro_Lago(self.postaladro, ((self.dimension_ventana[0]/2), (self.dimension_ventana[1]/2-70)), 140)

            if self.angulo_taladro > 6.28:
                self.angulo_taladro = 0
            self.angulo_taladro = self.angulo_taladro+0.057*self.direccion

            nuevo_vector = [None, None]
            nuevo_vector[0] = (((self.taladro_vector[0]*math.cos(self.angulo_taladro)) - (self.taladro_vector[1]*math.sin(self.angulo_taladro))))
            nuevo_vector[1] = (((self.taladro_vector[0]*math.sin(self.angulo_taladro)) + (self.taladro_vector[1]*math.cos(self.angulo_taladro))))


            if self.angulo_prueba > 360:
                self.angulo_prueba = 0

            self.postaladro[0] = self.postaladro[0]  + nuevo_vector[0]
            self.postaladro[1] = self.postaladro[1] + nuevo_vector[1]

            #Añadimos nueva posicion de camino a nustra lista de puntos del camino :
            self.lista_puntos_camino.append([self.postaladro[0], self.postaladro[1]])


            #Primero pintamos la tierra removida por el camino
            self.Pintar_Camino_De_Tierra(self.lista_puntos_camino, self.pantalla)
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
            self.clock.tick(10)
            

        #Limpiando pygame
        pygame.quit()
        exit()
        



juego = Perforacion((500, 500), (155, 102, 72), (208, 253, 255), "Juego perforacion direccional")
juego.Inicio_Juego()
juego.Bucle_Juego()