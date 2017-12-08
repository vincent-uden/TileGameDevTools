import tkinter as tk
import os
from tkinter import ttk
from tkinter.filedialog import askopenfilename

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
		tiles.append(["NONE" for x1 in range(x)])

def export_input(box1, box2, frame):
	inp1 = box1.get()
	inp2 = box2.get()
	try:
		x = int(inp1)
		y = int(inp2)
		set_dimensions(x, y)
		app.frames[StartPage].render_tiles()
		frame.destroy()
	except ValueError:
		pass


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

def open_map(frame):
	current_path = os.path.dirname(os.path.abspath(__file__))
	name = askopenfilename(initialdir=current_path, filetypes=(("Map files", "*.txt"), ("All files", "*.*")), title="Choose a file")
	try:
		input_map = open(name)
	except:
		return
	data = input_map.read()
	input_map.close()
	data = data.split("\n")[:-1]
	new_data = []
	while tiles != []:
		tiles.pop()
	for row in data:
		tiles.append(row.split(" "))
	frame.render_tiles()

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
		file_menu.add_command(label="Open", command=lambda:open_map(self.frames[StartPage]))
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

		self.selected_colour = "Red"
		self.colors = {
					   "Red"  : ("#ff0000", "RED1"),
					   "Green": ("#00ff00", "LGRE"),
					   "Blue" : ("#2659f2", "WBLU"),
					   "Brown": ("#9b6700", "BRWN"),
					   "Black": ("#000000", "BLCK")
					   }
		self.internal_colors = {
								"NONE":"#ffffff",
								"RED1":"#ff0000",
								"LGRE":"#00ff00",
								"WBLU":"#2659f2",
								"BRWN":"#9b6700",
								"BLCK":"#000000"
								}

		default_color = tk.StringVar(self)
		default_color.set("Red")

		right_frame = tk.Frame(self)
		right_frame.grid(column=1, row=0, sticky="N")

		color_menu = tk.OptionMenu(right_frame, default_color, *list(self.colors.keys()), command=self.select_material)
		color_menu.grid(column=0, row=0, sticky="EW")

		# Tools
		size_label = tk.Label(right_frame, text="Brush size", font=SMALL_FONT)
		size_label.grid(row=1)

		default_size = tk.IntVar(self)
		default_size.set(1)
		self.brush_size = tk.Scale(right_frame, from_=1, to=15, orient=tk.HORIZONTAL, variable=default_size, command=self.select_size)
		self.brush_size.grid(row=2)

		brush_tool = ttk.Button(right_frame, text="Draw",
								command=lambda:self.select_tool(self.draw))
		brush_tool.grid(row=3)

		erase_tool = ttk.Button(right_frame, text="Erase",
								command=lambda:self.select_tool(self.erase))
		erase_tool.grid(row=4)

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
	
	def erase(self, event):
		x = event.x
		y = event.y
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
		y_dim = len(tiles[0])
		for y, row in enumerate(tiles):
			for x, item in enumerate(row):
				self.canvas.create_rectangle(x * 20, y * 20, (x + self.selected_size) * 20, (y + self.selected_size) * 20, fill=self.internal_colors[item], width=0)

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
