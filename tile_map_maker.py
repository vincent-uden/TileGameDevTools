import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 9)

tiles = []

mouse_pressed = False
# TODO: Change to save different material types
def set_dimensions(x, y):
    """
    Populates tiles with None to according to x and y.
    :param x: Int
    :param y: Int
    :return: None
    """
    while tiles != []:
        tiles.pop()
    for y1 in range(y):
        tiles.append([None for x1 in range(x)])

def export_input(box1, box2):
    inp1 = box1.get()
    inp2 = box2.get()
    try:
        x = int(inp1)
        y = int(inp2)
        set_dimensions(x, y)
    except ValueError:
        win = tk.Toplevel(padx=20, pady=20)
        win.wm_title("Error")
        l = tk.Label(win, text="Please enter two integers", font=LARGE_FONT)
        l.pack(side=tk.TOP)


def new_map_popup():
    win = tk.Toplevel(padx=20, pady=20)
    win.wm_title("New Map")

    l = tk.Label(win, text="Choose dimensions", font=LARGE_FONT)
    l.pack(side=tk.TOP)

    dim_frame = tk.Frame(win)
    x_l = tk.Label(dim_frame, text="X:")
    x_l.pack(side=tk.LEFT)
    x_box = tk.Entry(dim_frame, exportselection=0)
    x_box.pack(side=tk.LEFT)

    y_box = tk.Entry(dim_frame, exportselection=0)
    y_box.pack(side=tk.RIGHT)
    y_l = tk.Label(dim_frame, text="Y:")
    y_l.pack(side=tk.RIGHT)
    dim_frame.pack()

    confirm = ttk.Button(win, text="Confirm",
                         command=lambda: export_input(x_box, y_box))
    confirm.pack(side=tk.BOTTOM, pady=20)

def save_map(name, window):
    output = open(f"{name}.txt", "w")
    for row in tiles:
        text_row = " ".join([str(x) for x in row])
        output.write(text_row)
        output.write("\n")
    output.close()
    window.destroy()

def save_map_popup():
    win = tk.Toplevel(padx=20, pady=20)
    win.wm_title("Save Map")

    l = tk.Label(win, text="Enter map name", font=LARGE_FONT)
    l.pack(side=tk.TOP)

    name_box = tk.Entry(win, exportselection=0)
    name_box.pack()
    name_box.bind("<Return>", lambda event: save_map(name_box.get(), win))

    save_button = ttk.Button(win, text="Confirm",
                             command=lambda: save_map(name_box.get(), win))
    save_button.pack()

# This class will be root frame
class TileMapCreator(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self ,*args, **kwargs)

        tk.Tk.wm_title(self, "Tile Map Creator 1.0")

        container = tk.Frame(self, padx=0, pady=0)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}

        for F in (StartPage, Page2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        menu_bar = tk.Menu(self)
        # TODO: Add open(load) functionality
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New Map", command=new_map_popup)
        file_menu.add_command(label="Save", command=save_map_popup)
        file_menu.add_command(label="Open")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menu_bar)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(self, width=800, height=800, background="white")
        self.canvas.grid(column=0, row=0)
        set_dimensions(40, 40)

        self.selected_tool = self.draw
        self.selected_size = 1

        self.canvas.bind("<Button-1>", self.selected_tool)
        self.canvas.bind("<B1-Motion>", self.selected_tool)

        self.selected_colour = "Erase"
        self.colors = {
                       "Erase": ("#ffffff", "None"),
                       "Red"  : ("#ff0000", "RED1"),
                       "Green": ("#00ff00", "LGRE"),
                       "Blue" : ("#2659f2", "WBLU"),
                       "Brown": ("#9b6700", "BRWN")
                       }

        default_color = tk.StringVar(self)
        default_color.set("Erase")

        right_frame = tk.Frame(self)
        right_frame.grid(column=1, row=0, sticky="N")

        color_menu = tk.OptionMenu(right_frame, default_color, *list(self.colors.keys()), command=self.select_material)
        color_menu.grid(column=0, row=0, sticky="EW")

        # Tools
        brush_tool = ttk.Button(right_frame, text="Brush",
                                command=lambda:self.select_tool(self.draw))
        brush_tool.grid(row=1)

        default_size = tk.IntVar(self)
        default_size.set(1)
        self.brush_size = tk.Scale(right_frame, from_=1, to=15, orient=tk.HORIZONTAL, variable=default_size, command=self.select_size)
        self.brush_size.grid(row=2)

    def draw(self, event):
        x = event.x
        y = event.y
        x = x // 20 * 20
        y = y // 20 * 20
        self.canvas.create_rectangle(x, y, x + self.selected_size * 20, y + self.selected_size * 20, fill=self.colors[self.selected_colour], width=0)
        for ix in range(self.selected_size):
            for iy in range(self.selected_size):
                try:
                    tiles[(y + iy * 20) // 20][(x + ix * 20) // 20] = self.colors[self.selected_colour][1]
                except:
                    pass

    def select_material(self, mat):
        self.selected_colour = mat

    def select_tool(self, tool):
        self.selected_tool = tool
        self.canvas.bind("<Button-1>", self.selected_tool)
        self.canvas.bind("<B1-Motion>", self.selected_tool)

    def select_size(self, size):
        self.selected_size = int(size)



class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


app = TileMapCreator()
app.mainloop()

