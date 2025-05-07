from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import time


# Camera-related variables
camera_pos = (0, 500, 500)

fovY = 120  # Field of view
GRID_LENGTH = 200  # Length of grid lines
rand_var = 423

# Floor animation variables
floor_offset = 0  
floor_speed = 1  
not_paused = True  
floor_color = (0.7, 0.5, 0.95)      
column_number = 4

# Obstacle variables
obstacles = []  
obstacle_types = ["wall", "box", "enemy", "gem", "ammo"]
obstacle_spawn_rate = 0.0015 
max_obstacles = 4  
obstacle_distance = -1000  

# Player and hostage variables
player_pos = [0,450,0]  
hostage_pos = [50,500,0]  
player_speed = 10  
hostage_delay = 0.15
last_move_time = 0 


last_time = time.time()
elapsed_time = 0.0

camera_mode = "third_person" 
fp_offset = [0, -25, 70]  
tp_distance = 90  
tp_height = 130  
tp_angle = 0 

# Bullet 
bullets = []
missed_bullets = 0
max_missed_bullets = 10

#gems
gem_pulse_speed = 0.005
min_size = 0.6
max_size = 1.2
size_fact = 1.0
is_expanding_gem = True

game_won= False
game_over = False
player_health = 100
player_score = 0


current_level = 1

gameState_start = 0
is_game_playing = 1
is_game_won = 2
game_state = gameState_start


button_width = 200
button_height = 80
start_button_pos = (500, 400)  # center x, y
exit_button_pos = (500, 300)   # center x, y


menu_button_width = 100
menu_button_height = 40
pause_button_pos = (300, 750)   # top-left corner
restart_button_pos = (450, 750) # top-left corner
exit_game_button_pos = (600, 750) # top-left corner


def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2] + 15)
    glScalef(2.0, 2.0, 2.0) 
    
    #  legs
    glPushMatrix()
    glColor3f(0, 0, 0.8)  # Blue pants
    glTranslatef(-5, 0, -5)  # Left 
    glScalef(0.4, 0.8, 0.4)
    glutSolidCube(20)
    glPopMatrix()
    
    glPushMatrix()
    glColor3f(0, 0, 0.8)  
    glTranslatef(5, 0, -5)  # Right
    glScalef(0.4, 0.8, 0.4)
    glutSolidCube(20)
    glPopMatrix()
    
    #  body 
    glPushMatrix()
    glColor3f(0.9, 0, 0) 
    glTranslatef(0, 0, 10)
    glScalef(1.0, 1.0, 1.0)
    glutSolidCube(20)
    glPopMatrix()
    
    # arms
    glPushMatrix()
    glColor3f(0.8, 0, 0)  
    glTranslatef(-13, 0, 10)  #right
    glScalef(0.3, 0.3, 0.8)
    glutSolidCube(20)
    glPopMatrix()
    
    glPushMatrix()
    glColor3f(0.8, 0, 0)  
    glTranslatef(13, -10, 15)  # left 
    glScalef(0.3, 0.8, 0.3)
    glutSolidCube(20)
    glPopMatrix()
    
    # head 
    glPushMatrix()
    glTranslatef(0, 0, 25)
    
    # Face
    glColor3f(1.0, 0.8, 0.62)  # Skin 
    glutSolidSphere(8, 20, 20)
    
    # Hair 
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)  # Black
    glTranslatef(0, 0, 5)
    glScalef(1.0, 1.0, 0.7)
    glutSolidSphere(8, 20, 20)
    glPopMatrix()
    
    glPopMatrix()
    
    #  gun 
    glPushMatrix()
    glTranslatef(13, -17, 17) 
    glRotatef(90, 0, 1, 0)  
    
    # Gun handle
    glColor3f(0.3, 0.2, 0.1)
    glPushMatrix()
    glScalef(1.0, 0.3, 0.3)
    glutSolidCube(10)
    glPopMatrix()
    
    # Gun body
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)  # Brown 
    glTranslatef(-4, -5, 0)
    glScalef(0.3, 0.9, 0.3)
    glutSolidCube(15)
    glPopMatrix()
    
    glPopMatrix()
    
    glPopMatrix()
# def gun():
def draw_hostage():
    glPushMatrix()
    glTranslatef(hostage_pos[0], hostage_pos[1], hostage_pos[2] + 15)
    glScalef(1.8, 1.8, 1.8) 
    #green pant
    glPushMatrix()
    glColor3f(0, 0.5, 0)  
    glTranslatef(-5, 0, -5)  # Left
    glScalef(0.4, 0.8, 0.4)
    glutSolidCube(20)
    glPopMatrix()
    
    glPushMatrix()
    glColor3f(0, 0.5, 0) 
    glTranslatef(5, 0, -5)  # Right
    glScalef(0.4, 0.8, 0.4)
    glutSolidCube(20)
    glPopMatrix()
    
    # body blue
    glPushMatrix()
    glColor3f(0.6, 0.8, 1.0)  
    glTranslatef(0, 0, 10)
    glScalef(1.0, 1.0, 1.0)
    glutSolidCube(20)
    glPopMatrix()
    
    #  arms
    glPushMatrix()
    glColor3f(0.6, 0.8, 1.0)  
    glTranslatef(-13, 0, 10)  # Left 
    glScalef(0.3, 0.3, 0.8)
    glutSolidCube(20)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(13, 0, 10)  # Right 
    glScalef(0.3, 0.3, 0.8)
    glutSolidCube(20)
    glPopMatrix()
    
    # head hostage
    glPushMatrix()
    glTranslatef(0, 0, 25)
    
    # Face
    glColor3f(1.0, 0.8, 0.6)  # Skin color
    glutSolidSphere(8, 20, 20)
    
 
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)  # Gray hair
    glTranslatef(0, 0, 5)
    glScalef(1.0, 1.0, 0.7)
    glutSolidSphere(8, 20, 20)
    glPopMatrix()
    
    glPopMatrix()
    
    glPopMatrix()
def draw_enemy(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z -15)  
    glScalef(1.6, -1.6, 1.6) 
    
    # Legs 
    glPushMatrix()
    glColor3f(0, 0.4, 0)  # Dark green
    glTranslatef(-5, 0, -5)  # Left 
    glScalef(0.4, 0.8, 0.4)
    glutSolidCube(20)
    glPopMatrix()
    
    glPushMatrix()
    glColor3f(0, 0.4, 0)  # Dark green
    glTranslatef(5, 0, -5)  # Right
    glScalef(0.4, 0.8, 0.4)
    glutSolidCube(20)
    glPopMatrix()
    
    # Body (Medium Green)
    glPushMatrix()
    glColor3f(0, 0.6, 0) 
    glTranslatef(0, 0, 10)
    glScalef(1.0, 1.0, 1.0)
    glutSolidCube(20)
    glPopMatrix()
    
    # Arms (Light Green)
    glPushMatrix()
    glColor3f(0.4, 0.8, 0.4)  
    glTranslatef(-13, 0, 10)  # Right arm
    glScalef(0.3, 0.3, 0.8)
    glutSolidCube(20)
    glPopMatrix()
    
    glPushMatrix()
    glColor3f(0.4, 0.8, 0.4)  
    glTranslatef(13, -10, 15)  # Left arm
    glScalef(0.3, 0.8, 0.3)
    glutSolidCube(20)
    glPopMatrix()
    
    # Head 
    glPushMatrix()
    glTranslatef(0, 0, 25)
    
    # Face
    glColor3f(0.6, 0.9, 0.6)  # Light green
    glutSolidSphere(8, 20, 20)
    
    # Helmet
    glPushMatrix()
    glColor3f(0, 0.3, 0)  # Dark green
    glTranslatef(0, 0, 5)
    glScalef(1.0, 1.0, 0.7)
    glutSolidSphere(8, 20, 20)
    glPopMatrix()
    
    glPopMatrix()
    
    
    glPushMatrix()
    glTranslatef(13, -10, 15) 
    glRotatef(90, 0, 1, 0)  
    
    # Axe handle
    glColor3f(0.3, 0.2, 0.1)
    glPushMatrix()
    glTranslatef(-5, -8, 0)
    glScalef(1.3, 0.5, 0.2)
    glutSolidCube(10)
    glPopMatrix()
    
    # Axe blade
    glPushMatrix()
    glColor3f(0.8, 0.8, 0.8)  # Light gray
    glTranslatef(-10, -17, 0)
    glScalef(0.6, 3, 0.1)
    glutSolidCube(10)
    glPopMatrix()
    
    glPopMatrix()
    
    glPopMatrix()


def draw_bullet(bullet):
    glPushMatrix()
    x, y, z = bullet["position"]
    glTranslatef(x, y, z)
    glColor3f(0.2, 0.0, 0.0)  
    glutSolidSphere(5, 10, 10) 
    glPopMatrix()

def draw_gem(x, y, z):
    global size_fact
    
    glPushMatrix()
    glTranslatef(x, y, z)
    

    glColor3f(0.0, 0.8, 0.3) 
    glScalef(size_fact, size_fact, size_fact)
    glutSolidSphere(GRID_LENGTH * 0.25, 16, 16)  
     
    glColor3f(0.5, 1.0, 0.7) 
    glTranslatef(-5, -5, 5)
    glutSolidSphere(GRID_LENGTH * 0.1, 8, 8)  
    glPopMatrix()

def draw_ammo(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(0.7, 0.7, 0.2)  
    glRotatef(-90, 1, 0, 1)      
    quad = gluNewQuadric()
    gluCylinder(quad, GRID_LENGTH * 0.12, GRID_LENGTH * 0.12, GRID_LENGTH * 0.25, 16, 4)  

    glColor3f(0.5, 0.5, 0.5) 
    glTranslatef(0, 0, GRID_LENGTH * 0.25)  
    glutSolidSphere(GRID_LENGTH * 0.12, 16, 16)  
    
    glPopMatrix()


def draw_wall_obstacle(x, y, z):

    glPushMatrix()
    glTranslatef(x, y, z)

    glColor3f(0.9, 0.3, 0.3)  
    glScalef(GRID_LENGTH * 0.8, GRID_LENGTH * 0.2, GRID_LENGTH * 0.8)  
    glutSolidCube(1.0)
    
    glPopMatrix()

def draw_box_obstacle(x, y, z):

    glPushMatrix()
    glTranslatef(x, y, z)
 
    glColor3f(0.8, 0.6, 0.4)  
    glScalef(GRID_LENGTH * 0.4, GRID_LENGTH * 0.4, GRID_LENGTH * 0.4) 
    glutSolidCube(1.0)  
    
    glPopMatrix()


def draw_obstacle(obstacle):
    x, y, z = obstacle["position"]
    obstacle_type = obstacle["type"]
    
    if obstacle_type == "wall":
        draw_wall_obstacle(x, y, z)
    elif obstacle_type == "box":
        draw_box_obstacle(x, y, z)
    elif obstacle_type == "enemy":  
        draw_enemy(x, y, z)
    elif obstacle_type == "gem":
        draw_gem(x, y, z)
    elif obstacle_type == "ammo":
        draw_ammo(x, y, z)

def create_obstacle():
    global obstacles, column_number    
   
    if len(obstacles)>=max_obstacles:
        return

    column = random.randint(-(column_number//2), (column_number//2)-1)  
    x_pos = column * GRID_LENGTH + GRID_LENGTH/2 
    z_pos = GRID_LENGTH/2 -60   
    y_pos = obstacle_distance

    obstacle_type = random.choice(obstacle_types)

    if obstacle_type == "wall":
        size = GRID_LENGTH * 0.8
    elif obstacle_type == "box":
        size = GRID_LENGTH * 0.6
    elif obstacle_type == "enemy":  
        size = GRID_LENGTH * 0.5  
    elif obstacle_type == "gem":
        size = GRID_LENGTH * 0.25
    elif obstacle_type == "ammo":
        size = GRID_LENGTH * 0.3
    
    obstacle = {"type": obstacle_type, "position": (x_pos, y_pos, z_pos), "size": size, "active": True}
    
    obstacles.append(obstacle)

last_obstacle_y = -9999  
min_spawn_distance = 100  
def update_obstacles():

    global obstacles, floor_speed, last_obstacle_y, player_pos

    for obstacle in obstacles[:]: #makes a copy of the list obstacle. If we iterate over the list itself, we cant remove elements from it. Dont remove it
        x, y, z = obstacle["position"]
        
        y += floor_speed #matching floor speed

        if obstacle["type"] == "enemy":
            px, py, pz = player_pos
            dx = px - x
            # dz = pz - z
            step_size = 0.4 #change this to make the enemy move faster or slower
            if current_level == 2:
                step_size = 0.6
            elif current_level == 3:
                step_size = 0.8
            if abs(dx) > 1:
                x += 0.1 if dx > 0 else -step_size
            y+= step_size 
            # if abs(dz) > 1:
            #     z += step_size if dz > 0 else -step_size

        obstacle["position"] = (x, y, z)
        
        if y > 600:
            obstacles.remove(obstacle)

    if not_paused and (not obstacles or abs(obstacles[-1]["position"][1] - last_obstacle_y) >= min_spawn_distance):
        if random.random() < obstacle_spawn_rate:
            create_obstacle()
            last_obstacle_y = obstacles[-1]["position"][1]  # update after spawning

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


# def draw_shapes():
#     glPushMatrix()  # Save the current matrix state
#     glColor3f(1, 0, 0)
#     glTranslatef(0, 0, 0)  
#     glutSolidCube(60) # Take cube size as the parameter
#     glTranslatef(0, 0, 100) 
#     glColor3f(0, 1, 0)
#     glutSolidCube(60) 

#     glColor3f(1, 1, 0)
#     gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
#     glTranslatef(100, 0, 100) 
#     glRotatef(90, 0, 1, 0)  # parameters are: angle, x, y, z
#     gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)

#     glColor3f(0, 1, 1)
#     glTranslatef(300, 0, 100) 
#     gluSphere(gluNewQuadric(), 80, 10, 10)  # parameters are: quadric, radius, slices, stacks

#     glPopMatrix()  # Restore the previous matrix state

def draw_tiles():
    global floor_offset, column_number, floor_color

    effective_offset=floor_offset%(GRID_LENGTH*2)
    
    for i in range(-10, 10): #rows
            base_offset=effective_offset+(i * GRID_LENGTH)
            
            for j in range(-column_number//2,column_number//2):  # Columns 
                column_offset=j*GRID_LENGTH
                
                glBegin(GL_QUADS)             
                if (i + j) % 2 == 0:
                    glColor3f(1, 1, 1) 
                else:
                    glColor3f(floor_color[0], floor_color[1], floor_color[2])  # Colored tiles
                
                # SIngle tile
             
                glVertex3f(column_offset,base_offset+GRID_LENGTH,0) # bottom left
                glVertex3f(column_offset+GRID_LENGTH,base_offset + GRID_LENGTH,0)   # top right
                glVertex3f(column_offset+GRID_LENGTH, base_offset,0)             
                glVertex3f(column_offset,base_offset,0)                
                glEnd()

def update_hostage(current_time):
    global player_pos, hostage_pos, hostage_delay, last_move_time
    smoothing_speed = 0.5
    if current_time - last_move_time >= hostage_delay:
        hostage_pos[0] += (player_pos[0] +50 - hostage_pos[0]) * smoothing_speed
        hostage_pos[1] += (player_pos[1] + 50 - hostage_pos[1]) * smoothing_speed
        hostage_pos[2] += (player_pos[2] - hostage_pos[2]) * smoothing_speed 


        last_move_time = current_time 
def update_bullets():
    global bullets, obstacles, missed_bullets, game_over, player_score, missed_bullets

    for bullet in bullets[:]:
        x, y, z = bullet["position"]
        # print(y)
        y -= bullet["speed"]  
        bullet["position"]=(x, y, z)
      
        hit = False
        for o in obstacles[:]:
            ox, oy, oz = o["position"]

            if o["type"] == "wall":
                size = GRID_LENGTH*1
            elif o["type"] == "box":
                size = GRID_LENGTH*0.4
            elif o["type"] == "enemy":
                size = GRID_LENGTH*0.5

            elif o["type"] == "ammo":
                size = GRID_LENGTH*0.3
            if o["type"]!="gem":
                if (abs(x-ox)<size/2 and abs(y-oy)<size/2 and abs(z-oz)<size/2):
                    if o["type"] == "enemy":                    
                        # print("Hit enemy!")
                        obstacles.remove(o)
                        player_score += 10
                        hit = True
                    elif o["type"] == "wall" and o["type"] == "box":
                        missed_bullets += 1 #so wall hit counts
                    elif o["type"] == "ammo":
                        # print("Hit ammo!")
                        missed_bullets-= 2
                        missed_bullets=max(0,missed_bullets) 
                        obstacles.remove(o)
                        hit = True
                    bullets.remove(bullet)                
                    break

        if not hit and (y < -1500) :  #bullet missed all obstacles
            bullets.remove(bullet)
            missed_bullets += 1
            if missed_bullets >= max_missed_bullets:
                game_over = True
def check_collision_player():
    global player_health, player_score, missed_bullets, game_over, current_level
    
    px, py, pz = player_pos
    player_size = 50  
    for obstacle in obstacles[:]:
        ox, oy, oz = obstacle["position"]     
        size = obstacle["size"]         
        if (abs(px - ox) < (player_size + size) / 2 and abs(py - oy) < (player_size + size) / 2 and abs(pz - oz) < (player_size + size) / 2):
        
            if obstacle["type"] == "wall":
                if current_level == 1:
                    player_health -= 10
                elif current_level == 2:
                    player_health -= 15
                else:  # level 3
                    player_health -= 20
                
            elif obstacle["type"] == "box":
                if current_level == 1:
                    player_health -= 5
                elif current_level == 2:
                    player_health -= 10
                else:  # level 3
                    player_health -= 15
                
            elif obstacle["type"] == "enemy":
                if current_level == 1:
                    player_health -= 20
                elif current_level == 2:
                    player_health -= 30
                else:  # level 3
                    player_health -= 40
                
            elif obstacle["type"] == "gem":
                if current_level == 1:
                    player_health = min(100, player_health+10) 
                elif current_level == 2:
                    player_health = min(100, player_health+15) 
                else:
                    player_health = min(100, player_health+20) 
                    
                player_score += 50
            elif obstacle["type"] == "ammo":
                if current_level == 1:
                    missed_bullets = max(0, missed_bullets-2)
                elif current_level == 2:
                    missed_bullets = max(0, missed_bullets-3)
                else:  # level 3
                    missed_bullets = max(0, missed_bullets-4)
        
            obstacles.remove(obstacle)
            if player_health <= 0:
                player_health = 0
                game_over = True

            break

def keyboardListener(key, x, y):
    global player_pos, last_move_time, player_speed
    global not_paused, floor_speed, floor_offset
    global camera_mode, tp_angle  , current_level

    if key == b'd': 
        new_pos = player_pos[0] - player_speed
        if current_level == 1 or current_level ==3:
            if new_pos >= -(column_number//2) * GRID_LENGTH:
                player_pos[0] = new_pos
        else:
            if new_pos >= (-(column_number//2) * GRID_LENGTH)-150:
                player_pos[0] = new_pos

    elif key == b'a': 
        new_pos = player_pos[0] + player_speed
    
        if new_pos <= (column_number//2) * GRID_LENGTH -70: #-70 so the hostage can be in the tiles

            player_pos[0] = new_pos

    # Toggle animation on/off (Space bar)
    # elif key == b' ':
    #     not_paused = not not_paused
        

    if key == b'+':
        floor_speed += 1.0
 
    if key == b'-':
        if floor_speed > 1.0:
            floor_speed -= 1.0
            
    if key == b'v':  # Toggle camera mode
        if camera_mode == "first_person":
            camera_mode = "third_person"
        else:
            camera_mode = "first_person"
        

    # # Move forward (W key)
    # if key == b'w':  

    # # Move backward (S key)
    # if key == b's':

    # # Rotate gun left (A key)
    # if key == b'a':

    # # Rotate gun right (D key)
    # if key == b'd':

    # # Toggle cheat mode (C key)
    # if key == b'c':

    # # Toggle cheat vision (V key)
    # if key == b'v':

    # # Reset the game if R key is pressed
    # if key == b'r':


def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for camera and movement.
    """
    global camera_pos, tp_distance, tp_height, tp_angle
    

    if key == GLUT_KEY_UP:
        tp_distance -= 10
        if tp_distance < 50:  
            tp_distance = 50
    
    if key == GLUT_KEY_DOWN:
        tp_distance += 10
        if tp_distance > 300:  
            tp_distance = 300
    

    if key == GLUT_KEY_PAGE_UP:
        tp_height += 10
    
    if key == GLUT_KEY_PAGE_DOWN:
        tp_height -= 10
        if tp_height < 20:  
            tp_height = 20

    if key == GLUT_KEY_LEFT: 
        tp_angle -= 15
    if key == GLUT_KEY_RIGHT:  
        tp_angle += 15

        
def mouseListener(button, state, x, y):
    global bullets, player_pos, game_state, not_paused, game_over, game_won
    y = 800 - y #800 = screen height
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if game_state == gameState_start or game_over or game_won:

            bx, by = start_button_pos
            if (bx - button_width/2 <= x <= bx + button_width/2 and
                by - button_height/2 <= y <= by + button_height/2):
                reset_game()
                game_state = is_game_playing
                game_over = False
                game_won = False
                return
            
            #exit button
            bx, by = exit_button_pos
            if (bx - button_width/2 <= x <= bx + button_width/2 and
                by - button_height/2 <= y <= by + button_height/2):
                glutLeaveMainLoop()
                return
        
        elif game_state == is_game_playing:
          
            # Pause button
            bx, by = pause_button_pos
            if (bx <= x <= bx + menu_button_width and
                by <= y <= by + menu_button_height):
                not_paused = not not_paused
                return
            
            # Restart button
            bx, by = restart_button_pos
            if (bx <= x <= bx + menu_button_width and
                by <= y <= by + menu_button_height):
                reset_game()
                return
            
            # Exit button
            bx, by = exit_game_button_pos
            if (bx <= x <= bx + menu_button_width and
                by <= y <= by + menu_button_height):
                glutLeaveMainLoop()
                return            
            # Fire
            if not_paused and not game_over and not game_won:
                bullet_x = player_pos[0] + 13
                bullet_y = player_pos[1] - 17
                bullet_z = player_pos[2] + 17
                
                new_bullet = {"position": (bullet_x, bullet_y, bullet_z), "speed": 15, "active": True}
                bullets.append(new_bullet)


def setupCamera():
    """
    Configures the camera's projection and view settings.
    Supports both first-person and third-person modes.
    """
    global camera_mode, player_pos, hostage_pos
    global fp_offset, tp_distance, tp_height, tp_angle
    
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    
    # Set up a perspective projection
    gluPerspective(fovY, float(1000) / float(800), 0.1, 1500)  # fov, aspect ratio, near clip, far clip
    
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix
    
    if camera_mode == "first_person":
        # First-person view logic
        # Position camera at player's head position with offset
        eye_x = player_pos[0]+fp_offset[0]
        eye_y = player_pos[1]+fp_offset[1]
        eye_z = player_pos[2]+fp_offset[2]
        
   
        target_x =player_pos[0] 
        target_y = player_pos[1]-100  
        target_z = player_pos[2]
        
        # Set the camera
        gluLookAt(eye_x, eye_y, eye_z,          # Camera position
                  target_x, target_y, target_z,  # Point camera is looking at
                  0, 0, 1)                       # Up vector (z-axis)
    
    else: 
    
        angle_rad = math.radians(tp_angle)
        

        cam_x = player_pos[0] + tp_distance * math.sin(angle_rad)
        cam_y = player_pos[1] + tp_distance * math.cos(angle_rad)
        cam_z = player_pos[2] + tp_height
        

        gluLookAt(cam_x, cam_y, cam_z,  
                  player_pos[0], player_pos[1], player_pos[2],
                  0, 0, 1) 
        

def update_values_for_differnt_levels():
    global column_number, floor_color, obstacle_spawn_rate, max_obstacles
    global player_health, missed_bullets, max_missed_bullets
    
    if current_level == 1:
        column_number = 2  
        floor_color = (0.7, 0.5, 0.95)  
        obstacle_spawn_rate = 0.0010
        max_obstacles = 2

    elif current_level == 2:
        column_number = 3  
        floor_color = (0.6, 0.4, 0.2)  
        obstacle_spawn_rate = 0.0020
        max_obstacles = 3

    elif current_level == 3:
        column_number = 4 
        floor_color = (0.95, 0.4, 0.5) 
        obstacle_spawn_rate = 0.0030
        max_obstacles = 4

def reset_game():

    global floor_offset, not_paused, player_pos, hostage_pos
    global bullets, missed_bullets, obstacles, player_health, player_score
    global current_level, game_over, game_won, last_time
    
    floor_offset = 0
    not_paused = True
    player_pos = [0, 450, 0]
    hostage_pos = [50, 500, 0]
    bullets = []
    obstacles = []
    missed_bullets = 0
    player_health = 100
    player_score = 0
    current_level = 1
    game_over = False
    game_won = False
    last_time = time.time()
    
    update_values_for_differnt_levels()


def draw_button(x, y, width, height, text):
    glColor3f(0.4, 0.4, 0.8) 
    glBegin(GL_QUADS)
    glVertex2f(x - width/2, y - height/2)
    glVertex2f(x + width/2, y - height/2)
    glVertex2f(x + width/2, y + height/2)
    glVertex2f(x - width/2, y + height/2)
    glEnd()
    
    # Draw text
    text_width = 0
    for ch in text:
        text_width += glutBitmapWidth(GLUT_BITMAP_HELVETICA_18, ord(ch))
    
    text_x = x - text_width/2
    text_y = y - 9  
    
    glColor3f(1.0, 1.0, 1.0)  
    glRasterPos2f(text_x, text_y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))


def draw_menu_button(x, y, width, height, text):

    # glColor3f(0.3, 0.3, 0.7)  # Button color
    # glBegin(GL_QUADS)
    # glVertex2f(x, y)
    # glVertex2f(x + width, y)
    # glVertex2f(x + width, y + height)
    # glVertex2f(x, y + height)
    # glEnd()
    
    text_width = 0
    for ch in text:
        text_width += glutBitmapWidth(GLUT_BITMAP_HELVETICA_18, ord(ch))
    
    text_x = x + (width - text_width)/2
    text_y = y + height/2 - 6
    
    glColor3f(1.0, 1.0, 1.0)  
    glRasterPos2f(text_x, text_y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
def draw_start_screen():
    global game_over, game_won, game_state, player_score

    glDisable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(0.2, 0.2, 0.4)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(1000, 0)
    glVertex2f(1000, 800)
    glVertex2f(0, 800)
    glEnd()  

    glDisable(GL_DEPTH_TEST)
    

    glColor3f(1.0, 1.0, 0.0)
    
    if game_won:
        title = "YOU WON!"
    elif game_over:
        title = "GAME OVER"
    else:
        title = "HOSTAGE RESCUE MISSION"
    
    title_width = 0
    for ch in title:
        title_width += glutBitmapWidth(GLUT_BITMAP_HELVETICA_18, ord(ch))
    
    glRasterPos2f(500 - title_width/2, 600)
    for ch in title:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

    if game_won:
        desc = f"You have successfully rescued the hostage! Final score: {player_score}"
    elif game_over:
        if player_health <= 0:
            desc = "You died! Try again to save the hostage!"
        else:
            desc = "Too many missed bullets! Try again to save the hostage!"
    else:
        desc = "Save the hostage by dodging obstacles and eliminating enemies!"
    
    desc_width = 0
    for ch in desc:
        desc_width += glutBitmapWidth(GLUT_BITMAP_HELVETICA_18, ord(ch))
    
    glColor3f(0.9, 0.9, 0.9)
    glRasterPos2f(500 - desc_width/2, 550)
    for ch in desc:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

    x, y = start_button_pos
    button_text = "PLAY AGAIN" if (game_over or game_won) else "PLAY"
    draw_button(x, y, button_width, button_height, button_text)
    
    x, y = exit_button_pos
    draw_button(x, y, button_width, button_height, "EXIT")

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_game_menu():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    #pause button
    x, y = pause_button_pos
    text = "RESUME" if not not_paused else "PAUSE"
    draw_menu_button(x, y, menu_button_width, menu_button_height, text)
        #restart button
    x, y = restart_button_pos
    draw_menu_button(x, y, menu_button_width, menu_button_height, "RESTART")    
    #exit button
    x, y = exit_game_button_pos
    draw_menu_button(x, y, menu_button_width, menu_button_height, "EXIT")

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
def idle():
    global floor_offset, last_time, elapsed_time
    global is_expanding_gem, size_fact, gem_pulse_speed
    global current_level, player_score, game_over, game_won, game_state

    current_time = time.time()
    delta_time=current_time-last_time
    last_time=current_time    
    if game_state == is_game_playing and not_paused and not game_over and not game_won:
        floor_offset += floor_speed
        
        elapsed_time+=delta_time

        if player_score >= 400:
            game_won = True
            game_state = is_game_won
            return
 
        elif player_score >= 250 and current_level < 3:
            current_level = 3
            update_values_for_differnt_levels()
        elif player_score >= 100 and current_level < 2:
            current_level = 2
            update_values_for_differnt_levels()
                
        update_obstacles()
        update_hostage(elapsed_time)
        update_bullets()
        
        if is_expanding_gem:
            size_fact += gem_pulse_speed
            if size_fact >= max_size:
                is_expanding_gem = False
        else:
            size_fact -= gem_pulse_speed
            if size_fact <= min_size:
                is_expanding_gem = True
                
        check_collision_player()
    
    glutPostRedisplay()
def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen based on game state
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    global game_state, game_over, game_won, player_health, player_score
    global camera_mode, hostage_pos, player_pos, floor_speed, current_level
    
    if game_state == gameState_start or game_over or game_won:
        
        draw_start_screen()
        
    elif game_state == is_game_playing:

        glEnable(GL_DEPTH_TEST)
        glLoadIdentity()
        glViewport(0, 0, 1000, 800)
        
        setupCamera()

        draw_tiles()
        
        for obstacle in obstacles:
            draw_obstacle(obstacle)
        
        draw_player()
        if camera_mode == "third_person":
            draw_hostage()
            
        for bullet in bullets:
            draw_bullet(bullet)
            

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 1000, 0, 800)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        draw_text(10, 710, f"Health: {player_health}")
        draw_text(890, 740, f"Score: {player_score}")
        draw_text(890, 710, f"Level: {current_level}")
        # draw_text(10, 740, f"Animation Speed: {floor_speed}")
        draw_text(10, 740, f"Missed Bullets: {missed_bullets}/{max_missed_bullets}")

        draw_game_menu()

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
    
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  
    glutInitWindowSize(1000, 800)  
    glutInitWindowPosition(0, 0) 

    wind = glutCreateWindow(b"Hostage Rescue Mission")  

    glutDisplayFunc(showScreen)  
    glutKeyboardFunc(keyboardListener)  
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle) 
    update_values_for_differnt_levels()
    glutMainLoop() 

if __name__ == "__main__":
    main()
