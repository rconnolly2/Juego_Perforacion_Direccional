import pygame

class Perforacion:
    def __init__(self, dimension_ventana: tuple, color_tierra: tuple, color_cielo: tuple, titulo_ventana: str):
        self.dimension_ventana = dimension_ventana
        self.color_tierra = color_tierra
        self.color_cielo = color_cielo
        self.titulo_ventana = titulo_ventana
        self.pantalla = None
        self.running = True

    def Inicio_Juego(self):
        pygame.display.set_caption(self.titulo_ventana)

        try:
            self.pantalla = pygame.display.set_mode(self.dimension_ventana)
        except:
            print("Error: parametro dimension_vetnana no es valido al crear el objeto")

        try:
            #Primero dibujo la tierra
            self.pantalla.fill(self.color_tierra)
        except:
            print("Error: parametro color_cielo no es valido al crear el objeto")
        #Luego el lago que esta entre el suelo y el cielo
        pygame.draw.ellipse(self.pantalla, (0, 45, 243), (((self.dimension_ventana[0]/2)-(200/2)), (self.dimension_ventana[1]/2-70), 200, 150))
        #Luego el cielo
        pygame.draw.rect(self.pantalla, self.color_cielo, (0, 0, self.dimension_ventana[0], self.dimension_ventana[1]/2))

    def Bucle_Juego(self):
        while self.running == True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()

        #Limpiando pygame
        pygame.quit()



juego = Perforacion((500, 500), (155, 102, 72), (208, 253, 255), "Juego perforacion direccional")
juego.Inicio_Juego()
juego.Bucle_Juego()