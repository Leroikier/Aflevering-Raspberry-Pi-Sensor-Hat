from sense_hat import SenseHat
from time import sleep
from random import randint
sense = SenseHat()

sense.clear()       # sletter alt på skærmen
blue = (0, 0, 255)  # ny variabel som indeholder farven blå som RGB kode
red = (255, 0 ,0)   # ny variabel som indeholder farven rød som RGB kode
green = (0, 128, 0) # ny variabel som indeholder farven grøn som RGB kode
blank = (0, 0, 0)   # ny variabel som indeholder ikke indeholder en farve (blank)
direction = "right" # opretter en ny variabel ved navn, direction. med indholdet "right"

makeveg = []        # makeveg er vores liste der indeholder alle vegatable
super_veggie = []   # super_veggie er vores liste der indeholder alle super-vegatable
score = 0           # score variabel indeholder antal vegatables som der er samlet op
pause = 0.5         # pause varabel til at styre hvor lang tid der er imellem vores slug flytter sig en pixel
dead = False        # dead variabel til at tjekke som man er død eller ej.

slug_list = []      #slug_list er vores liste der indeholder alle ormens pixels
slug_1 = [3, 4]
slug_2 = [4, 4]     #lister med de pixels/kordinater vores orm indeholder
slug_3 = [5, 4]

slug_list.append(slug_1) #sætter en ny pixel ind i slug_list, så ormen vokser
slug_list.append(slug_2)
slug_list.append(slug_3)



# functions -----------------------------------------

def draw_slug(): #ny metode som indeholder slangens pixels
    for segment in slug_list: # for hver segment i listen gør dette:
        sense.set_pixel(segment[0], segment[1], red) # opretter en pixel på sense hatten
        
def move(): # metode til bevægelse af slange
    global score
    global pause # sørger for at vi kan ændre vores variabler inde i en metode.
    global dead
    remove = True # sætter boolean variablen remove til at være true
    
    # find den første og sidste pixel i vores slange
    last = slug_list[-1]
    first = slug_list[0]
    next = list(last) # lav en kopi af den sidste pixel
    
    # finder den næste pixel i den retning som vores slange bevæger sig i.
    if direction == "right":
        if last[0] + 1 == 8:
            next[0] = 0
        else:
            next[0] = last[0] + 1
    
    elif direction == "left":
        if last[0] - 1 == -1:
            next[0] = 7
        else:
            next[0] = last[0] - 1
    
    elif direction == "down":
        if last[1] + 1 == 8:
            next[1] = 0
        else:
            next[1] = last[1] + 1
    
    elif direction == "up":
        if last[1] - 1 == -1:
            next[1] = 7
        else:
            next[1] = last[1] - 1
    
    
    
    if next in slug_list:
        dead = True
    
    # tilføj denne pixel til enden af vores slange
    slug_list.append(next)
    
    #sæt den nye pixel til slangens farve
    sense.set_pixel(next[0], next[1], red)
    
    
    # sæt den første pixel til ikke at være blank
    sense.set_pixel(first[0], first[1], blank)

    # funktion til at at slangen kan spise nye vegatables
    if next in makeveg:
        makeveg.remove(next)
        score += 1
        if score % 5 == 0:
            remove = False
            pause = pause * 0.9
    
    # funktion til at slangen kan spise nye super-vegatables
    if next in super_veggie:
        super_veggie.remove(next)
        score += 5
        remove = False
        pause = pause * 0.9
    
    # tjekker at, når en veggie spises, slukkes lyset i dioden og den fjernes fra slug_list
    if remove == True:
        sense.set_pixel(first[0], first[1], blank)
        slug_list.remove(first)
        
    
#--------------------------------------------------------


def joystick_moved(event): # metode til styring af controller
    
global direction
direction = event.direction # direction variabel == den retning som controlleren trykkes til

# metode til at spawne nye veggies på banen, random steder 
def make_veg():
    while len(makeveg) >= 0 and len(makeveg) < 3:
        new = slug_list[0]  
        while new in slug_list:
            x = randint(0, 7)
            y = randint(0, 7)
            new = [x, y]
            sense.set_pixel(new[0], new[1], blue)
        makeveg.append(new)


# metode til at spawne en ny super-veggie på banen, random steder 
def superveggie():
    while len(super_veggie) >= 0 and len(super_veggie) < 1:
        new = slug_list[0]  
        while new in slug_list:
            x = randint(0, 7)
            y = randint(0, 7)
            new = [x, y]
            sense.set_pixel(new[0], new[1], green)
        super_veggie.append(new)
        
        
#main Program --------------------------------------
        
        
sense.stick.direction_any = joystick_moved # gør det muligt at bevæge controlleren i alle fire retninger
sense.clear()
draw_slug() # kalder draw_slug metoden til at tegne vores slange


# imens man ikke er død, kør disse metoder:
while dead == False:
    move()
    make_veg()
    if len(super_veggie) == 0 and randint(1, 10) > 8: #funktion til at styre spawn-rate på super-veggies
        superveggie()
    sleep(pause) # VENT!
    
sense.show_message("Game Over! " + " Score: " + str(score)) # viser du er død og din score
    