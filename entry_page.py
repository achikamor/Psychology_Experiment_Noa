import baseline_beep
import beep
import slider
import client
import tkinter as tk
import os
import csv
import baseline_press
import speed
import codecs
import random

WIDTH = 1540
HEIGHT = 864


def solve_block(b_num, container):
    if b_num == 1:
        solve_BLB(container)
    elif b_num == 2:
        solve_B(container)
    elif b_num == 3:
        solve_BLP(container)
    elif b_num == 4:
        solve_P(container)
    else:
        solve_S(container)


def solve_BLB(container):   #cont[0] = new_client   ,  cont[1] = client_dir
    text1_loc = os.getcwd() + "\my_texts\_baseline_beep_practice.txt"
    with codecs.open(text1_loc, 'r', 'utf-8') as in1:
        text1_practice = in1.read()
    welcome_page(text1_practice)
    baseline_beep.main(container[0], 2, True)
    open_write(container[1], "\_baseline_beep_practice.csv", ["BaseLine", "-", "Beep", "-", "Practice"],
               {'distance', 'timing'},
               container[0], 'baseline_beep_practice')
    text1_task = os.getcwd() + "\my_texts\_baseline_beep_task.txt"
    with codecs.open(text1_task, 'r', 'utf-8') as in1:
        text2 = in1.read()
    welcome_page(text2)
    baseline_beep.main(container[0], 2, False)
    slider1_res = slider.main()
    open_write(container[1], "\_baseline_beep_task.csv", ["BaseLine", "-", "Beep", "-", "Task"],
               {'distance', 'timing'},
               container[0], 'baseline_beep_task')
    with open(container[1] + "\_baseline_beep_task.csv", 'a') as file:
        writer = csv.writer(file)
        writer.writerow(["SLIDER - RESULT"])
        writer.writerow([str(slider1_res)])


def solve_B(container):
    text2_loc = os.getcwd() + "\my_texts\_beep_practice.txt"
    with codecs.open(text2_loc, 'r', 'utf-8') as in1:
        text2_practice = in1.read()
    welcome_page(text2_practice)
    beep.main(container[0], 2, True)
    open_write(container[1], "\_beep_practice.csv", ["Beep", "-", "Practice"], {'distance', 'timing'},
               container[0], 'beep_practice')
    task_text = os.getcwd() + "\my_texts\_beep_task.txt"
    with codecs.open(task_text, 'r', 'utf-8') as in2:
        text_task = in2.read()
    welcome_page(text_task)
    beep.main(container[0], 2, False)
    slider2_res = slider.main()
    open_write(container[1], "\_beep_task.csv", ["Beep", "-", "Task"], {'distance', 'timing'},
               container[0], 'beep_task')
    with open(container[1] + "\_beep_task.csv", 'a') as file:
        writer = csv.writer(file)
        writer.writerow(["SLIDER - RESULT"])
        writer.writerow([str(slider2_res)])


def solve_BLP(container):
    text_loc = os.getcwd() + "\my_texts\_baseline_press_practice.txt"
    with codecs.open(text_loc, 'r', 'utf-8') as in1:
        text_practice = in1.read()
    welcome_page(text_practice)
    baseline_press.main(container[0], True, 2, True)
    open_write(container[1], "\_baseline_press_practice.csv", ["BaseLine", "-", "Press", "-", "Practice"],
               {'distance', 'timing'},
               container[0], 'baseline_press_practice')
    text1_loc = os.getcwd() + "\my_texts\_baseline_press_task.txt"
    with codecs.open(text1_loc, 'r', 'utf-8') as in1:
        text_task = in1.read()
    welcome_page(text_task)
    baseline_press.main(container[0], True, 2, False)
    open_write(container[1], "\_baseline_press_task.csv", ["BaseLine", "-", "Press", "-", "Task"],
               {'distance', 'timing'},
               container[0], 'baseline_press_task')


def solve_P(container):
    text_loc = os.getcwd() + "\my_texts\_press_practice.txt"
    with codecs.open(text_loc, 'r', 'utf-8') as in1:
        text_practice = in1.read()
    welcome_page(text_practice)
    baseline_press.main(container[0], False, 2, True)
    open_write(container[1], "\_press_practice.csv", ["Press", "-", "Practice"],
               {'distance', 'timing'},
               container[0], 'press_practice')
    text_loc = os.getcwd() + "\my_texts\_press_task.txt"
    with codecs.open(text_loc, 'r', 'utf-8') as in1:
        text_task = in1.read()
    welcome_page(text_task)
    baseline_press.main(container[0], False, 2, False)
    open_write(container[1], "\_press_task.csv", ["Press", "-", "Task"],
               {'distance', 'timing'},
               container[0], 'press_task')
    slider3_res = slider.main()
    with open(container[1] + "\_press_task.csv", 'a') as file:
        writer = csv.writer(file)
        writer.writerow(["SLIDER - RESULT"])
        writer.writerow([str(slider3_res)])


def solve_S(container):
    text_loc = os.getcwd() + "\my_texts\_speed_practice.txt"
    with codecs.open(text_loc, 'r', 'utf-8') as in1:
        text_practice = in1.read()
    welcome_page(text_practice)
    speed.main(container[0], 1, True)
    open_write(container[1], "\_speed_practice.csv", ["Speed", "-", "Practice"],
               {'timing'},
               container[0], 'speed_practice')
    text1_loc = os.getcwd() + "\my_texts\_speed_task.txt"
    with codecs.open(text1_loc, 'r', 'utf-8') as in1:
        text_task = in1.read()
    welcome_page(text_task)
    speed.main(container[0], 1, False)
    open_write(container[1], "\_speed_task.csv", ["Speed", "-", "Task"],
               {'timing'},
               container[0], 'speed_task')
    slider_res = slider.main()
    with open(container[1] + "\_speed_task.csv", 'a') as file:
        writer = csv.writer(file)
        writer.writerow(["SLIDER - RESULT"])
        writer.writerow([str(slider_res)])


def start_expiriment(root):
    root.destroy()
    return


def welcome_page(text):
    root = tk.Tk()
    root.title('welcome page')
    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()
    frame = tk.Frame(root, bg='grey')
    frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
    button = tk.Button(frame, text="    I'm ready   ", bg='red', fg='white', font=30, command=lambda: start_expiriment(root))
    button.pack(side='bottom', expand=True)
    label = tk.Label(frame, text=text, bg='grey', font=40)
    label.pack()
    root.mainloop()


def open_write(location, file_name, first_line, criters, curr_client, buffer):
    with open(location+file_name, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(first_line)
        writer.writerow(criters)
        for i in range(len(curr_client.blocks[buffer])):
            writer.writerow(curr_client.blocks[buffer][i])


def main():
    number = input("please enter participant's number:  ")
    new_client = client.Client(number)
    client_dir = os.getcwd()
    client_dir += "\data\_" + str(new_client.number)
    try:
        os.mkdir(client_dir)
    except:
        print("this client number is already in use, please choose a new number")
        main()
    container = [new_client, client_dir]
    blocks_array = [1, 2, 3, 4, 5]
    rand_order = []
    i = 4
    while len(blocks_array) > 0:
        r1 = random.randint(0, i)
        rand_order.append(blocks_array[r1])
        blocks_array.remove(blocks_array[r1])
        i = i - 1
    for j in range(len(rand_order)):
        solve_block(rand_order[j], container)
    for i in range(len(rand_order)):
        if rand_order[i] == 1:
          rand_order[i] = "baseline_beep"
        elif rand_order[i] == 2:
            rand_order[i] = "beep"
        elif rand_order[i] == 3:
            rand_order[i] = "baseline_press"
        elif rand_order[i] == 4:
            rand_order[i] = "press"
        elif rand_order[i] == 5:
            rand_order[i] = "speed"
    with open(container[1]+'\_block_order.csv', 'w') as file:
        file.write("Block-Order\n\n")
        for i in range(len(rand_order)):
            file.write(rand_order[i] + "\n")


if __name__ == "__main__":
    main()
