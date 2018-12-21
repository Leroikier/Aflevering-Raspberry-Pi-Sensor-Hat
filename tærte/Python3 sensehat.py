from sense_hat import SenseHat
from time import sleep


sense = SenseHat()


white = (255, 255, 255)
sense.clear(white)
red = (255, 0, 0)
blue = (0, 0, 255)
bat_y = 4
bat_x = 0
ball_position = [3, 3]
ball_velocity = [1, 1]


#Functions --------------------------------
def draw_bat():
  sense.set_pixel(bat_x, bat_y, red)
  sense.set_pixel(bat_x, bat_y + 1, red)
  sense.set_pixel(bat_x, bat_y - 1, red)

def move_up(event):
    global bat_y
    
    if event.action == 'pressed' and bat_y > 1:
        bat_y -= 1

def move_down(event):
    global bat_y
    
    if event.action == 'pressed' and bat_y < 6:
        bat_y += 1

def draw_ball():
    sense.set_pixel(ball_position[0], ball_position[1], blue)
    ball_position[0] += ball_velocity[0]
    if ball_position[0] == 7 or ball_position[0] == 0:
        ball_velocity[0] = -ball_velocity[0]
        
    ball_position[1] += ball_velocity[1]
    if ball_position[1] == 7 or ball_position[1] == 0:
        ball_velocity[1] = -ball_velocity[1]
        
    if ball_position[0] == 1 and (bat_y - 1) <= ball_position[1] <= (bat_y + 1):
        ball_velocity[0] = -ball_velocity[0]
        
    if ball_position[0] == 0:
        sense.show_message("You Lose")
# Main program ------------------------------
sense.stick.direction_up = move_up
sense.stick.direction_down = move_down
while True:
    draw_bat()
    sleep(0.30)
    sense.clear(white)
    draw_ball()