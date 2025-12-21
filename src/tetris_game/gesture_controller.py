import pygame
from gestures import read_gesture

class GestureController:
    def __init__(self, game):
        self.game = game
        self.last_gesture_time = 0
        self.last_pushdown_time = 0
        self.last_rotation_time = 0

        # Cooldown para realizar ciertas acciones
        self.GESTURE_COOLDOWN = 600
        self.PUSHDOWN_COOLDOWN = 1000
        self.ROTATION_COOLDOWN = 700

        # Estados de las manos actuales
        self.estado_mano_izq = "Nada"
        self.estado_mano_der = "Nada"
        self.distancia_ok = False 

        # Contadores de veces que se cierra y abre manos
        self.contador_cerrar_manos = 0
        self.contador_inclinar_manos = 0

        # Contador para saber cual es el ultimo gesto realizado
        self.ultimo_gesto_izq = "Nada"
        self.ultimo_gesto_der = "Nada"

    def update_hands_state(self, gesture):
        izq_estado = gesture["Left"]
        der_estado = gesture["Right"]

        if izq_estado == "Sin gesto":
            self.estado_mano_izq = "Nada"
        elif izq_estado == "palma_izquierda":
            self.estado_mano_izq = "Abierta"
        elif izq_estado == "cerrar_izquierda":
            self.estado_mano_izq = "Cerrada"
        else:
            self.estado_mano_izq = "Inclinada"

        if der_estado == "Sin gesto":
            self.estado_mano_der = "Nada"
        elif der_estado == "palma_derecha":
            self.estado_mano_der = "Abierta"
        elif der_estado == "cerrar_derecha":
            self.estado_mano_der = "Cerrada"
        else:
            self.estado_mano_der = "Inclinada"

    def update_last_gests(self):
        if self.estado_mano_izq != "Nada":
            self.ultimo_gesto_izq = self.estado_mano_izq
            
        if self.estado_mano_der != "Nada":
            self.ultimo_gesto_der = self.estado_mano_der

    def update_counters(self):
        if self.estado_mano_izq == "Cerrada" and not self.ultimo_gesto_izq == "Cerrada":
            self.contador_cerrar_manos += 1

        if self.estado_mano_der == "Cerrada" and not self.ultimo_gesto_der == "Cerrada":
            self.contador_cerrar_manos += 1

        if self.estado_mano_izq == "Inclinada" and not self.ultimo_gesto_izq == "Inclinada":
            self.contador_inclinar_manos += 1

        if self.estado_mano_der == "Inclinada" and not self.ultimo_gesto_der == "Inclinada":
            self.contador_inclinar_manos += 1

    def gesture_input(self, frame):
        if self.game.game_over:
            return

        now = pygame.time.get_ticks()
        if now - self.last_gesture_time < self.GESTURE_COOLDOWN:
            return

        self.last_gesture_time = now
        gesture = read_gesture(frame)     
        self.distancia_ok = gesture.get("distance_ok", False)

        self.update_hands_state(gesture)
        self.update_counters()
        self.update_last_gests()

        if "Sin gesto" in gesture.values():
            return

        if (now - self.last_pushdown_time > self.PUSHDOWN_COOLDOWN
            and gesture["Left"].startswith("cerrar")
            and gesture["Right"].startswith("cerrar")):
            self.game.push_down()
            self.last_pushdown_time = now
            return

        if gesture["Left"].startswith("cerrar"):
            self.game.move_left()
        if gesture["Right"].startswith("cerrar"):
            self.game.move_right()

        if now - self.last_rotation_time > self.ROTATION_COOLDOWN:
            if gesture["Left"].startswith("inclinar"):
                self.game.rotate_left()
            if gesture["Right"].startswith("inclinar"):
                self.game.rotate_right()
            self.last_rotation_time = now
