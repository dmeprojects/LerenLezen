import pygame
import sys
import random
import time

# --- Woordenlijst ---
woorden = [
    "dip","rijk","doop","hoek","boem",
    "koek","ijs","doos","hoes","poes",
    "dik","daar","hij","zoom","rij",
    "boen","soep","zee","hijs","den",
    "been","voer","raam","bij","oor",
    "haas","zit","boer","dijk","zoem",
    "hip","dit","moet","hees","zeer",
    "hoop","bijt","zes","poen","heet",
    "roep","zoek","rijp","door","hik",
    "doen","daan","rijm","zet","pit",
    "hoor","koen","peer","zoet","kijk",
    "voet","haar","zijn","deen","toet",
    "zeep","kaas","hek","beek","doek",
    "hit","beer","vaas","zoen","haas",
    "boek","mijn","haat","zaak","boot",
    "haan","pijn","hen","toen","boos"
]

random.shuffle(woorden)

pygame.init()

# --- Scherm ---
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Woorden oefenen - met score en WPM")

# --- Lettertypes ---
font_word = pygame.font.SysFont("Arial", 150)
font_info = pygame.font.SysFont("Arial", 40)

# --- Scores ---
good_count = 0
bad_count = 0
stars = 0

# --- Timing ---
last_time = time.time()
wpm = 0

# --- Index ---
index = 0

def new_word():
    """Selecteer een nieuw willekeurig woord"""
    random.shuffle(woorden)
    return woorden[0]

current_word = new_word()

def draw_screen():
    screen.fill((255, 255, 255))

    # --- Woord ---
    word_surface = font_word.render(current_word, True, (0, 0, 0))
    rect = word_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(word_surface, rect)

    # --- Score en statistieken ---
    info_text = f"Goed: {good_count}   Fout: {bad_count}   WPM: {int(wpm)}"
    info_surface = font_info.render(info_text, True, (0, 0, 0))
    screen.blit(info_surface, (20, 20))

    # --- Sterren ---
    star_text = "⭐" * stars
    if stars > 0:
        star_surface = font_info.render(star_text, True, (0, 0, 0))
        screen.blit(star_surface, (20, 70))

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

                # WPM berekenen (woorden per minuut)
                if elapsed > 0:
                    wpm = 60 / elapsed

                # Score updaten
                if event.key == pygame.K_RIGHT:  # juist
                    good_count += 1

                    # Elke 10 goede woorden → sterretje erbij
                    if good_count % 10 == 0:
                        stars += 1

                elif event.key == pygame.K_LEFT:  # fout
                    bad_count += 1

                # Nieuw woord
                current_word = new_word()
                draw_screen()
