import pygame, sys, os, cv2
from game import Game
from colors import Colors
from gestures import read_gesture
from gesture_controller import GestureController

# Se desactiva escalado DPI en windows
if sys.platform == "win32":
    os.environ["SDL_VIDEO_HIGHDPI_DISABLED"] = "1"

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 880

pygame.init()

# Se definen fuentes
title_font = pygame.font.Font(None, 40)
text_font = pygame.font.Font(None, 35)

# Se definen textos
inf_title_surface = title_font.render("Información Manos", True, Colors.white)
hands_title_surface = title_font.render("Manos", True, Colors.white)
counter_title_surface = title_font.render("Acciones", True, Colors.white)

next_surface = title_font.render("Siguiente", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)
play_game_surface = title_font.render('Apreta "espacio" para jugar', True, Colors.white)

# Se definen rectangulos
inf_title_rect = pygame.Rect(50, 115, 340, 60)
inf_title_center_rect = inf_title_surface.get_rect(center=inf_title_rect.center)

hands_action_rect = pygame.Rect(82, 255, 280, 120)
hands_title_rect = hands_title_surface.get_rect(centerx=hands_action_rect.centerx, y=214)

counter_actions_rect = pygame.Rect(82, 482, 280, 120)
counter_title_rect = counter_title_surface.get_rect(centerx=counter_actions_rect.centerx, y=440)

next_rect = pygame.Rect(900, 175, 320, 280)
next_title_rect = next_surface.get_rect(centerx=next_rect.centerx, y=127)

# Se crea pantalla de juego
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Se inicializa tiempo
clock = pygame.time.Clock()

# Se inicializa camara
cap = cv2.VideoCapture(0)
cv2.namedWindow("Captura de mano", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Captura de mano", 300, 300)        

game = Game()
gesture_controller = GestureController(game)

# Tiempo en el que demora bajar un bloque automaticamente
GAME_UPDATE = pygame.USEREVENT + 1
pygame.time.set_timer(GAME_UPDATE, 2000)

# Tiempo en el que lee cada gesto
HANDS_UPDATE = pygame.USEREVENT + 2
pygame.time.set_timer(HANDS_UPDATE, 100)


# Función de dibujado
def draw():
    screen.fill(Colors.dark_blue)

    # Título de información de manos
    pygame.draw.rect(screen, Colors.light_blue, inf_title_rect, 0, 15)
    screen.blit(inf_title_surface, inf_title_center_rect)

    # Sección de visualización de acción de manos acutal
    pygame.draw.rect(screen, Colors.light_blue, hands_action_rect, 0, 15)

    screen.blit(hands_title_surface, hands_title_rect)

    left_hand_surface = text_font.render(f"IZQ: {gesture_controller.estado_mano_izq}", True, Colors.white)
    right_hand_surface = text_font.render(f"DER: {gesture_controller.estado_mano_der}", True, Colors.white)
    screen.blit(left_hand_surface, (108, 275))
    screen.blit(right_hand_surface, (108, 325))

    # Seccion de contador de acciones
    pygame.draw.rect(screen, Colors.light_blue, counter_actions_rect, 0, 15)

    screen.blit(counter_title_surface, counter_title_rect)

    close_counter_surface = text_font.render(f"Puños: {0}", True, Colors.white)
    incline_counter_surface = text_font.render(f"Inclinaciones: {0}", True, Colors.white)
    screen.blit(close_counter_surface, (108, 500))
    screen.blit(incline_counter_surface, (108, 550))

    # Sección de siguiente bloque

    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 15)
    screen.blit(next_surface, next_title_rect)

    if game.game_over:
        screen.blit(game_over_surface, (500, 500, 50, 50))


    # Mostrar cuadro de puntaje
    # pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)

    # pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    game.draw(screen)

    pygame.display.update()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()

            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN: 
            if game.game_over == True:
                if event.key == pygame.K_SPACE:
                    game.game_over = False
                    game.reset()

            if event.key == pygame.K_a and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_d and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_s and game.game_over == False:
                # game.move_down()
                game.push_down()
                game.update_score(0, 1)
            if event.key == pygame.K_q and game.game_over == False:
                game.rotate_left()
            if event.key == pygame.K_e and game.game_over == False:
                game.rotate_right()

        if event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()

        if event.type == HANDS_UPDATE:
            ret, frame = cap.read()

            if ret:
                flipped = cv2.flip(frame, 1)
                cv2.imshow("Captura de mano", flipped)
                cv2.waitKey(1)
                gesture_controller.gesture_input(frame)

    draw()

    clock.tick(60)
