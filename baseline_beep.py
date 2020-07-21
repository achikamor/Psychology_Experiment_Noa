import numpy as np
import math
import tkinter as tk
from pynput.mouse import Controller
import clickINFO
import time
import random
import location
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
CENTER_X = 375
CENTER_Y = 355

sin = lambda degs: math.sin(math.radians(degs))
cos = lambda degs: math.cos(math.radians(degs))


class Celestial(object):
    # Constants
    COS_0, COS_180 = cos(0), cos(180)
    SIN_90, SIN_270 = sin(90), sin(270)

    def __init__(self, x, y, radius):
        self.x, self.y = x, y
        self.radius = radius

    def bounds(self):
        """ Return coords of rectangle surrounding circlular object. """
        return (self.x + self.radius*self.COS_0,   self.y + self.radius*self.SIN_270,
                self.x + self.radius*self.COS_180, self.y + self.radius*self.SIN_90)

    def get_position(self):
        x = self.x
        y = self.y
        return x, y


def circular_path(x, y, radius, delta_ang, start_ang=0):
    """ Endlessly generate coords of a circular path every delta angle degrees. """
    ang = start_ang % 360
    while True:
        yield x + radius*cos(ang), y + radius*sin(ang)
        ang = (ang+delta_ang) % 360


def update_position(canvas, id, celestial_obj, path_iter):
    celestial_obj.x, celestial_obj.y = next(path_iter)  # iterate path and set new position
    # update the position of the corresponding canvas obj
    x0, y0, x1, y1 = canvas.coords(id)  # coordinates of canvas oval object
    oldx, oldy = (x0+x1) // 2, (y0+y1) // 2  # current center point
    dx, dy = celestial_obj.x - oldx, celestial_obj.y - oldy  # amount of movement
    canvas.move(id, dx, dy)  # move canvas oval object that much
    # repeat after delay
    canvas.after(DELAY, update_position, canvas, id, celestial_obj, path_iter)


def clicker(i):
    mouse = Controller()
    x_loc, y_loc = mouse.position
    currT = time.time()
    curr_click = clickINFO.clickINFO(x_loc, y_loc, currT - start_t)
    clicks.append(curr_click)
    top.destroy()
    return


def play_sound(planet_obj1):
    winsound.Beep(2500, 100)
    x, y = planet_obj1.get_position()
    curr_location = location.location(x, y)
    locations.append(curr_location)
    return


def my_dest(top):
    circular = False
    top.destroy()


def main(client, iters, is_prac):
    result = []
    global clicks
    clicks = []
    global locations
    locations = []
    global circular
    circular = True
    global root
    global top
    global curr_client
    curr_client = client
    global start_t

    for i in range(iters):
        sound_time = random.randint(1200, 3200)
        end_time = random.randint(1000, 3000)
        top = tk.Tk()
        top.title('Baseline_Beep')
        canvas = tk.Canvas(top, bg='grey', height=HEIGHT, width=WIDTH)
        canvas.pack()
        clock = canvas.create_oval(CLOCK_X, CLOCK_Y, CLOCK_SIZE+CLOCK_X, CLOCK_SIZE+CLOCK_Y, width=4)
        if circular:
            sol_obj = Celestial(410, 370, 1)
            planet_obj1 = Celestial(640, 600, 10)  # the blue circle that moves
            planet1 = canvas.create_oval(planet_obj1.bounds(), fill='blue', width=0)
            orbital_radius = math.hypot(sol_obj.x - planet_obj1.x, sol_obj.y - planet_obj1.y)
            path_iter = circular_path(sol_obj.x, sol_obj.y, orbital_radius, CIRCULAR_PATH_INCR)
            next(path_iter)  # prime generator
            top.after(DELAY, update_position, canvas, planet1, planet_obj1, path_iter)
            top.after(sound_time, play_sound, planet_obj1)
            top.after(sound_time + end_time, my_dest, top)
            circular = False
        else:
            start_t = time.time()
            canvas_text = canvas.create_text(1100, 400, font="Times 28 bold", text="סמן את המקום שבו הייתה הנקודה \n  כאשר שמעת את הצפצוף", fill='blue')
            canvas.bind("<Button-1>", lambda x: clicker(x))
            circular = True
        top.mainloop()
    distances = calc_dist(locations, clicks)
    for i in range(len(distances)):
        final_curr_result = [clicks[i].timing, distances[i]]
        result.append(final_curr_result)
    if is_prac:
        client.blocks['baseline_beep_practice'] = result
    else:
        client.blocks['baseline_beep_task'] = result


def slider_click(x):
    mouse = Controller()
    x_loc, y_loc = mouse.position
    in_scale = ((x_loc-WIDTH*0.3)/400 * 10)
    curr_client.blocks['baseline_beep_slider'] = in_scale
    root.destroy()
    return


def angle_between(x1, x2, y1, y2):
    new_y2 = CLOCK_SIZE+CLOCK_Y-y2
    new_y1 = CLOCK_SIZE+CLOCK_Y-y1
    angle = math.atan2(new_y1 - new_y2, x1 - x2)
    angle = np.degrees(angle)
    if angle < 0:
        angle = 360+angle
    return angle


def check_validility(ball_angle, click_angle, is_right):
    if is_right:
        fst = (ball_angle + 90)
        snd = ball_angle-90
        if snd <= 0:
            snd = 360+snd
        if click_angle >= snd or click_angle <= fst:
            return True
    else:
        fst = ball_angle - 90
        if fst < 0:
            fst = 360+fst
        snd = (ball_angle + 90) % 360
        if (click_angle >= fst) and (click_angle <= snd):
            return True
        if (click_angle >= 0) and (click_angle <= snd):
            return True
    return False


def calc_dist(curr_locations, curr_clicks):
    dists = []
    for i in range(len(curr_clicks)):
        if curr_clicks[i] is not None and curr_locations[i] is not None:
            ball_x = int(curr_locations[i].x_loc)
            ball_y = int(curr_locations[i].y_loc)
            click_x = int(curr_clicks[i].x_loc)
            click_y = int(curr_clicks[i].y_loc)
            if ball_x > HALF_CLOCK + CLOCK_X:
                is_right = True
            else:
                is_right = False
            ball_angle = angle_between(ball_x, CENTER_X, ball_y, CENTER_Y)
            click_angle = angle_between(click_x, CENTER_X, click_y, CENTER_Y)
            is_valid_click = check_validility(ball_angle, click_angle, is_right)
            if is_valid_click:
                if (click_y >= CENTER_Y) and (ball_y >= CENTER_Y):
                    if click_x < ball_x:
                        sign = 1
                    else:
                        sign = -1
                elif (click_y <= CENTER_Y) and (ball_y <= CENTER_Y):
                    if click_x < ball_x:
                        sign = -1
                    else:
                        sign = 1
                else:
                    if is_right and (click_y < ball_y):
                        sign = -1
                    elif is_right and (click_y >= ball_y):
                        sign = 1
                    else:
                        if click_y > ball_y:
                            sign = -1
                        else:
                            sign = 1
                curr_destination = sign * (math.sqrt((math.pow((ball_x - click_x), 2)) + (math.pow((ball_y - click_y), 2))))
                dists.append(curr_destination)
            else:
                dists.append('error')
    return dists

