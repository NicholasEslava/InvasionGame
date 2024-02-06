import pygame
import sys
import random
import math
from pygame import mixer

# Inicializar pygame
pygame.init()

# Tamaño de la pantalla
screen = pygame.display.set_mode((800, 600))

# Titulo e icono
pygame.display.set_caption("Space Invasion")
icono = pygame.image.load("icono/ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("Fondo/fondo_space.jpg")

# Musica
mixer.music.load("Sonido/MusicaFondo.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)

# Nave
img_nave = pygame.image.load("nave/nave.png")
nave_x = 368
nave_y = 510
nave_movimiento_x = 0

# Naves enemigas
img_nave_enemiga = []
nave_enemiga_x = []
nave_enemiga_y = []
nave_enemiga_movimiento_x = []
nave_enemiga_movimiento_y = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_nave_enemiga.append(pygame.image.load("nave/nave_enemiga.png"))
    nave_enemiga_x.append(random.randint(0, 736))
    nave_enemiga_y.append(random.randint(50, 200))
    nave_enemiga_movimiento_x.append(0.3)
    nave_enemiga_movimiento_y.append(50)

# Balas
img_bala = pygame.image.load("nave/bala.png")
bala_x = 0
bala_y = 500
bala_movimiento_x = 0
bala_movimiento_y = 1
bala_visible = False

# Puntaje
puntaje = 0
fuente = pygame.font.Font("freesansbold.ttf", 32)
texto_x = 10
texto_y = 10

# Texto final de juego
fuente_final = pygame.font.Font("Letra/FreeSansBold.ttf", 40)


def texto_final():
    mi_fuente_final = fuente_final.render("GAME OVER", True, (255, 255, 255))
    screen.blit(mi_fuente_final, (270, 200))


# Función mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Score: {puntaje}", True, (255, 255, 255))
    screen.blit(texto, (x, y))


# Función nave enemiga
def nave_enemiga(x, y, ene):
    screen.blit(img_nave_enemiga[ene], (x, y))


# Función nave
def nave(x, y):
    screen.blit(img_nave, (x, y))


# Función disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    screen.blit(img_bala, (x + 16, y + 10))


# Función detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False


# Loop del juego
while True:

    # Fondo
    screen.blit(fondo, (0, 0))

    for evento in pygame.event.get():

        # Cerrar programa
        if evento.type == pygame.QUIT:
            sys.exit()

        # Presionar tecla
        if evento.type == pygame.KEYDOWN:

            # Presionar flecha izquierda
            if evento.key == pygame.K_LEFT:
                nave_movimiento_x = -0.3

            # Presionar flecha derecha
            if evento.key == pygame.K_RIGHT:
                nave_movimiento_x = 0.3

            if evento.key == pygame.K_SPACE:
                sonido_disparo = mixer.Sound("Sonido/disparo.mp3")
                if not bala_visible:
                    sonido_disparo.play()
                    bala_x = nave_x
                    disparar_bala(bala_x, bala_y)

        # Soltar tecla
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                nave_movimiento_x = 0

    # Movimiento de la nave
    nave_x += nave_movimiento_x

    # Limites de la nave
    if nave_x <= 0:
        nave_x = 0
    elif nave_x >= 736:
        nave_x = 736

    # Movimiento de la nave enemiga
    for e in range(cantidad_enemigos):

        # Fin del juego
        if nave_enemiga_y[e] > 480:
            for k in range(cantidad_enemigos):
                nave_enemiga_y[k] = 1000
            texto_final()
            break

        nave_enemiga_x[e] += nave_enemiga_movimiento_x[e]

        # Limites de la nave enemiga
        if nave_enemiga_x[e] <= 0:
            nave_enemiga_movimiento_x[e] = 0.3
            nave_enemiga_y[e] += nave_enemiga_movimiento_y[e]
        elif nave_enemiga_x[e] >= 736:
            nave_enemiga_movimiento_x[e] = -0.3
            nave_enemiga_y[e] += nave_enemiga_movimiento_y[e]

        # Colisión
        colision = hay_colision(nave_enemiga_x[e], nave_enemiga_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound("Sonido/Golpe.mp3")
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1
            nave_enemiga_x[e] = random.randint(0, 736)
            nave_enemiga_y[e] = random.randint(50, 200)

        nave_enemiga(nave_enemiga_x[e], nave_enemiga_y[e], e)

    # Movimiento Bala
    if bala_y <= -64:
        bala_y = 510
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_movimiento_y

    nave(nave_x, nave_y)

    mostrar_puntaje(texto_x, texto_y)

    # Actualizar programa
    pygame.display.update()