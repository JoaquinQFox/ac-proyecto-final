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

game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)
HANDS_UPDATE = pygame.USEREVENT
pygame.time.set_timer(HANDS_UPDATE, 100)

last_gesture_time = 0
GESTURE_COOLDOWN = 800

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
            if event.key == pygame.K_w and game.game_over == False:
                game.rotate()

        # if event.type == GAME_UPDATE and game.game_over == False:
        #     game.move_down()

        if event.type == HANDS_UPDATE:
            ret, frame = cap.read()

            if ret:
                flipped = cv2.flip(frame, 1)
                cv2.imshow("Camara", flipped)
                cv2.waitKey(1)

                now = pygame.time.get_ticks()
                if now - last_gesture_time > GESTURE_COOLDOWN:
                    gesture = read_gesture(frame)

                    print(gesture)

                    if gesture == "palma_izquierda":
                        game.move_left()
                    elif gesture == "palma_derecha":
                        game.move_right()
                    elif gesture == "cerrar_izquierda" or gesture == "cerrar_derecha":
                        game.move_down()
                
                    last_gesture_time = now

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
