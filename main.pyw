"""Application meant to show the time in a binary representation"""
from datetime import datetime
from tkinter import Canvas, Label, Tk


class App(Tk):

    def __init__(self):
        super().__init__()

        self.resizable(False, False)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.geometry("+0+0")
        self.config(
            bg="black",
            highlightcolor="white",
            highlightthickness=1
        )

        self.cell_size = 40  # dont render properly under 40
        self.font = f"Arial {self.cell_size//2} bold"
        self.cell_color = "black", "Dark Orange"

        self.start_x, self.start_y = None, None

        self.hour_label = Label(self,
                                text="H",
                                justify="center",
                                font=self.font,
                                bg="black",
                                fg="white",
                                highlightcolor="white",
                                highlightthickness=1
                                )

        self.minute_label = Label(self,
                                  text="M",
                                  justify="center",
                                  font=self.font,
                                  bg="black",
                                  fg="white",
                                  highlightcolor="white",
                                  highlightthickness=1
                                  )

        self.canvas = Canvas(self,
                             width=6*self.cell_size,
                             height=2*self.cell_size,
                             bg="black",
                             highlightcolor="white",
                             highlightthickness=1
                             )

        for index in range(7):
            self.grid_columnconfigure(index=index, minsize=self.cell_size)
        for index in range(2):
            self.grid_rowconfigure(index=index, minsize=self.cell_size)

        self.hour_label.grid(row=0, column=0, sticky="nesw")
        self.minute_label.grid(row=1, column=0, sticky="nesw")
        self.canvas.grid(row=0, column=1, rowspan=2, columnspan=6)

        self.bind("<Escape>", lambda _: self.destroy())
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.do_move)
        self.bind("<ButtonRelease-1>", self.stop_move)

    def update_clock(self):

        current = datetime.now()
        self.update_display(current.hour, current.minute)
        self.after(1000, self.update_clock)

    def update_display(self, hour, minute):

        time_values = [32, 16, 8, 4, 2, 1]

        # draw the hour row
        for index, value in enumerate(time_values):
            fill_color = self.cell_color[hour >= value]
            if hour >= value:
                hour -= value
            self.canvas.create_rectangle(
                index*self.cell_size,
                0,
                (index+1)*self.cell_size+1,
                self.cell_size,
                fill=fill_color,
                outline="white",
                width=1
            )

        # draw the minute row
        for index, value in enumerate(time_values):
            fill_color = self.cell_color[minute >= value]
            if minute >= value:
                minute -= value
            self.canvas.create_rectangle(
                index*self.cell_size,
                self.cell_size+1,
                (index+1)*self.cell_size+1,
                self.cell_size*2+1,
                fill=fill_color,
                outline="white",
                width=1
            )

    def start(self):
        self.update_clock()
        self.mainloop()

    def start_move(self, event):
        self.start_x, self.start_y = event.x, event.y

    def do_move(self, event):
        self.geometry(f"+{self.winfo_x() + event.x - self.start_x}" +
                      f"+{self.winfo_y() + event.y - self.start_y}")

    def stop_move(self, _):
        self.start_x, self.start_y = None, None


if __name__ == "__main__":
    App().start()
