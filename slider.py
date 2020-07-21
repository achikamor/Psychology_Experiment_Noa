import tkinter as tk
from pynput.mouse import Controller
import entry_page as ep
WIDTH = 1540
HEIGHT = 864


def clicker(x):
    mouse = Controller()
    x_loc, y_loc = mouse.position
    res.append(x_loc)
    top.destroy()
    return


def main():
    global top
    global res
    res = []
    text = "?באיזו מידה הרגשת שאת/ה זה/זו שהפיק/ה את הצלילים  \n  'מקמ/י (באמצעות העכבר) את תחושותיך על הרצף שבין 'כלל לא' ובין 'במידה רבה מאוד"
    ep.welcome_page(text)
    top = tk.Tk()
    top.title('Slider')
    canvas = tk.Canvas(top, bg='grey', height=HEIGHT, width=WIDTH)
    canvas.pack()
    slider = canvas.create_line(0.25*WIDTH, 0.55*HEIGHT, 0.75*WIDTH, 0.55*HEIGHT, width=3, activewidth=5)
    canvas.create_line(0.25*WIDTH, 0.6*HEIGHT, 0.25*WIDTH, 0.63*HEIGHT, width=5)
    label = tk.Label(top, text="כלל לא הרגשתי\n"
                                  "שהפקתי את הצלילים", bg='grey', font=25)
    label.place(rely=0.67, relx=0.21)
    canvas.create_line(0.75 * WIDTH, 0.6 * HEIGHT, 0.75 * WIDTH, 0.63 * HEIGHT, width=5)
    label = tk.Label(top, text="הרגשתי במידה רבה מאוד\n"
                               "שאני הפקתי את הצלילים", bg='grey', font=25)
    label.place(rely=0.66, relx=0.70)
    canvas.bind("<Button-1>", lambda x: clicker(x))
    top.mainloop()
    result = round((10 * (res[0] - 0.25*WIDTH) / (0.5*WIDTH)), 1)
    return result

