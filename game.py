import pygame
import sys
import random
import csv

# Initialisierung Pygame:
pygame.init()

# Fenster:
width, height = 400, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Die Alkocops')

# Bild-Dateien:
image_spieler1 = pygame.image.load('images\\lausi.png')
image_spieler2 = pygame.image.load('images\\passi.png')
image_spieler3 = pygame.image.load('images\\nilsi.png')
image_spieler4 = pygame.image.load('images\\fabi.png')
image_spieler5 = pygame.image.load('images\\hermann.png')

# Spieler-Wahl:
selected_character = 0  # Default to the first character
character_images = [image_spieler1, image_spieler2, image_spieler3, image_spieler4, image_spieler5]

image_spieler = character_images[selected_character]

# Farben:
white = (255, 255, 255)
black = (0, 0, 0)
gold = (255, 215, 0)
brown = (102, 48, 2)
blue = (102, 178, 255)
grey = (200, 200, 210)

# Spieler:
player = pygame.Rect((width // 2 - 200, height - 125, 100, 100))
player_speed = 12

# Bier:
bier_width = 30
bier_height = 60
bier_speed = 3
beer_spawn = 0.010
biere = []

# Wasser:
wasser_width = 30
wasser_height = 60
wasser_speed = 5
wassers = []

# SFX:
rechnung_sfx = pygame.mixer.Sound("sounds\\Ober.wav")
collide_sfx = pygame.mixer.Sound("sounds\\schluck.wav")
glass_sfx = pygame.mixer.Sound("sounds\\glas.wav")
wasser_sfx = pygame.mixer.Sound("sounds\\super.wav")

# Musik:
uff_sfx_list = [pygame.mixer.Sound("sounds\\uff1.wav"),
                pygame.mixer.Sound("sounds\\uff2.wav"),
                pygame.mixer.Sound("sounds\\uff3.wav"),
                pygame.mixer.Sound("sounds\\uff4.wav"),
                pygame.mixer.Sound("sounds\\uff5.wav"),
                pygame.mixer.Sound("sounds\\uff6.wav"),
                pygame.mixer.Sound("sounds\\uff7.wav")]
background_music = pygame.mixer.Sound("music\\background1.mp3")
background_music.set_volume(0.15)
background_music.play(loops=-1)

# Score
score = 0
font2 = pygame.font.Font(None, 36)
name = 'lausi'

# High-Score extern speichern:
def add_score_to_highscore(name, score):
    highscore_path = 'highscore.csv'
    with open(highscore_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, score])

# Leben:
lives = 3

# Schriftgröße:
font_size1 = 64  # Start-Screen
font1 = pygame.font.Font(None, font_size1)
font_size2 = 32  # Score / Lives
font2 = pygame.font.Font(None, font_size2)

# Start:
start_ticks = pygame.time.get_ticks()
start_screen_duration = 3000
start_screen_shown = False

# Start // Spieler wählen:
character_selection = True
while character_selection:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                selected_character = (selected_character - 1) % len(character_images)
            elif event.key == pygame.K_RIGHT:
                selected_character = (selected_character + 1) % len(character_images)
            elif event.key == pygame.K_RETURN:
                character_selection = False

    # Schrift // Start Screen:
    screen.fill(brown)
    start_screen_text1 = font1.render("Die Alkocops", True, white)
    start_screen_text2 = font1.render("Stimmt so", True, white)
    screen.blit(start_screen_text1, (width // 2 - start_screen_text1.get_width() // 2, height - 520))
    screen.blit(start_screen_text2, (width // 2 - start_screen_text2.get_width() // 2, height - 440))
    character_text = font2.render("Choose Your Character", True, white)
    screen.blit(character_text, (width // 2 - character_text.get_width() // 2, height // 2 - 40))
    enter_text = font2.render("Press Enter", True, white)
    screen.blit(enter_text, (width // 2 - enter_text.get_width() // 2, height // 2 + 180))
    arrow_text = font2.render("<--      -->", True, white)
    screen.blit(arrow_text, (width // 2 - arrow_text.get_width() // 2, height // 2 + 140))

    # Images // Start Screen:
    screen.blit(character_images[selected_character], (width // 2 - 50, height // 2))

    pygame.display.flip()

# Spieler festlegen:
image_spieler = character_images[selected_character]

# Main Game Loop:
start_ticks = pygame.time.get_ticks()
start_screen_shown = False
start_screen_duration = 30

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not start_screen_shown:
            start_screen_shown = True
            character_selection = False
            start_ticks = pygame.time.get_ticks()

    current_time = pygame.time.get_ticks()
    if not start_screen_shown:
        pygame.display.flip()

        if current_time - start_ticks >= start_screen_duration:
            start_screen_shown = True
            start_ticks = pygame.time.get_ticks()

    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < width:
            player.x += player_speed

        for bier in biere:
            bier.y += bier_speed
            if bier.colliderect(player):
                biere.remove(bier)
                score += 1
                collide_sfx.stop()
                collide_sfx.play()
                if score % 5 == 0:
                    uff_sfx = random.choice(uff_sfx_list)
                    uff_sfx.play()
                    bier_speed += 0.5
                if score % 20 == 0:
                    beer_spawn += 0.005

            if bier.y > height:
                biere.remove(bier)
                lives -= 1
                glass_sfx.stop()
                glass_sfx.play()

        for wasser in wassers:
            wasser.y += wasser_speed
            if wasser.colliderect(player):
                wassers.remove(wasser)
                lives += 1
                wasser_sfx.stop()
                wasser_sfx.play()

        if random.random() < beer_spawn:
            bier_x = random.randint(0, width - bier_width)
            new_bier = pygame.Rect(bier_x, 0, bier_width, bier_height)
            biere.append(new_bier)

        if score >= 30:
            if random.random() < 0.0015:
                wasser_x = random.randint(0, width - wasser_width)
                new_wasser = pygame.Rect(wasser_x, 0, wasser_width, wasser_height)
                wassers.append(new_wasser)

        if lives == 0:
            add_score_to_highscore(name, score)
            pygame.mixer.pause()
            rechnung_sfx.play()
            game_over = False
            while lives == 0 and not game_over:
                player_speed = 0
                bier_speed = 0

                game_over_text1 = font1.render("Game Over!", True, white)
                game_over_text2 = font2.render("Final Score: {}".format(score), True, white)

                restart_text = font2.render("Restart Game", True, white)
                restart_rect = restart_text.get_rect(center=(width // 2, height // 2 + 50))

                screen.blit(game_over_text1, (width // 2 - game_over_text1.get_width() // 2, height // 2 - 40))
                screen.blit(game_over_text2, (width // 2 - game_over_text2.get_width() // 2, height // 2))
                screen.blit(restart_text, restart_rect)

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and lives == 0 and not game_over:
                        if restart_rect.collidepoint(event.pos):
                            lives = 3
                            score = 0
                            biere = []
                            player_speed = 12
                            bier_speed = 3
                            beer_spawn = 0.010
                            background_music.play(loops=-1)
                            game_over = False

        screen.fill(brown)
        screen.blit(image_spieler, player)

        for bier in biere:
            pygame.draw.rect(screen, gold, bier)
            pygame.draw.rect(screen, white, pygame.Rect(bier.left, bier.top, bier_width, bier_height // 4))
            pygame.draw.rect(screen, grey, bier, width=2)

        for wasser in wassers:
            pygame.draw.rect(screen, blue, wasser)
            pygame.draw.rect(screen, grey, pygame.Rect(wasser.left, wasser.top, wasser_width, wasser_height // 4))
            pygame.draw.rect(screen, grey, wasser, width=2)

        score_text = font2.render("Score: {}".format(score), True, white)
        screen.blit(score_text, (10, 10))

        lives_text = font2.render("Lives: {}".format(lives), True, white)
        screen.blit(lives_text, (width - 100, 10))

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
sys.exit()
