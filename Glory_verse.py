import pygame, random, time
from datetime import datetime as dt
from sys import exit

pygame.init()

obs_height = 10
obs_width = 10
left_limit, right_limit = 0, 800
ground_level = 283
vector_coords = []

screen = pygame.display.set_mode((right_limit - left_limit, 400))

class Player:
    def __init__(self):
        raw_image1 = pygame.image.load(r"player-0.png") #Standing Image
        self.image1 = pygame.transform.scale(raw_image1, (40, 50)).convert_alpha()

        raw_image2 = pygame.image.load(r"player-1.png") #Jumping Image
        self.image2 = pygame.transform.scale(raw_image2, (40, 50)).convert_alpha()

        raw_image3 = pygame.image.load(r"player--1.png") #Falling image
        self.image3 = pygame.transform.scale(raw_image3, (40, 50)).convert_alpha()

        self.main_image = self.image1 #Image drawn by screen
        self.rect = self.image1.get_rect(bottomleft = (left_limit, ground_level))
        self.dirn = 0
        self.main_attack = vectorAttack()
        self.step = 1
        self.vpreparing = False
        self.vmoving = False
        self.destination_coords = None
        self.last_x = self.rect.x
        self.last_y = self.rect.y

    @property
    def coords(self):
        coords = (self.rect.x, self.rect.y)
        return coords

    @property
    def image(self):
        return (self.main_image)

class Enemy:
    def __init__(self, image, x_decrement = 0, y_decrement = 0):
        self.hp = 100
        self.step = 2
        self.image = image
        self.rect = self.image.get_rect(bottomright = (right_limit - x_decrement, ground_level - y_decrement))
        self.init_x = self.rect.x
        self.movement = random.randrange(-1, 2, 2) #Gives 1 and -1 randomly
        self.collided = False
        self.last_x = self.rect.x
        self.last_y = self.rect.y
    
    @property
    def coords(self):
        return self.rect.x, self.rect.y

class vectorAttack:
    def __init__(self):
        self.strength = 10
        self.range = 100
        self.bonus1 = None
        self.bonus2 = None
        self.bonus3 = None
        raw_image = pygame.image.load(r"arrowhead.png")
        self.image = pygame.transform.scale(raw_image, (20, 20)).convert_alpha()

    def rect(self, coords):
        rect = self.image.get_rect(bottomleft = coords)
        return rect

    @property
    def eff_range(self):
        #Loads bonus 1/2/3 and in case of None, substitute them with a 0
        bonus1 = self.bonus1 or 0 
        bonus2 = self.bonus2 or 0
        bonus3 = self.bonus3 or 0

        length = self.range + bonus1 + bonus2 + bonus3
        return length

class Coords:
    def __init__(self, x, y = None):
        """CHECK IF X IS A TUPLE SIGNALLING COORDS TUPLE IS GIVEN DIRECTLY"""
        if isinstance(x, tuple):
            self.x = x[0]
            self.y = x[1]

        else:
            self.x = x
            self.y = y

    def add(self, coords):
        self.x += coords[0]
        self.y += coords[1]

    def subtract(self, coords):
        self.x -= coords[0]
        self.y -= coords[1]

    @property
    def coords(self):
        return self.x, self.y

class PlatformTiles():
    def __init__(self, topleft):
        raw_image = pygame.image.load(r"White_Background.jpg")
        self.image = pygame.transform.scale(raw_image, (10, 10)).convert()
        self.rect = self.image.get_rect(topleft=topleft)
    
p = Player()

vector_attack = 1
init_attack_coords = (0, 0)
final_coords = (0, 0)
attacking = False
vectors = []
grouped_vector_movement_coords = None

raw_enemy = pygame.image.load(r"enemy_red_100_by_100.png")
movement = -1 #-1 -> left, 1 -> right, 0 -> for neutral
step = 2

raw_bg = pygame.image.load(r"C:\Users\Lenovo\Documents\Video_Editing_Assets\Images\sci-fi-background.jpg")
bg = pygame.transform.scale(raw_bg, (800, 400)).convert_alpha()

projectiles = []
proj_speed = 10
    
all_hostile_rects = [] #Contains enemy obj except player's
for i in range(0):
    x_decrement = random.randrange(100, 600)
    #y_decrement = random.randrange(0, 200)
    y_decrement = random.randrange(0, 10)
    enemy_obj = Enemy(raw_enemy, x_decrement, y_decrement)
    all_hostile_rects.append(enemy_obj)

tiles = []
used = []
ground_levels = (260, 240, 220)
starts = (100, 200, 300)

for i in range(3):
    start = starts[i]
    for j in range(5):
        tile = PlatformTiles((start, ground_levels[i]))
        start += 10
        tiles.append(tile)
        used.append(start)

right_movement, left_movement = False, False

g = 4 #Denotes real world gravity
g_deacc = 0

clock = pygame.time.Clock()

init_time = None #Used to check spent time during jumps
jumping = None #Used for player jumps

def quit():
    pygame.quit()
    exit()

def move_toward(target_coords, moving_obj, step, **kwargs):
    print("RUNNING")
    moving_rect = moving_obj.rect

    last_x = moving_rect.x
    last_y = moving_rect.y

    x_diff = (target_coords[0] - moving_rect.x) or 1 #To prevent value 0
    x_dir = 1 #Right

    y_diff = target_coords[1] - moving_rect.y
    y_dir = 1

    if x_diff < 0:
        x_diff *= -1
        x_dir = -1

    if y_diff < 0:
        y_diff *= -1
        y_dir = -1

    slope = (y_diff / x_diff)

    x_step = max(((step ** 2) // (1 + (slope ** 2))) ** .5, 1) #Fron equation of slope, and pythagoras theorem, floor division to ensure only integer values; Max to ensure minimum 1 step
    y_step = slope * x_step

    #print("X_STEP: ", x_step, "Y_STEP: ", y_step, "SLOPE: ", slope, "X_DIFF: ", x_diff, "Y_DIFF: ", y_diff)
    moving_rect.x += x_dir * min(x_step, x_diff) #To ensure player doesn't overshoot target coords
    moving_rect.y += y_dir * min(y_step, y_diff) #dirn tells which way to move in the slope
    moving_obj.last_x = last_x
    moving_obj.last_y = last_y

    if kwargs:
            print("MOVE TOWARD VALUES:\nX STEP", x_step, "\nY STEP", y_step, "\nSLOPE", slope, "\nX_DIFF", x_diff, "\nY_DIFF", y_diff, "\nX_DIR", x_dir, "\nY_DIR", y_dir, "\nrect.x", moving_rect.x, "\nrect.y", moving_rect.y)

def distance(init_coords, final_coords):
    length = ((init_coords[0] - final_coords[0]) ** 2 + (init_coords[1] - final_coords[1]) ** 2) ** .5
    return length

def check_vector_movements(player: Player = p, vectors = vectors):
    """Check if any vector is eligible to cause player movement.
        Destination coords -> coordinates of the point where player is headed, if player is moving which it would be."""

    multiplier = 0
    resultant = Coords(0, 0)
    player_coords = player.coords
    updated_vectors = []

    for i, (init_coords, final_coords) in enumerate(vectors):
        length = distance(p.coords, final_coords)
        pcollision = player.rect.collidepoint(init_coords)

        if length <= p.main_attack.eff_range:
            if pcollision:
                x = final_coords[0] - init_coords[0]
                y = final_coords[1] - init_coords[1]
            
                resultant.add((x, y))
                multiplier += 1
        
            else:
                updated_vectors.append((init_coords, final_coords))

    destination_coords = p.destination_coords
    if destination_coords is not None:
        print("DEST COORDS NOT NONE")
        destination_coords = Coords(destination_coords)

        destination_coords.subtract(player_coords) #Gives x and y distance from player of destination coordinates
        resultant.add(destination_coords.coords)
        multiplier += 1

    resultant.add(player.coords) #To put movements centrered around player

    if resultant.coords[1] > ground_level:
        resultant.y = ground_level

    player.destination_coords =  resultant.coords #Stores coords after scalar product is applied to player coords
    player.step *= multiplier

    vectors.clear() #Clears vectors list while effecting the global one
    vectors.extend(updated_vectors) #Updates vectors list to remove ineligible vectors
            
def check_vector_attack(hostile_rects = all_hostile_rects, vctr_lst = vectors, player = p):
    """Checks if a vector attack is eligible before doing the attack."""

    print("RANGE: ", player.main_attack.eff_range)
    updated_hostile_rects = all_hostile_rects.copy() #To avoid modifying the list while iterating over it
    #print("VECTOR LIST INSIDE: ", vectors)

    for init_coords, final_coords in vctr_lst:
        length1 = distance(p.coords, init_coords)
        length2 = distance(p.coords, final_coords)

        if length1 <= player.main_attack.eff_range and length2 <= player.main_attack.eff_range:
            length3 = distance(init_coords, final_coords)
            
            for j, enemy in enumerate(hostile_rects):
                attack_collision = enemy.rect.collidepoint(final_coords)
                #print("ENEMY COORDS: ", enemy.coords, "FINAL COORDS: ", final_coords, "COLLISION: ", attack_collision)
                if attack_collision:
                    dmg = vector_attack * length3
                    enemy.hp -= dmg
                    print("DEALT: ", dmg, "\nREMAINING HP: ", enemy.hp)
                    if enemy.hp <= 0:
                        print("ENEMY KILLED!")
                        updated_hostile_rects.pop(j) #Removes enemy from hostile rects list
            
            hostile_rects.clear() #Clears hostile rects list while effecting the global one
            hostile_rects.extend(updated_hostile_rects) #Updates hostile rects list to remove dead enemies

    reward_player(len(hostile_rects), player)
    """NO VECTOR LIST UPDATE CODE HERE AS VECTOR LIST IS CLEARED AFTER THIS FUNCTION IS CALLED IN THE MAIN LOOP"""

def reward_player(enemy_num, player = p):
    if enemy_num < 10 and player.main_attack.bonus1 is None:
        player.main_attack.bonus1 = 50

    if enemy_num <= 7 and player.main_attack.bonus2 is None:
            player.main_attack.bonus2 = 100

    if enemy_num <= 4 and player.main_attack.bonus3 is None:
            player.main_attack.bonus3 = 200

def enemy_movement(enemy: Enemy, p: Player):

    dis = distance(enemy.coords, p.coords)
    if dis < 100:
        move_toward(p.rect, enemy, enemy.step,)# **{"a":1})
        if enemy.rect.colliderect(p.rect):
            quit()

        return

    enemy_ylevel = enemy.rect.bottomleft[1]

    if enemy.rect.bottomright[0] >= right_limit:
        enemy.rect.bottomright = (right_limit, enemy_ylevel)
        enemy.movement = -1

    elif enemy.rect.bottomleft[0] <= left_limit:
        enemy.rect.bottomleft = (left_limit, enemy_ylevel)
        enemy.movement = 1

    if enemy.collided:
        enemy.movement *= -1 #Reverses direction of enemy movement if it collided with a tile
        enemy.collided = False #Resets collided attribute to False

    if enemy.movement:
        last_x = enemy.rect.x
        new_x = last_x + (enemy.step * enemy.movement)
        if (new_x - enemy.init_x) < -200: 
            enemy.movement = 1

        elif (new_x - enemy.init_x) > 200:
            enemy.movement = -1

        enemy.last_x = last_x
        enemy.rect.x = new_x

def tiles_collision(tiles, objs):

    for i, obj in enumerate(objs):
        rect = obj.rect
        last_x = obj.last_x
        last_y = obj.last_y
        collided = False

        for tile in tiles:
            tile_rect = tile.rect
            collided = tile_rect.colliderect(rect)

            if not collided:
                continue

            print("COLLIDED WITH TILE: ", collided)

            left = rect.left - tile_rect.left
            top = rect.top - tile_rect.top

            def check_side(side1, side2, fallback_side2):
                """SIDE1 -> tile side, SIDE2/FALLBACK -> rect side"""
                diff = side1 - side2
                if diff == 0:
                    diff = check_side(side1, fallback_side2, None)
                return diff
                
            x_diff = check_side(tile.rect.left, rect.left, last_x)
            y_diff = check_side(tile.rect.top, rect.top, last_y)

            while tile_rect.colliderect(rect):
                rect.x += x_diff
                rect.y += y_diff

            if y_diff < 0:
                global jumping, init_time
                jumping = False
                init_time = dt.now()

            break #To stop check for other tiles once a collision is detected


        if i > 0 and collided: #Ensures that only enemies are affected by this code
            obj.collided = True

while True:
    """POSITIONING IN PYGAME: Later blits are placed on upper layers"""

    reward_player(len(all_hostile_rects), p)
    screen.blit(bg, (0, 0)) #Placed here so that every other draw happens after it.

    if right_movement:
        p.rect.x += 10

    elif left_movement:
        p.rect.x -= 10

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            coords = pygame.mouse.get_pos()
            length = distance(p.coords, coords)
            if length <= p.main_attack.eff_range:
                #print("INIT COORDS APPENDED", coords)
                vectors.append([coords, coords]) #Both coords are saved as initial coords

        if event.type == pygame.MOUSEBUTTONUP:
            fcoords = pygame.mouse.get_pos()
            length = distance(p.coords, fcoords)
            try:
                if length <= p.main_attack.eff_range:
                    #print("FINAL COORDS APPENDED", coords)
                    vectors[-1][1] = fcoords
                    #print("APPENDED TO:", vectors)

                else:
                    del vectors[-1]
            except:
                pass

            if not p.vpreparing: #Signifies vectors have been prepared.
                check_vector_movements()
                #print(len(all_hostile_rects), "HOSTILE RECTS BEFORE ATTACK CHECK")
                #print("VECTOR LIST BEFORE: ", vectors)
                check_vector_attack()
                
                vectors.clear()
                #print(len(all_hostile_rects), "HOSTILE RECTS AFTER ATTACK CHECK")

        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and p.rect.y == ground_level: #Handles jump
                    init_time = dt.now()
                    jumping = True

                if event.key == pygame.K_d: #Handles forward movement
                    right_movement = True
                    p.rect.x += 10
                    p.dir = 1
                    
                if event.key == pygame.K_a: #Handles backward movement
                    left_movement = True
                    p.rect.x -= 10
                    p.dirn = -1

                if event.key == pygame.K_k:
                    attack = pygame.image.load(r"attack_projectile.png").convert_alpha()
                    attack_coords = (p.rect.midleft[0], (p.rect.topright[1] + p.rect.midright[1])/2)

                    if p.dirn != 0:
                        if p.dirn == 1:
                            attack_x = p.rect.midright[0]
                            attack_y = (p.rect.topright[1] + p.rect.midright[1])/2
                            attack_rect = attack.get_rect(midleft = (attack_x, attack_y))

                        elif p.dirn == -1:
                            attack_x = p.rect.midleft[0]
                            attack_y = (p.rect.topleft[1] + p.rect.midleft[1])/2
                            attack_rect = attack.get_rect(midright = (attack_x, attack_y))

                        projectiles.append((attack, attack_rect, p.dirn))

                if event.key == pygame.K_q:
                    p.vpreparing = not p.vpreparing
                    print("PREPARING: ", p.vpreparing)

                    if not p.vpreparing:
                        check_vector_movements()
                        #print(len(all_hostile_rects), "HOSTILE RECTS BEFORE ATTACK CHECK")
                        check_vector_attack()
                        vectors.clear()
                        #print(len(all_hostile_rects), "HOSTILE RECTS AFTER ATTACK CHECK")
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    right_movement = False
                    
                if event.key == pygame.K_a:
                    left_movement = False

    if p.destination_coords is not None and p.coords != p.destination_coords:
        #print("DESTINATION IS", p.destination_coords, "WHILE CURRENTLY: ", p.coords)
        p.vmoving = True
        if p.destination_coords[1] - p.coords[1] < 0:
            p.main_image = p.image2 #Jumping image

        elif p.destination_coords[1] - p.coords[1] > 0:
            p.main_image = p.image3 #Falling image

        print("MOVING TOWARD DEST COORDS")
        move_toward(p.destination_coords, p, p.step, **{"1": 12})

    elif p.destination_coords == p.coords:
        #print("REACHED DESTINATION!")
        p.vmoving = False #Signifies player reached final coords
        p.destination_coords = None
        p.step = 1
        p.main_image = p.image1

    if jumping:
        g_deacc += g
        curr_time = dt.now()
        
        time_diff = (curr_time - init_time)
        time_spent = time_diff.seconds + time_diff.microseconds / 1000000 #Division to convert to a float second value like .001, .002, etc.
        
        if time_spent < .2:
            p.rect.y -= g * (time_spent + 1) ** 2

        else:
            p.rect.y += g * (time_spent + .7) ** 2 #.7 to compensate for .3 increase in time_spent before else block activates

    elif not p.vmoving:
        p.rect.y +=g

    #p.rect.x += 1

    if p.rect.y > ground_level: #Applied at last to ensure player y level isn't manipulated by anything after this.
        p.rect.y = ground_level

    if p.rect.y == ground_level:
        jumping = False #Not required as init changes every jump

    for enemy in all_hostile_rects:
        enemy_movement(enemy, p)
        screen.blit(enemy.image, enemy.rect)

    for j, (projectile, proj_rect, dirn) in enumerate(projectiles):
        """dirn -> Direction when throwing"""
        for i, h_obj in enumerate(all_hostile_rects):
            hrect = h_obj.rect

            if proj_rect.colliderect(hrect):
                del all_hostile_rects[i]
                del projectiles[j]
                break

        else:
            proj_rect.x += (dirn * proj_speed)

            if dirn == -1:
                projectile = pygame.transform.flip(projectile, 1, 0)
        
            screen.blit(projectile, proj_rect)

    white = (255, 255, 255)
    brown = (139, 69, 19)
    line_width = 10

    for vector in vectors:
        init_coords = vector[0]
    
        if vector[1] != init_coords: #Ensure final coord is saved
            final_coords = vector[1]

        else:
            final_coords = pygame.mouse.get_pos()

        length1 = distance(p.coords, init_coords)
        length2 = distance(p.coords, final_coords)

        attack_range = p.main_attack.eff_range

        if length1 <= attack_range and length2 <= attack_range:
            pygame.draw.line(screen, brown, init_coords, final_coords, line_width)
            rect = p.main_attack.rect(final_coords)
            screen.blit(p.main_attack.image, rect)

    tiles_collision(tiles, [p] +  all_hostile_rects)
    for tile in tiles:
        screen.blit(tile.image, tile.rect)

    screen.blit(p.image, p.rect)
    #Updates all draw on screen
    pygame.display.update()
    clock.tick(60)
