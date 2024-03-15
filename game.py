import pygame
import sys
import random
import csv 

# Initialisiere Pygame
pygame.init()

# Fenstergröße
width, height = 400, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Die Alkocops')

# Definition der Images:
image_spieler = pygame.image.load('images\\passi.png')

# Definition der Farben:
white = (255, 255, 255)
black = (0, 0, 0)
gold = (255, 215, 0)
brown = (102, 48, 2)
blue = (102, 178, 255)
grey = (200, 200, 210)

# Spieler-Eigenschaften:
player = pygame.Rect((width // 2 - 200, height - 125, 100, 100))
player_speed = 12

# Bier-Eigenschaften:
bier_width = 30
bier_height = 60
bier_speed = 3
beer_spawn = 0.010
biere = []

# Wasser-Eigenschaften:
wasser_width = 30
wasser_height = 60
wasser_speed = 5
wassers = []

# Soundeffekte:
rechnung_sfx = pygame.mixer.Sound("sounds\\Ober.wav")
collide_sfx = pygame.mixer.Sound("sounds\\schluck.wav")
glass_sfx = pygame.mixer.Sound("sounds\\glas.wav")
wasser_sfx = pygame.mixer.Sound("sounds\\super.wav")

# Hintergrundmusik:
uff_sfx_list = [pygame.mixer.Sound("sounds\\uff1.wav"), 
                pygame.mixer.Sound("sounds\\uff2.wav"), 
                pygame.mixer.Sound("sounds\\uff3.wav"), 
                pygame.mixer.Sound("sounds\\uff4.wav"), 
                pygame.mixer.Sound("sounds\\uff5.wav"), 
                pygame.mixer.Sound("sounds\\uff6.wav"), 
                pygame.mixer.Sound("sounds\\uff7.wav")]
background_music = pygame.mixer.Sound("music\\background2.mp3")
background_music.set_volume(0.15)
background_music.play(loops=-1)

# Score:
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

# Anfangsphase:
start_ticks = pygame.time.get_ticks()
start_screen_duration = 3000  # Zeit in Millisekunden
start_screen_shown = False

# Hauptprogrammschleife:
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not start_screen_shown:
            start_screen_shown = True
            start_ticks = pygame.time.get_ticks()

    # Anfangsphase
    current_time = pygame.time.get_ticks()
    if not start_screen_shown:
        start_screen_text1 = font1.render("Die Alkocops", True, white)
        start_screen_text2 = font1.render("Stimmt so", True, white)
        screen.blit(start_screen_text1, (width // 2 - start_screen_text1.get_width() // 2, height // 2 - 80))
        screen.blit(start_screen_text2, (width // 2 - start_screen_text2.get_width() // 2, height // 2))
        pygame.display.flip()

        # Überprüfe, ob die Startzeit abgelaufen ist
        if current_time - start_ticks >= start_screen_duration:
            start_screen_shown = True
            start_ticks = pygame.time.get_ticks()

    else:
        # Bewegung des Spielers
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < width:
            player.x += player_speed

        # Bewegung der Biere
        for bier in biere:
            bier.y += bier_speed
            if bier.colliderect(player):
                biere.remove(bier)
                score += 1
                collide_sfx.stop()
                collide_sfx.play()
        # Überprüfe, ob die Punktzahl ein Vielfaches von 5 ist
                if score % 5 == 0:
                    uff_sfx = random.choice(uff_sfx_list)
                    uff_sfx.play()
                    bier_speed += 0.5
                if score % 20 == 0:
                    beer_spawn += 0.005 

            # Entferne Biere, die den unteren Bildschirmrand erreicht haben
            if bier.y > height:
                biere.remove(bier)
                lives -= 1
                glass_sfx.stop()
                glass_sfx.play()

        # Bewegung von Wasser
        for wasser in wassers:
            wasser.y += wasser_speed
            if wasser.colliderect(player):
                wassers.remove(wasser)
                lives += 1
                wasser_sfx.stop()
                wasser_sfx.play()

        # Erzeuge neue Biere mit einer gewissen Wahrscheinlichkeit
        if random.random() < beer_spawn:
            bier_x = random.randint(0, width - bier_width)
            new_bier = pygame.Rect(bier_x, 0, bier_width, bier_height)
            biere.append(new_bier)

        # Erzeuge Wasser mit einer gewissen Wahrscheinlichkeit
        if score >= 30:
            if random.random() < 0.0015:
                wasser_x = random.randint(0, width - wasser_width)
                new_wasser = pygame.Rect(wasser_x, 0, wasser_width, wasser_height)
                wassers.append(new_wasser)

        # Game Over
        if lives == 0:
            add_score_to_highscore(name, score)
            background_music.stop()
            rechnung_sfx.play()

        game_over = False
        while lives == 0 and not game_over:

            player_speed = 0  # Stoppe die Spielerbewegung
            bier_speed = 0   # Stoppe die Bierbewegung
            
            # Zeige die Game Over-Meldung auf dem Bildschirm
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
                        # Restart the game logic here
                        lives = 3
                        score = 0
                        biere = []
                        player_speed = 12
                        bier_speed = 3
                        beer_spawn = 0.010
                        background_music.play()
                        game_over = False

        # Zeichne den Hintergrund:
        screen.fill(brown)
              
        # Zeichne den Spieler:
        screen.blit(image_spieler, player)

        # Zeichne die Biere:
        for bier in biere:
            pygame.draw.rect(screen, gold, bier)  # Körper
            pygame.draw.rect(screen, white, pygame.Rect(bier.left, bier.top, bier_width, bier_height // 4))  # Schaumkrone
            pygame.draw.rect(screen, grey, bier, width=2) # Glas

        # Zeichne das Wasser:
        for wasser in wassers:
            pygame.draw.rect(screen, blue, wasser) # Körper
            pygame.draw.rect(screen, grey, pygame.Rect(wasser.left, wasser.top, wasser_width, wasser_height // 4)) # Luft
            pygame.draw.rect(screen, grey, wasser, width=2) # Glas

        # Score und Leben:
        score_text = font2.render("Score: {}".format(score), True, white)
        screen.blit(score_text, (10, 10))

        lives_text = font2.render("Lives: {}".format(lives), True, white)
        screen.blit(lives_text, (width - 100, 10))

        # Aktualisiere den Bildschirm:
        pygame.display.flip()

        # Begrenze die Bildwiederholrate:
        clock.tick(60)

# Beende Pygame:
pygame.quit()
sys.exit()
