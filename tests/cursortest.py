import tkinter as tk
class CursorTest(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Curosor demo")
        self.group1 = tk.LabelFrame(self, padx=15, pady=10, text="ラベルを選択してください。カーソルが変更されます。")
        self.group1.pack(padx=10, pady=5)
        self.windows_native = ["X_cursor","arrow","based_arrow_down","based_arrow_up",
                               "boat","bogosity","bottom_left_corner","bottom_right_corner",
                               "bottom_side","bottom_tee","box_spiral","center_ptr",
                               "circle","clock","coffee_mug","cross",
                               "cross_reverse","crosshair","diamond_cross","dot",
                               "dotbox","double_arrow","draft_large","draft_small",
                               "draped_box","exchange","fleur","gobbler",
                               "gumby","hand1","hand2","heart",
                               "ibeam","icon","iron_cross","left_ptr",
                               "left_side","left_tee","leftbutton","ll_angle",
                               "lr_angle","man","middlebutton","mouse",
                               "none","pencil","pirate","plus",
                               "question_arrow","right_ptr","right_side","right_tee",
                               "rightbutton","rtl_logo","sailboat","sb_down_arrow",
                               "sb_h_double_arrow","sb_left_arrow","sb_right_arrow","sb_up_arrow",
                               "sb_v_double_arrow","shuttle","sizing","spider",
                               "spraycan","star","target","tcross",
                               "top_left_arrow","top_left_corner","top_right_corner","top_side",
                               "top_tee","trek","ul_angle","umbrella",
                               "ur_angle","watch","xterm",]
        for i, c in enumerate(self.windows_native):
            l = tk.Label(self.group1, text=c, cursor=c, bg="white", font=(22))
            l.grid(row=i//4, column=i%4, padx=3, pady=3, sticky=tk.W+tk.E)
if __name__ == "__main__":
    cursorTest = CursorTest()
    cursorTest.mainloop()