import pygame
import random
import sys

# 1. Initialize Pygame & Constants
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Glory Verse - 2D Edition")
font = pygame.font.Font(None, 28)
big_font = pygame.font.Font(None, 48)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
BLUE = (50, 150, 255)
RED = (255, 50, 50)
GREEN = (50, 200, 50)
YELLOW = (255, 255, 0)
PURPLE = (150, 50, 200)
GOLD = (255, 215, 0)

# Game States
STATE_MENU = 0
STATE_LEVEL1 = 1
STATE_LEVEL2 = 2
STATE_GAMEOVER = 3
STATE_WIN = 4

# 2. Object-Oriented Classes for Level 2
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 30, 30)
        self.color = BLUE
        self.speed = 10
        self.hp = 100
        self.inventory = []

    def move(self, keys):
        if keys[pygame.K_LEFT]: self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]: self.rect.x += self.speed
        if keys[pygame.K_UP]: self.rect.y -= self.speed
        if keys[pygame.K_DOWN]: self.rect.y += self.speed
        # Keep player on screen
        #self.rect.clamp_ip(screen.get_rect())

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Item:
    def __init__(self, name, x, y, color):
        self.name = name
        self.rect = pygame.Rect(x, y, 15, 15)
        self.color = color
        self.collected = False

    def draw(self, surface):
        if not self.collected:
            pygame.draw.rect(surface, self.color, self.rect)

class Enemy:
    def __init__(self, name, x, y):
        self.name = name
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = RED
        self.hp = 30
        self.defeated = False

    def draw(self, surface):
        if not self.defeated:
            pygame.draw.rect(surface, self.color, self.rect)

# 3. Game Setup Variables
current_state = STATE_MENU

# Level 1 Vars
secret_number = random.randint(0, 10) # Simplified range for 2D UI
user_guess = ""
guesses_left = 8
level1_msg = "Guess a number between 0 and 10! Type it and press ENTER."

# Level 2 Vars
player = Player(150, 450)
items = [
    Item("Crystal", 200, 500, PURPLE),
    Item("Rope", 100, 400, YELLOW),
    Item("Shield", 150, 150, GRAY)
]

troll = Enemy("Cave Troll", 450, 450)
blade_dropped = False
blade = Item("Blade", 450, 450, WHITE)

# Map Areas (Rooms as Rectangles)
rooms = {
    "Entrance": pygame.Rect(50, 350, 250, 200),
    "Chamber": pygame.Rect(350, 350, 250, 200),
    "River Bank": pygame.Rect(350, 50, 250, 200),
    "Altar Room": pygame.Rect(50, 50, 250, 200),
    "Treasure Room": pygame.Rect(650, 200, 100, 100) # Only accessible after puzzle
}

# 4. Helper Functions
def draw_text(surface, text, x, y, color=WHITE, font_type=font):
    text_obj = font_type.render(text, True, color)
    surface.blit(text_obj, (x, y))

def draw_map():
    # Draw Rooms
    pygame.draw.rect(screen, (30, 30, 30), rooms["Entrance"])
    pygame.draw.rect(screen, (50, 30, 30), rooms["Chamber"])
    pygame.draw.rect(screen, (30, 50, 50), rooms["River Bank"])
    pygame.draw.rect(screen, (40, 40, 60), rooms["Altar Room"])
    
    # Draw paths between rooms
    pygame.draw.rect(screen, GRAY, (300, 425, 50, 50)) # Entrance to Chamber
    pygame.draw.rect(screen, BLUE, (450, 250, 50, 100)) # River blocking Chamber to River Bank
    pygame.draw.rect(screen, GRAY, (300, 125, 50, 50)) # River Bank to Altar

    draw_text(screen, "Entrance", 60, 360)
    draw_text(screen, "Chamber", 360, 360)
    draw_text(screen, "River Bank (Needs Rope/Blade)", 360, 60)
    draw_text(screen, "Altar Room (Puzzle)", 60, 60)

# 5. Main Game Loop
clock = pygame.time.Clock()
running = True
log_msg = "Level 2: Use ARROWS to move. SPACE to attack/interact."
collided = False

while running:
    screen.fill(BLACK)
    events = pygame.event.get()
    
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            
        # STATE: MENU
        if current_state == STATE_MENU:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                current_state = STATE_LEVEL2

        # STATE: LEVEL 1 (Number Guessing)
        elif False: #current_state == STATE_LEVEL1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_guess.isdigit():
                        guess_int = int(user_guess)
                        if guess_int == secret_number:
                            current_state = STATE_LEVEL2
                        else:
                            guesses_left -= 1
                            if guesses_left <= 0:
                                current_state = STATE_GAMEOVER
                            elif guess_int > secret_number:
                                level1_msg = f"Too high! Guesses left: {guesses_left}"
                            else:
                                level1_msg = f"Too low! Guesses left: {guesses_left}"
                    user_guess = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_guess = user_guess[:-1]
                else:
                    user_guess += event.unicode

        # STATE: LEVEL 2 (Adventure)
        elif current_state == STATE_LEVEL2:
            if event.type == pygame.KEYDOWN:
                # Interaction / Combat Key
                if event.key == pygame.K_SPACE:
                    # Item Collection
                    for item in items:
                        if not item.collected and player.rect.colliderect(item.rect):
                            item.collected = True
                            player.inventory.append(item.name)
                            log_msg = f"You picked up the {item.name}!"
                    
                    if blade_dropped and not blade.collected and player.rect.colliderect(blade.rect):
                        blade.collected = True
                        player.inventory.append(blade.name)
                        log_msg = "You picked up the Blade!"

                    # Combat Troll
                    if not troll.defeated and collided:
                        print("PLAYER COLLIDED WITH TROLL")
                        troll.hp -= 10
                        if troll.hp <= 0:
                            troll.defeated = True
                            blade_dropped = True
                            log_msg = "You defeated the Cave Troll! A blade dropped."
                        else:
                            player.hp -= 15
                            log_msg = f"You hit Troll! Troll hits back! HP: {player.hp}"
                            if player.hp <= 0:
                                current_state = STATE_GAMEOVER
                        collided = False
                    
                    # Altar Puzzle
                    if player.rect.colliderect(rooms["Altar Room"]):
                        if "Crystal" in player.inventory and "Shield" in player.inventory and "Blade" in player.inventory:
                            current_state = STATE_WIN
                        else:
                            log_msg = "The altar requires a Crystal, Shield, and Blade."

    # --- UPDATES AND DRAWING BASED ON STATE ---

    if current_state == STATE_MENU:
        draw_text(screen, "THE GLORY VERSE - 2D", 200, 200, GOLD, big_font)
        draw_text(screen, "Press ENTER to start Level 1", 250, 300)

    elif current_state == STATE_LEVEL1:
        draw_text(screen, "LEVEL 1: NUMBER GUESSING", 200, 100, BLUE, big_font)
        draw_text(screen, level1_msg, 200, 200)
        draw_text(screen, f"Your guess: {user_guess}_", 200, 300, YELLOW)

    elif current_state == STATE_LEVEL2:
        # Movement
        keys = pygame.key.get_pressed()
        old_x, old_y = player.rect.x, player.rect.y
        player.move(keys)

        # Basic Environment Collisions (Troll Blockade & River Death)
        if not troll.defeated and player.rect.colliderect(troll.rect):
            collided = True
            player.rect.x, player.rect.y = old_x, old_y # Block movement
            
        river_rect = pygame.Rect(450, 250, 50, 100)
        if player.rect.colliderect(river_rect):
            if "Rope" in player.inventory or "Blade" in player.inventory:
                pass # Safe to cross
            else:
                log_msg = "The river swept you away! You need a rope or blade."
                player.hp -= 100
                current_state = STATE_GAMEOVER

        # Rendering Level 2
        draw_map()
        
        for item in items:
            item.draw(screen)
        
        if blade_dropped:
            blade.draw(screen)
            
        troll.draw(screen)
        player.draw(screen)

        # UI Overlay
        pygame.draw.rect(screen, BLACK, (0, 550, WIDTH, 50))
        draw_text(screen, f"HP: {player.hp} | Inv: {', '.join(player.inventory)}", 10, 560, GREEN)
        draw_text(screen, log_msg, 10, 10, YELLOW)

    elif current_state == STATE_GAMEOVER:
        draw_text(screen, "GAME OVER! YOU DIED.", 250, 250, RED, big_font)

    elif current_state == STATE_WIN:
        screen.fill(GOLD)
        draw_text(screen, "CONGRATULATIONS!", 250, 250, BLACK, big_font)
        draw_text(screen, "You have claimed the Glory's Crown!", 180, 300, BLACK)

    pygame.display.flip()
    clock.tick(30) # 30 Frames Per Second

pygame.quit()
sys.exit()
