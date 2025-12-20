import pygame, sys, os, cv2
from game import Game
from colors import Colors
from gestures import read_gesture
from gesture_controller import GestureController

# Se desactiva escalado DPI en windows
if sys.platform == "win32":
    os.environ["SDL_VIDEO_HIGHDPI_DISABLED"] = "1"

SCREEN_WIDTH = 730
SCREEN_HEIGHT = 860

pygame.init()

# Se definen fuentes
title_font = pygame.font.Font(None, 40)
text_font = pygame.font.Font(None, 30)

score_surface = title_font.render("Manos", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

score_rect = pygame.Rect(480, 85, 200, 80)
next_rect = pygame.Rect(495, 245, 170, 180)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

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

    row_offset = 30
    # DRAWING
    left_hand_surface = text_font.render(f"IZQ: {gesture_controller.estado_mano_izq}", True, Colors.white)
    right_hand_surface = text_font.render(f"DER: {gesture_controller.estado_mano_der}", True, Colors.white)

    screen.fill(Colors.dark_blue)

    screen.blit(score_surface, (545, 50, 50, 50))
    screen.blit(next_surface, (550, 200, 50, 50))

    if game.game_over:
        screen.blit(game_over_surface, (500, 500, 50, 50))

    # Mostrar cuadro de puntaje
    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    screen.blit(left_hand_surface, (500, 100))
    screen.blit(right_hand_surface, (500, 140))

    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    game.draw(screen)

    pygame.display.update()
    clock.tick(60)
