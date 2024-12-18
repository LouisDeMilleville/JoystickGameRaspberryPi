import serial
import pygame
import sys
import random
import time

# Initialisation de la communication srie
ser = serial.Serial('/dev/ttyACM0', 9600)

# Initialisation de Pygame
pygame.init()

# Configuration de l'affichage
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Joystick Square Game")

# Couleurs
beige = (245, 245, 220)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)

# Parametres du carre
square_size = 30
square_pos = [screen_width // 2 - square_size // 2, screen_height // 2 - square_size // 2]
speed_factor = 5  # Facteur de vitesse pour le mouvement

# Parametres des meteorites
meteorite_size = 30
meteorites = []
number_of_meteorites = 25  # Nombre de meteorites simultanees

# Temps de demarrage
start_time = time.time()
immobile_duration = 7  # Temps pendant lequel les meteorites restent immobiles

# Fonction pour creer une nouvelle meteorite
def create_meteorite():
    x_pos = random.randint(0, screen_width - meteorite_size)
    speed = random.uniform(2, 5)  # Vitesse aleatoire entre 2 et 5 pixels par frame
    return {'pos': [x_pos, 0], 'speed': speed}

# Initialiser les meteorites
for _ in range(number_of_meteorites):
    meteorites.append(create_meteorite())

# Initialisation du score
score = 0
last_score_update = time.time()

# Police pour afficher le score
font = pygame.font.SysFont(None, 36)

# Boucle principale
running = True
while running:
    # Verification des evenements Pygame pour quitter
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Lecture des donnees du port serie
    try:
        read_serial = ser.readline().decode('utf-8').strip()
        _, x_axis, y_axis = map(int, read_serial.split('|'))

        # Calcul du mouvement du carre
        move_x = (x_axis - 505) / 515.0
        move_y = (y_axis - 505) / 515.0

        # Mise a jour de la position du carre
        square_pos[0] += move_x * speed_factor
        square_pos[1] += move_y * speed_factor

        # S'assurer que le carre reste a l'interieur de la fenetre
        square_pos[0] = max(0, min(screen_width - square_size, square_pos[0]))
        square_pos[1] = max(0, min(screen_height - square_size, square_pos[1]))

    except ValueError as e:
        # Ignorez les lignes invalides
        print(f"Erreur lors de l'analyse des donnees : {e}")
        continue

    # Calcul du temps ecoule
    elapsed_time = time.time() - start_time

    # Deplacer les meteorites apres le temps immobile
    if elapsed_time > immobile_duration:
        for meteorite in meteorites:
            meteorite['pos'][1] += meteorite['speed']

        # Mise a jour du score toutes les secondes, seulement apres le delai initial
        if time.time() - last_score_update >= 1:
            score += 1
            last_score_update = time.time()

    # Supprimer et recreer les meteorites qui sortent de l'ecran
    for i, meteorite in enumerate(meteorites):
        if meteorite['pos'][1] >= screen_height:
            meteorites[i] = create_meteorite()

    # Detection des collisions
    for meteorite in meteorites:
        if (square_pos[0] < meteorite['pos'][0] + meteorite_size and
            square_pos[0] + square_size > meteorite['pos'][0] and
            square_pos[1] < meteorite['pos'][1] + meteorite_size and
            square_pos[1] + square_size > meteorite['pos'][1]):
            running = False  # Arreter la partie en cas de collision

    # Dessin du fond, du carre et des meteorites
    screen.fill(beige)
    pygame.draw.rect(screen, green, (*square_pos, square_size, square_size))
    for meteorite in meteorites:
        pygame.draw.rect(screen, red, (*meteorite['pos'], meteorite_size, meteorite_size))

    # Affichage du score
    score_text = font.render(f'Score: {score}', True, black)
    screen.blit(score_text, (10, 10))

    # Mise a jour de l'affichage
    pygame.display.flip()

# Afficher le score final dans le terminal
print(f"Score final: {score}")

# Quitter Pygame
pygame.quit()
sys.exit()
