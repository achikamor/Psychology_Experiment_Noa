import baseline_beep as bp
import random
import math
import tkinter as tk
import keyboard
import time
import location
from pynput.mouse import Controller
import clickINFO
import winsound


DELAY = 50
CIRCULAR_PATH_INCR = 5
WIDTH = 1540
HEIGHT = 864
SPACE = 0xA
SOUND_TIME = 3000
END_OF_GAME = 8000
CLOCK_X = 70
CLOCK_Y = 30
CLOCK_SIZE = 680
HALF_CLOCK = 340


def clicker(i):
    mouse = Controller()
    x_loc, y_loc = mouse.position
    currT = time.time()
    curr_click = clickINFO.clickINFO(x_loc, y_loc, currT - start_t)
    beep_clicks.append(curr_click)
    top.destroy()
    return


def play_sound(planet_obj1):
    winsound.Beep(2500, 100)
    x, y = planet_obj1.get_position()
    curr_location = location.location(x, y)
    beep_locations.append(curr_location)
    return


def get_location(planet_obj1):
    x, y = planet_obj1.get_position()
    curr_location = location.location(x, y)
    beep_locations.append(curr_location)
    return


def update_position2(canvas, id, planet_obj1, path_iter, cont, is_baseline):
    pressed = False
    try:
        if keyboard.is_pressed('s') and cont:
            cont = False
            keyboard.release('s')
            pressed = True
    except:
        pressed = False
    if pressed:
        if not is_baseline:
            top.after(250, play_sound, planet_obj1)
        else:
            get_location(planet_obj1)
        kill_t = random.randint(1000, 3000)
    planet_obj1.x, planet_obj1.y = next(path_iter)  # iterate path and set new position
    # update the position of the corresponding canvas obj
    x0, y0, x1, y1 = canvas.coords(id)  # coordinates of canvas oval object
    oldx, oldy = (x0+x1) // 2, (y0+y1) // 2  # current center point
    dx, dy = planet_obj1.x - oldx, planet_obj1.y - oldy  # amount of movement
    canvas.move(id, dx, dy)  # move canvas oval object that much
    # repeat after delay
    canvas.after(DELAY, update_position2, canvas, id, planet_obj1, path_iter, cont, is_baseline)
    if pressed:
        canvas.after(kill_t, bp.my_dest, top)
        cont= True
        circular = False
        return


def main(client, is_baseline, iter, is_prac):
    global kill_t
    kill_t = 15000
    result = []
    global beep_clicks
    beep_clicks = []
    global beep_locations
    beep_locations = []
    global circular
    circular = True
    global top
    global start_t
    global cont
    cont = True
    for i in range(iter):
        kill_t = 15000
        end_time = random.randint(1000, 3000)
        top = tk.Tk()
        top.title('Baseline_Press')
        canvas = tk.Canvas(top, bg='grey', height=HEIGHT, width=WIDTH)
        canvas.pack()
        clock = canvas.create_oval(CLOCK_X, CLOCK_Y, CLOCK_SIZE + CLOCK_X, CLOCK_SIZE + CLOCK_Y, width=4)
        if circular:
            sol_obj = bp.Celestial(410, 370, 1)
            planet_obj1 = bp.Celestial(640, 600, 10)  # the blue circle that moves
            planet1 = canvas.create_oval(planet_obj1.bounds(), fill='blue', width=0)
            orbital_radius = math.hypot(sol_obj.x - planet_obj1.x, sol_obj.y - planet_obj1.y)
            path_iter = bp.circular_path(sol_obj.x, sol_obj.y, orbital_radius, CIRCULAR_PATH_INCR)
            next(path_iter)  # prime generator
            top.after(DELAY, update_position2, canvas, planet1, planet_obj1, path_iter, cont, is_baseline)
            circular = False
        else:
            start_t = time.time()
            canvas_text = canvas.create_text(1100, 400, font="Times 28 bold", text="סמן את המקום שבו הייתה \n הנקודה כאשר לחצת על המקש", fill='blue')
            canvas.bind("<Button-1>", lambda x: clicker(x))
            circular = True
        top.mainloop()
    distances = bp.calc_dist(beep_locations, beep_clicks)
    for i in range(len(distances)):
        final_curr_result = [beep_clicks[i].timing, distances[i]]
        result.append(final_curr_result)
    if is_baseline:
        if is_prac:
            client.blocks['baseline_press_practice'] = result
        else:
            client.blocks['baseline_press_task'] = result
    else:
        if is_prac:
            client.blocks['press_practice'] = result
        else:
            client.blocks['press_task'] = result


