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
    pass


def draw_bullet(bullet):
    pass
def draw_gem(x, y, z):
    pass

def draw_ammo(x, y, z):
    pass

def draw_wall_obstacle(x, y, z):

    pass

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
    pass
def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    pass
def draw_tiles():
    pass

def update_hostage(current_time):
    global player_pos, hostage_pos, hostage_delay, last_move_time
    smoothing_speed = 0.5
    if current_time - last_move_time >= hostage_delay:
        hostage_pos[0] += (player_pos[0] +50 - hostage_pos[0]) * smoothing_speed
        hostage_pos[1] += (player_pos[1] + 50 - hostage_pos[1]) * smoothing_speed
        hostage_pos[2] += (player_pos[2] - hostage_pos[2]) * smoothing_speed 


        last_move_time = current_time 
def update_bullets():
    pass
def check_collision_player():
    pass

def keyboardListener(key, x, y):
    pass
def specialKeyListener(key, x, y):
    pass
        
def mouseListener(button, state, x, y):
    pass

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
