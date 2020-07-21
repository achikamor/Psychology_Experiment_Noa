class Client:
    def __init__(self, number):
        self.number = number
        self.mod = False
        self.blocks = dict({"baseline_beep_practice": [], "baseline_beep_task": [], "baseline_beep_slider": -1, "beep_practice": [], "beep_task": [],
                            "beep_slider": -1, "baseline_press_practice": [], "baseline_press_task": [], "press_practice": [],
                             "press_task": [], "press_slider": -1, "speed_practice": [], "speed_task": [], "speed_slider": -1, "block_order": []})

    def expender(self, blocks):
        self.mod = True
        self.blocks = blocks

    def printer(self):
        print("the number is:", self.number,
              "\n the mod is:", self.mod)
