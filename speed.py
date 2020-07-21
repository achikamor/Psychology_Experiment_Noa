import baseline_beep as bp
import random
import math
import tkinter as tk
import keyboard
import time
import entry_page
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


def play_sound(timings):
    winsound.Beep(2500, 100)
    timings[0] = time.time()
    return


def handle_error():
    print("in handle error")
    text='אנא לחצ/י על הכפתור רק לאחר השמע הצלצול'
    entry_page.welcome_page(text)
    return


def update_position2(canvas, id, planet_obj1, path_iter, timings, top, result, is_prac):
    try:
        if keyboard.is_pressed('s'):
            keyboard.release('s')
            pt = time.time()
            timings[1] = pt
            diff = pt - timings[0]
            top.destroy()
            if diff > 156460:
                if is_prac:
                    handle_error()
                diff = 'error'
            result.append(diff)
            return
    except:
        pass
    planet_obj1.x, planet_obj1.y = next(path_iter)  # iterate path and set new position
    # update the position of the corresponding canvas obj
    x0, y0, x1, y1 = canvas.coords(id)  # coordinates of canvas oval object
    oldx, oldy = (x0+x1) // 2, (y0+y1) // 2  # current center point
    dx, dy = planet_obj1.x - oldx, planet_obj1.y - oldy  # amount of movement
    canvas.move(id, dx, dy)  # move canvas oval object that much
    # repeat after delay
    canvas.after(DELAY, update_position2, canvas, id, planet_obj1, path_iter, timings, top, result, is_prac)


def main(client, iter, is_prac):
    result = []
    global top
    global timings
    timings = [0.0]*2
    for i in range(iter):
        sound_time = random.randint(1200, 3200)
        top = tk.Tk()
        top.title('Speed')
        canvas = tk.Canvas(top, bg='grey', height=HEIGHT, width=WIDTH)
        canvas.pack()
        clock = canvas.create_oval(CLOCK_X, CLOCK_Y, CLOCK_SIZE + CLOCK_X, CLOCK_SIZE + CLOCK_Y, width=4)
        sol_obj = bp.Celestial(410, 370, 1)
        planet_obj1 = bp.Celestial(640, 600, 10)  # the blue circle that moves
        planet1 = canvas.create_oval(planet_obj1.bounds(), fill='blue', width=0)
        orbital_radius = math.hypot(sol_obj.x - planet_obj1.x, sol_obj.y - planet_obj1.y)
        path_iter = bp.circular_path(sol_obj.x, sol_obj.y, orbital_radius, CIRCULAR_PATH_INCR)
        next(path_iter)  # prime generator
        top.after(sound_time, play_sound, timings)
        top.after(DELAY, update_position2, canvas, planet1, planet_obj1, path_iter, timings, top, result, is_prac)
        top.mainloop()
    for i in range(len(result)):
        result[i] = [result[i]]
    if is_prac:
        client.blocks['speed_practice'] = result
    else:
        client.blocks['speed_task'] = result



