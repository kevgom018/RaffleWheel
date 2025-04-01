import pygame
import random
import math
import time
import pygame.gfxdraw

DEBUG = False

# Screen settings
WIDTH, HEIGHT = 900, 600
screen = None

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Wheel settings
CENTER = (WIDTH // 3, HEIGHT // 2)
RADIUS = int(min(HEIGHT, WIDTH) / 3)

# List of participants
VISIBLE_ENTRIES = HEIGHT // 24
START_INDEX = 0

# Defined or modified later
ANGLE_STEP = 0
angle = 0
uniques = set()
colors = {}
participants = []
winner = ""
eraseWinnerScreen = False

# Names Extraction
def get_participants(filename):
    global uniques, participants, ANGLE_STEP

    file = open(filename, "r")
    lines = file.readlines()

    for line in lines:
        parts = line.strip().split()
        name = " ".join(parts[:-1])

        try:
            tickets = int(parts[-1])
        except ValueError:
            tickets = 1 # Invalid user inputs will recieve only 1 ticket

        participants.extend([name] * tickets)
        uniques.add(name)
        colors[name] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    file.close()

    uniques = list(uniques)
    participants.sort()
    ANGLE_STEP = 360 / len(participants)

# Pygame Wheel Setup
def draw_arrow():
    arrow_color = (255, 0, 0)  # Red arrow
    arrow_x = (WIDTH // 3) - RADIUS
    arrow_y = HEIGHT // 2  # Position above the wheel
    arrow_size = 20

    # Draw a downward-pointing triangle
    pygame.draw.polygon(screen, arrow_color, [
        (arrow_x - arrow_size, arrow_y - arrow_size),
        (arrow_x - arrow_size, arrow_y + arrow_size),
        (arrow_x, arrow_y)
    ])

def display_selected_name(name):
    font = pygame.font.Font(None, int(((WIDTH + HEIGHT) / 2) / 20.83333333))
    text = font.render(name, True, WHITE)
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT - 50 # Under Wheel
    screen.blit(text, (text_x, text_y))

def display_erase_option():
    font = pygame.font.Font(None, int(((WIDTH + HEIGHT) / 4) / 20.83333333))
    text = font.render('Remove choice once (Click Enter) Remove all instances (Click Backspace)', True, WHITE)
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT - 25 # Under selected name
    screen.blit(text, (text_x, text_y))
    pygame.display.update()


def draw_people(screen, choices, START_INDEX, visible_entries):
    title_font = pygame.font.Font(None, int(((WIDTH + HEIGHT) / 2) / 31.25))
    font = pygame.font.Font(None, int(((WIDTH + HEIGHT) / 2) / 37.5))
    x = int(WIDTH / 1.38461538)
    y_start = HEIGHT // 12  # Start drawing names from here
    
    title_surface = title_font.render("Participants", True, (255, 255, 255))
    screen.blit(title_surface, (x, y_start - 25))
    
    for i in range(START_INDEX, min(len(choices), START_INDEX + visible_entries)):
        y = y_start + (i - START_INDEX) * 20
        text = font.render(f"• {choices[i]}", True, (255, 255, 255))
        screen.blit(text, (x, y))

def draw_wheel():
    screen.fill((30, 30, 30))
    global winner, uniques, participants
    for i, name in enumerate(participants):
        start_angle = math.radians(i * ANGLE_STEP + angle)
        end_angle = math.radians((i + 1) * ANGLE_STEP + angle)

        x1, y1 = CENTER
        x2 = x1 + RADIUS * math.cos(start_angle)
        y2 = y1 + RADIUS * math.sin(start_angle)
        x3 = x1 + RADIUS * math.cos(end_angle)
        y3 = y1 + RADIUS * math.sin(end_angle)

        pygame.draw.polygon(screen, colors[name], [CENTER, (x2, y2), (x3, y3)])
        if DEBUG and i % 10 == 0:
            # Place text at the middle of the section
            font = pygame.font.Font(None, 24)
            winner_index = (int(-(angle % 360) // ANGLE_STEP) + 315) % len(participants)
            winner = participants[winner_index]
            if winner == name:
                color = (250, 0, 0)
            else:
                color = WHITE
            text_x = x1 + (RADIUS * 0.7) * math.cos(start_angle + (end_angle - start_angle) / 2)
            text_y = y1 + (RADIUS * 0.7) * math.sin(start_angle + (end_angle - start_angle) / 2)
            text = font.render(name.split()[0], True, color)
            screen.blit(text, (text_x - text.get_width() // 2, text_y - text.get_height() // 2))

    
    # Background Info
    font_title = pygame.font.Font(pygame.font.match_font("arial"), int(((WIDTH + HEIGHT) / 2) / 15))
    title_surface = font_title.render("AON Raffle Roulette", True, (0, 255, 0))
    title_rect = title_surface.get_rect(center=(int(WIDTH / 2.57142857), HEIGHT // 15))
    screen.blit(title_surface, title_rect)
    draw_arrow()
    if DEBUG:
        string = f"Congratulations {winner}! Angle: {int(angle)}, Winner Index: {winner_index}"
    else:
        string = f"Congratulations {winner}!"
    display_selected_name(string)
    draw_people(screen, uniques, START_INDEX, VISIBLE_ENTRIES)
    pygame.display.update()

# Spin and Pick Winner
def spin_wheel():
    global angle, winner, eraseWinnerScreen
    angle = 0
    speed = random.randint(70, 80)  # Initial speed
    deceleration = random.uniform(0.85, 0.95)
    eraseWinnerScreen = False 

    while speed > 0.1:
        angle += speed
        angle %= 360
        draw_wheel()
        # TODO: Check the calculation, after deleting a participant it stops working correctly
        winner_index = (int(-(angle % 360) // ANGLE_STEP) + 315) % len(participants)
        winner = participants[winner_index]
        speed *= deceleration
        time.sleep(0.05)
    
    draw_wheel()
    eraseWinnerScreen = True
    with open("winner.txt", "a") as f:
        f.write(f"Winner: {winner}\n")

def draw_screen():
    # TODO: Refactor all drawing calls to here
    pass

def main():
    pygame.init()
    global screen, START_INDEX, WIDTH, HEIGHT, CENTER, RADIUS, VISIBLE_ENTRIES, DEBUG, ANGLE_STEP, eraseWinnerScreen
    # Screen settings
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Spinning Wheel")
    get_participants("participants.txt")

    # Main loop
    running = True
    while running:
        draw_wheel()
        if eraseWinnerScreen:
            display_erase_option()
        for event in pygame.event.get():
            if eraseWinnerScreen and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    eraseWinnerScreen = False
                    participants.remove(winner)
                elif event.key == pygame.K_BACKSPACE:
                    eraseWinnerScreen = False
                    while True:
                        try:
                            participants.remove(winner)
                        except ValueError:
                            break
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                ANGLE_STEP = 360 / len(participants)
                spin_wheel()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                DEBUG = not DEBUG
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and START_INDEX > 0:
                        START_INDEX -= 1
                    elif event.key == pygame.K_DOWN and START_INDEX < len(uniques) - VISIBLE_ENTRIES:
                        START_INDEX += 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and START_INDEX > 0:  # Scroll up
                    START_INDEX -= 1
                elif event.button == 5 and START_INDEX < len(uniques) - VISIBLE_ENTRIES:  # Scroll down
                    START_INDEX += 1
            if event.type == pygame.WINDOWRESIZED:
                WIDTH = screen.get_width()
                HEIGHT = screen.get_height()
                CENTER = (WIDTH // 3, HEIGHT // 2)
                RADIUS = int(min(HEIGHT, WIDTH) / 3)
                VISIBLE_ENTRIES = HEIGHT // 24
    pygame.quit()


if __name__ == "__main__":
    main()

# TODO: Clean up code, comment throughly