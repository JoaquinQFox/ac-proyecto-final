import pygame, sys, cv2
from game import Game
from colors import Colors
from gestures import read_gesture

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 1000

pygame.init()

# title_font = pygame.font.Font(None, 40)
# score_surface = title_font.render("Score", True, Colors.white)
# next_surface = title_font.render("Next", True, Colors.white)
# game_over_surface = title_font.render("GAME OVER", True, Colors.white)

# score_rect = pygame.Rect(320, 55, 170, 60)
# next_rect = pygame.Rect(320, 215, 170, 180)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

cap = cv2.VideoCapture(0)
cv2.namedWindow("Captura de mano", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Captura de mano", 300, 300)        

game = Game()

# Tiempo en el que demora bajar un bloque automaticamente
GAME_UPDATE = pygame.USEREVENT + 1
pygame.time.set_timer(GAME_UPDATE, 2000)

# Tiempo en el que lee cada gesto
HANDS_UPDATE = pygame.USEREVENT + 2
pygame.time.set_timer(HANDS_UPDATE, 100)

# Cooldown para lectura de gesto
last_gesture_time = 0
GESTURE_COOLDOWN = 600

# Cooldown para hacer accion de pushdown (mover abajo defrente)
last_pushdown_time = 0
PUSHDOWN_COOLDONW = 1000


def gesture_input(gesture):
    if game.game_over == True:
        return

    now = pygame.time.get_ticks()
    if (now - last_gesture_time < GESTURE_COOLDOWN
        and gesture["Left"] == "Sin gesto" 
        and gesture["Right"] == "Sin gesto"):
        return
    
    if not gesture["Left"] == "Sin gesto":
        if gesture["Left"] == "cerrar_izquierda":
            game.move_left()
        elif gesture["Left"] == "inclinar_izquierda":
            game.rotate_left()

    if not gesture["Right"] == "Sin gesto":
        if gesture["Right"] == "cerrar_derecha":
            game.move_right()
        elif gesture["Right"] == "inclinar_derecha":
            game.rotate_right()

    if (now - last_pushdown_time > PUSHDOWN_COOLDONW
        and gesture["Left"] == "cerrar_izquierda" 
        and gesture["Right"] == "cerrar_derecha"):
        game.push_down()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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
                game.move_down()
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

                gesture = read_gesture(frame)
                gesture_input(gesture)

                    # if gesture == "palma_izquierda" and game.game_over == False:
                    #     game.move_left()
                    # elif gesture == "palma_derecha" and game.game_over == False:
                    #     game.move_right()

                    # elif ((gesture == "cerrar_izquierda" or gesture == "cerrar_derecha") 
                    #       and now - last_pushdown_time > PUSHDOWN_COOLDONW 
                    #       and game.game_over == False):
                    #     game.push_down()
                    #     last_pushdown_time = now


    # DRAWING
    # score_value_surface = title_font.render(str(game.score), True, Colors.white)

    screen.fill(Colors.dark_blue)

    # screen.blit(score_surface, (365, 20, 50, 50))
    # screen.blit(next_surface, (375, 180, 50, 50))

    # if game.game_over:
    #     screen.blit(game_over_surface, (320, 450, 50, 50))

    # Mostrar cuadro de puntaje
    # pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    # screen.blit(score_value_surface, score_value_surface.get_rect(centerx= score_rect.centerx,
                                                                #   centery= score_rect.centery))

    # pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    game.draw(screen)

    pygame.display.update()
    clock.tick(60)
