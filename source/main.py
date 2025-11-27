import pygame
import sys
import random
import time


# --- Woorden inladen uit een textbestand ---
def load_words(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read().split()
    return content

woorden = load_words("./leesblaadjes/woorden kern_4a.txt")

random.shuffle(woorden)

pygame.init()

# --- Scherm ---
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Woorden oefenen - checks en sterren")

# --- Lettertypes ---
font_word = pygame.font.SysFont("Arial", 150)
font_info = pygame.font.SysFont("Arial", 40)

# --- Afbeeldingen laden ---
green_check = pygame.image.load("D:\Github\LerenLezen\source\icons\green_check.png")
red_check   = pygame.image.load("D:/Github/LerenLezen/source/icons/red_check.png")
star_img    = pygame.image.load("D:\Github\LerenLezen\source\icons\star.jpg")
happy_img   = pygame.image.load("D:\Github\LerenLezen\source\icons\happy.png")
sad_img     = pygame.image.load("D:\Github\LerenLezen\source\icons\sad.png")

# Alles naar uniforme grootte schalen
green_check = pygame.transform.scale(green_check, (50, 50))
red_check   = pygame.transform.scale(red_check,   (50, 50))
star_img    = pygame.transform.scale(star_img,    (70, 70))
sad_img     = pygame.transform.scale(sad_img,    (70, 70))

# --- Scores ---
good_checks_graphics = []   # lijst van groene check-afbeeldingen
bad_checks_graphics  = []   # lijst van rode check-afbeeldingen
stars_graphics       = []   # hoeveel sterren getoond zijn
sad_graphics        =  []   # sad faces

# --- Timing ---
last_time = time.time()
wpm = 0

# --- Initieel woord ---
current_word = woorden[0]

def new_word():
    random.shuffle(woorden)
    return woorden[0]

def draw_screen():
    screen.fill((255, 255, 255))

    # --- Woord in het midden ---
    word_surface = font_word.render(current_word, True, (0, 0, 0))
    rect = word_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(word_surface, rect)

    # --- Informatie ---
    info_text = f"WPM: {int(wpm)}"
    info_surface = font_info.render(info_text, True, (0, 0, 0))
    screen.blit(info_surface, (20, 20))

    # --- Groene checks tekenen ---
    x = 20
    y = HEIGHT - 80
    for chk in good_checks_graphics:
        screen.blit(green_check, (x, y))
        x += 60

    # --- Rode checks tekenen ---
    x = 20
    y = HEIGHT - 150
    for chk in bad_checks_graphics:
        screen.blit(red_check, (x, y))
        x += 60

    # --- Sterren tekenen ---
    x = WIDTH - (len(stars_graphics) * 80) - 20
    y = 20
    for st in stars_graphics:
        screen.blit(star_img, (x, y))
        x += 80
        
    # --- Sad faces tekenen ---
    x = WIDTH - (len(sad_graphics) * 80) - 20
    y = 100
    for st in sad_graphics:
        screen.blit(sad_img, (x, y))
        x += 80

    pygame.display.flip()


draw_screen()

# --- Hoofdloop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RIGHT, pygame.K_LEFT):

                # Tijd meten
                now = time.time()
                elapsed = now - last_time
                last_time = now

                # WPM
                if elapsed > 0:
                    wpm = 60 / elapsed

                # GOED
                if event.key == pygame.K_RIGHT:
                    good_checks_graphics.append(green_check)

                    # Elke 10 groene checks → 1 ster
                    if len(good_checks_graphics) == 10:
                        stars_graphics.append(star_img)
                        good_checks_graphics = []  # reset groene checks

                # FOUT
                if event.key == pygame.K_LEFT:
                    bad_checks_graphics.append(red_check)
                    
                    if len(bad_checks_graphics) == 10:
                        sad_graphics.append(sad_img)
                        bad_checks_graphics = []

                # Nieuw woord tonen
                current_word = new_word()
                draw_screen()
