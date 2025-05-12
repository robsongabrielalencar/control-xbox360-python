import pygame
from pynput.keyboard import Controller, Key
import sys

pygame.init()
pygame.joystick.init()

keyboard = Controller()

# Verifica controle
if pygame.joystick.get_count() == 0:
    print("Nenhum controle detectado.")
    sys.exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Controle detectado: {joystick.get_name()}")

# =====================================
# 🎮 BOTÕES DO CONTROLE → TECLAS
botao_para_tecla = {
    0: 't',              # A
    1: Key.esc,          # B
    2: Key.enter,        # X
    3: Key.ctrl_l,       # Y
    4: 'w',              # LB
    5: 'e',              # RB
    6: 's',              # BACK
    7: 'p',              # START
    8: 'h',              # Xbox (Guia)
    9: Key.shift,        # L Stick (click)
    10: Key.shift_r      # R Stick (click)
}

# 🎯 Gatilhos (LT = eixo 4, RT = eixo 5 em controles modernos)
# Se não funcionar, tente 2 e 5 dependendo do modelo do controle
eixo_LT = 4
eixo_RT = 5
gatilho_threshold = 0.5  # Valor entre 0 e 1
gatilho_estado = {'LT': False, 'RT': False}
gatilho_para_tecla = {
    'LT': 'q',
    'RT': 'r'
}

def apertar_tecla(tecla):
    try:
        keyboard.press(tecla)
        keyboard.release(tecla)
        print(f"→ Tecla enviada: {tecla}")
    except Exception as e:
        print(f"Erro ao enviar tecla {tecla}: {e}")

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.JOYBUTTONDOWN:
            botao = event.button
            if botao in botao_para_tecla:
                tecla = botao_para_tecla[botao]
                apertar_tecla(tecla)
            else:
                print(f"[Botão {botao}] sem mapeamento.")

    # LT
    valor_LT = joystick.get_axis(eixo_LT)
    if valor_LT > gatilho_threshold and not gatilho_estado['LT']:
        apertar_tecla(gatilho_para_tecla['LT'])
        gatilho_estado['LT'] = True
    elif valor_LT <= gatilho_threshold:
        gatilho_estado['LT'] = False

    # RT
    valor_RT = joystick.get_axis(eixo_RT)
    if valor_RT > gatilho_threshold and not gatilho_estado['RT']:
        apertar_tecla(gatilho_para_tecla['RT'])
        gatilho_estado['RT'] = True
    elif valor_RT <= gatilho_threshold:
        gatilho_estado['RT'] = False

    clock.tick(60)
