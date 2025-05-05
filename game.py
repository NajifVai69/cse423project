from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
#TODo make sure that multiple obstacles are not spawned in the same quadrent



# Camera-related variables
camera_pos = (0, 500, 500)

fovY = 100  # Field of view
GRID_LENGTH = 200  # Length of grid lines
rand_var = 423

# Floor animation variables
floor_offset = 0  
floor_speed = 1  
not_paused = True  
floor_color = (0.7, 0.5, 0.95)      
column_number = 2

# Obstacle variables
obstacles = []  
obstacle_types = ["wall", "box"]  
obstacle_spawn_rate = 0.0015 
max_obstacles = 4  
obstacle_distance = -1000  

# Player and hostage variables
player_pos = [0,450,0]  
hostage_pos = [0,500,0]  
player_speed = 10  
hostage_delay = 0.5
last_move_time = 0 
def draw_player():
    pass
# def gun():
def draw_hostage():
    pass

def draw_wall_obstacle(x, y, z):

    pass

def draw_box_obstacle(x, y, z):
    pass


def draw_obstacle(obstacle):
    pass

def create_obstacle():
    pass


def update_obstacles():

    pass

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    pass


def draw_shapes():
    pass

def draw_moving_floor():
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

def update_hostage_position(current_time):
    global player_pos, hostage_pos, hostage_delay, last_move_time

    if current_time - last_move_time >= hostage_delay:
        hostage_pos[0] = player_pos[0]  
        hostage_pos[2] = player_pos[2]  
        last_move_time = current_time 
                
def keyboardListener(key, x, y):
    global player_pos, last_move_time

    global not_paused, floor_speed, floor_offset
    if key == b'd':  # Move left
        player_pos[0] -= player_speed
    elif key == b'a':  # Move right
        player_pos[0] += player_speed

    
    # Toggle animation on/off (Space bar)
    # elif key == b' ':
    #     not_paused = not not_paused
        

    if key == b'+':
        floor_speed += 1.0
 
    if key == b'-':
        if floor_speed > 1.0:
            floor_speed -= 1.0
     
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
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos
    x, y, z = camera_pos
    # Move camera up (UP arrow key)
    # if key == GLUT_KEY_UP:

    # # Move camera down (DOWN arrow key)
    # if key == GLUT_KEY_DOWN:

    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        x -= 1  # Small angle decrement for smooth movement

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        x += 1  # Small angle increment for smooth movement

    camera_pos = (x, y, z)


def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
    # # Left mouse button fires a bullet
    # if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

    # # Right mouse button toggles camera tracking mode
    # if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
    pass


def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1, 0.1, 1500) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix


    x, y, z = camera_pos

    gluLookAt(x, y-1300, z,  # Camera position
              0, 0, 0,  # Look-at target
              0, 0, 1)  # Up vector (z-axis)


def idle():
    """
    Idle function that runs continuously:
    - Updates animations
    - Triggers screen redraw for real-time updates.
    """
    global floor_offset

    if not_paused:
        floor_offset += floor_speed


    current_time = glutGet(GLUT_ELAPSED_TIME) / 1000.0  
    update_obstacles()
    update_hostage_position(current_time)

    glutPostRedisplay()


def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  

    # # Draw a random points
    # glPointSize(20)
    # glBegin(GL_POINTS)
    # glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    # glEnd()

    # Draw the animated floor
    draw_moving_floor()


    for obstacle in obstacles:
        draw_obstacle(obstacle)
    draw_hostage()
    draw_player()
    

    draw_text(10, 710, f"Animation Speed: {floor_speed}")
    draw_text(10, 740, f"Level: One")

    # draw_shapes()   


    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  
    glutInitWindowSize(1000, 800)  
    glutInitWindowPosition(0, 0) 
    wind = glutCreateWindow(b"3D OpenGL Running Animation")  

    glutDisplayFunc(showScreen)  
    glutKeyboardFunc(keyboardListener)  
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle) 

    glutMainLoop() 

if __name__ == "__main__":
    main()