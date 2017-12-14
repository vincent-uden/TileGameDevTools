import tkinter as tk
import os
from math import pi
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory

LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 9)

tiles = []
tile_set = {}
tile_rotations = {}

mouse_pressed = False
def set_dimensions(x, y, c):
    """
    Populates tiles with None to according to x and y.
    :param x: Int
    :param y: Int
    :return: None
    """
    while tiles != []:
        tiles.pop()
    for y1 in range(y):
        tiles.append(["NONE" for x1 in range(x)])
    c.config(scrollregion=(0, 0, x*20, y*20))
    print(x, y)
    if x >= 40:
        c.config(width=800)
    else:
        c.config(width=x*20)
    if y >= 40:
        c.config(height=800)
    else:
        c.config(height=y*20)

def export_input(box1, box2, frame):
    inp1 = box1.get()
    inp2 = box2.get()
    try:
        x = int(inp1)
        y = int(inp2)
        app.frames[StartPage].set_canvas_dim(x, y)
        while tiles != []:
            tiles.pop()
        for y1 in range(y):
            tiles.append(["NONE" for x1 in range(x)])

        app.frames[StartPage].render_tiles()
        frame.destroy()
    except ValueError:
        pass

def new_map_popup():
    # TODO: Fix, doesnt resize properly
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
                         command=lambda: export_input(x_box, y_box, win))
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

def save_map1():
    current_path = os.path.dirname(os.path.abspath(__file__))
    name = asksaveasfilename(initialdir=current_path, filetypes=(("Map files", "*.txt"), ("All files", "*.*")), title="Choose a file", defaultextension=".txt")
    if name is None:
        return
    file = open(name, mode="w")
    for row in tiles:
        text_row = " ".join([str(x) for x in row])
        file.write(text_row)
        file.write("\n")
    file.close()

def open_map(frame):
    current_path = os.path.dirname(os.path.abspath(__file__))
    name = askopenfilename(initialdir=current_path, filetypes=(("Map files", "*.txt"), ("All files", "*.*")), title="Choose a file")
    try:
        input_map = open(name)
    except:
        raise IOError
    data = input_map.read()
    input_map.close()
    data = data.split("\n")[:-1]
    new_data = []
    while tiles != []:
        tiles.pop()
    for row in data:
        tiles.append(row.split(" "))
    frame.render_tiles()

def import_tile_set(frame):
    current_path = os.path.dirname(os.path.abspath(__file__))
    directory = askdirectory(title="Choose a the directory of the tile set")
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            base_name = filename.split(".")[0]
            img = Image.open(directory + "/" + filename)
            #                      Image             ,   rot_angle
            tile_set[base_name] = []
            for i in range(4):
                rotated_img = img.rotate(i * 90)
                new_img = ImageTk.PhotoImage(rotated_img)
                tile_set[base_name].append(new_img)
            tile_rotations[base_name] = 0
    frame.update_color_menu()

def get_tile(tile):
    return tile_set[tile][tile_rotations[tile]]

def rotate_tile(tile, angle):
    tile_rotations[tile] = (tile_rotations[tile] + angle) % 4

def rotate_tile_abs(tile, angle):
    tile_rotations[tile] = angle

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
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New Map", command=new_map_popup)
        file_menu.add_command(label="Save", command=save_map1)
        file_menu.add_command(label="Open", command=lambda:open_map(self.frames[StartPage]))
        file_menu.add_command(label="Import Tile Set", command=lambda:import_tile_set(self.frames[StartPage]))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menu_bar)
        self.resizable(width=False, height=False)
        self.geometry("920x820")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        left_frame = tk.Frame(self)
        left_frame.grid(column=0, row=0, sticky="NW")


        self.canvas = tk.Canvas(left_frame, background="white", scrollregion=(0,0,800,800))
        self.canvas.grid(column=0, row=0)
        set_dimensions(60, 60, self.canvas)

        self.selected_tool = self.draw_event_pp
        self.selected_size = 1

        self.canvas.bind("<Button-1>", self.selected_tool)
        self.canvas.bind("<B1-Motion>", self.selected_tool)

        self.selected_colour = "Red"
        self.colors = {
                       "Red"        : ("#ff0000", "RED1"),
                       "Green"      : ("#00ff00", "LGRE"),
                       "Dark Green" : ("#008c00", "DGRE"),
                       "Blue"       : ("#2659f2", "WBLU"),
                       "Brown"      : ("#824900", "BRWN"),
                       "Black"      : ("#000000", "BLCK")
                       }
        self.internal_colors = {
                                "NONE":"#ffffff",
                                "RED1":"#ff0000",
                                "LGRE":"#00ff00",
                                "WBLU":"#2659f2",
                                "BRWN":"#9b6700",
                                "BLCK":"#000000",
                                "DGRE":"#008c00"
                                }

        self.default_color = tk.StringVar(self)
        self.default_color.set("Red")

        right_frame = tk.Frame(self)
        right_frame.grid(column=2, row=0, sticky="N")

        # Scroll bars
        self.hbar = tk.Scrollbar(left_frame, orient=tk.HORIZONTAL)
        self.hbar.grid(column=0, row=1, sticky="WE")
        self.hbar.config(command=self.canvas.xview)
        self.vbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.vbar.grid(column=1, row=0, sticky="NS")
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

        

        self.color_menu = tk.OptionMenu(right_frame, self.default_color, *list(self.colors.keys()), command=self.select_material)
        self.color_menu.grid(column=0, row=0, sticky="EW")

        self.selected_tile = None

        # Tools
        size_label = tk.Label(right_frame, text="Brush size", font=SMALL_FONT)
        size_label.grid(row=1)

        default_size = tk.IntVar(self)
        default_size.set(1)
        self.brush_size = tk.Scale(right_frame, from_=1, to=15, orient=tk.HORIZONTAL, variable=default_size, command=self.select_size)
        self.brush_size.grid(row=2)

        brush_tool = ttk.Button(right_frame, text="Draw",
                                command=lambda:self.select_tool(self.draw_event_pp))
        brush_tool.grid(row=3)

        erase_tool = ttk.Button(right_frame, text="Erase",
                                command=lambda:self.select_tool(self.erase_event_pp))
        erase_tool.grid(row=4)

        rot_label = tk.Label(right_frame, text="Rotate Texture", font=SMALL_FONT)
        rot_label.grid(row=5)
        rot_clockwise  = ttk.Button(right_frame, text=" 90°", command=lambda:rotate_tile(self.selected_tile, 1))
        rot_countclock = ttk.Button(right_frame, text="-90°", command=lambda:rotate_tile(self.selected_tile, -1))
        rot_clockwise.grid(row=6)
        rot_countclock.grid(row=7)

        self.grid_propagate(0)
        self.configure(height=850, width=950)
        left_frame.grid_propagate(0)
        left_frame.configure(height=850, width=800)
    
    def set_canvas_dim(self, x, y):
        self.canvas.config(scrollregion=(0, 0, x*20, y*20))
        if x >= 40:
            self.canvas.config(width=800)
        else:
            self.canvas.config(width=x*20)
        if y >= 40:
            self.canvas.config(height=800)
        else:
            self.canvas.config(height=y*20)
        
    def update_color_menu(self):
        self.default_color.set("")
        self.color_menu["menu"].delete(0, "end")

        for choice in tile_set.keys():
            self.color_menu["menu"].add_command(label=choice, command=lambda v=choice: self.select_tile(v))

    def draw_event_pp(self, event):
        x = int(self.canvas.canvasx(event.x))
        y = int(self.canvas.canvasy(event.y))
        self.draw(x, y)

    def draw(self, x, y):
        x = int(x // 20 * 20)
        y = int(y // 20 * 20)
        if self.selected_colour != None:
            self.canvas.create_rectangle(x, y, x + self.selected_size * 20, y + self.selected_size * 20, fill=self.colors[self.selected_colour], width=0)
            for ix in range(self.selected_size):
                for iy in range(self.selected_size):
                    try:
                        tiles[(y + iy * 20) // 20][(x + ix * 20) // 20] = self.colors[self.selected_colour][1]
                    except:
                        pass
        else:
            for ix in range(self.selected_size):
                for iy in range(self.selected_size):
                    self.canvas.create_image(x + ix * 20 + 10, y + iy * 20 + 10, image=get_tile(self.selected_tile))
                    try:
                        tiles[(y + iy * 20) // 20][(x + ix * 20) // 20] = str(tile_rotations[self.selected_tile]) + self.selected_tile
                    except:
                        pass

    def erase_event_pp(self, event):
        x = int(self.canvas.canvasx(event.x))
        y = int(self.canvas.canvasy(event.y))
        self.erase(x, y)

    def erase(self, x, y):
        x = x // 20 * 20
        y = y // 20 * 20
        self.canvas.create_rectangle(x, y, x + self.selected_size * 20, y + self.selected_size * 20, fill="white", width=0)
        for ix in range(self.selected_size):
            for iy in range(self.selected_size):
                try:
                    tiles[(y + iy * 20) // 20][(x + ix * 20) // 20] = "NONE"
                except:
                    pass

    def render_tiles(self):
        y_dim = len(tiles)
        x_dim = len(tiles[0])
        self.set_canvas_dim(x_dim, y_dim)
        for y, row in enumerate(tiles):
            for x, item in enumerate(row):
                if item in list(self.internal_colors.keys()):
                    self.canvas.create_rectangle(x * 20, y * 20, (x + self.selected_size) * 20, (y + self.selected_size) * 20, fill=self.internal_colors[item], width=0)
                elif item[1::] in list(tile_set):
                    self.select_tile(item[1::])
                    rotate_tile_abs(item[1::], int(item[0]))
                    self.draw(x * 20, y * 20)

    def select_material(self, mat):
        self.selected_colour = mat
        self.selected_tile = None
    
    def select_tile(self, tile):
        self.selected_tile = tile
        self.selected_colour = None
        self.default_color = tile

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
