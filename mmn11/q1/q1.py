import tkinter as tk
from enum import Enum

class Color(Enum):
    WHITE = 0
    BLACK = 1
    GREEN = 2
    PURPLE = 3
    BLUE = 4

rules = [
    [[Color.BLACK, Color.WHITE, Color.WHITE, Color.WHITE, Color.WHITE], Color.WHITE],
    [[Color.BLACK, Color.BLACK, Color.WHITE, Color.WHITE, Color.BLACK], Color.WHITE],
    [[Color.BLACK, Color.WHITE, Color.BLACK, Color.WHITE, Color.WHITE], Color.PURPLE],
    [[Color.BLACK, Color.WHITE, Color.BLACK, Color.WHITE, Color.PURPLE], Color.PURPLE],
    [[Color.BLACK, Color.WHITE, Color.WHITE, Color.BLACK, Color.WHITE], Color.PURPLE],
    [[Color.BLACK, Color.PURPLE, Color.WHITE, Color.BLACK, Color.WHITE], Color.PURPLE],
    [[Color.BLACK, Color.BLACK, Color.WHITE, Color.WHITE, Color.WHITE], Color.BLUE],
    [[Color.BLACK, Color.BLACK, Color.WHITE, Color.BLUE, Color.WHITE], Color.BLUE],
    [[Color.BLACK, Color.WHITE, Color.BLUE, Color.WHITE, Color.BLACK], Color.BLUE],
    [[Color.BLACK, Color.WHITE, Color.WHITE, Color.WHITE, Color.BLACK], Color.BLUE],
    [[Color.BLACK, Color.PURPLE, Color.BLUE, Color.BLUE, Color.PURPLE], Color.GREEN]
]


class CellGrid(tk.Tk):
    def __init__(self, rows, cols, cell_size=20):
        super().__init__()
        
        self.title("Non Symmetrical Cross Eliminator")
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        
        self.cells = [[None for _ in range(cols)] for _ in range(rows)]
        self.colors = [[Color.WHITE for _ in range(cols)] for _ in range(rows)]  

        self.canvas = tk.Canvas(self, width=cols * cell_size, height=rows * cell_size)
        self.canvas.pack()

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        clear_button = tk.Button(button_frame, text="Clear Grid", command=self.clear_grid)
        clear_button.grid(row=0, column=0, padx=5)
        start_button = tk.Button(button_frame, text="Step", command=self.step)
        start_button.grid(row=0, column=1, padx=5)
        self.create_grid()
        
    def create_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                cell = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                self.cells[row][col] = cell
                self.canvas.tag_bind(cell, "<Button-1>", lambda event, r=row, c=col: self.toggle_cell(r, c))

    def clear_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.canvas.itemconfig(self.cells[row][col], fill="white")
                self.colors[row][col] = Color.WHITE

    def check_von_neumann(self, row, col):
        for rule, result in rules:
            if self.colors[row][col]==rule[0] and (row==0 or self.colors[row-1][col]==rule[1]) and (col==self.cols-1 or self.colors[row][col+1]==rule[2]) and (row==self.rows-1 or self.colors[row+1][col]==rule[3]) and (col==0 or self.colors[row][col-1]==rule[4]):
                return result
        return -1

    def has_neighbor(self, row, col, color):
        if (row>0 and self.colors[row-1][col]==color) or (row<self.rows-1 and self.colors[row+1][col]==color) or (col>0 and self.colors[row][col-1]==color) or (col<self.cols-1 and self.colors[row][col+1]==color):
            return True
        return False
    
    def step(self):
        self.update_colors(self.update_board())

    def update_board(self):
        to_color = []
        for row in range(self.rows):
            for col in range(self.cols):
                cur_color = self.colors[row][col]
                if cur_color!=Color.WHITE and cur_color!=Color.GREEN: #white and green are stable states
                    if self.has_neighbor(row, col, Color.GREEN): #if cell has green neighbor it becomes green
                        new_color = Color.GREEN
                    #blue and purple can't be neighbors - move into SELF DESTRUCTION    
                    elif cur_color == Color.PURPLE and self.has_neighbor(row, col, Color.BLUE) or cur_color == Color.BLUE and self.has_neighbor(row, col, Color.PURPLE):
                        new_color = Color.WHITE
                    #check rules    
                    else:
                        new_color = self.check_von_neumann(row, col)
                    if new_color==-1 and cur_color==Color.BLACK and (self.has_neighbor(row, col, Color.PURPLE) or self.has_neighbor(row, col, Color.BLUE)):
                        new_color = Color.WHITE
                    if new_color==-1 and cur_color == Color.PURPLE and ((row<self.rows-1 and self.colors[row+1][col]==Color.WHITE) and (col<self.cols-1 and self.colors[row][col+1]==Color.WHITE)):
                        new_color = Color.WHITE 
                    if new_color==-1 and cur_color == Color.BLUE and ((row>0 and self.colors[row-1][col]==Color.WHITE) and (col>0 and self.colors[row][col-1]==Color.WHITE)):
                        new_color = Color.WHITE     
                    if new_color != -1:
                        to_color.append([row, col, new_color])
        
        return to_color
    
    
    def update_colors(self, to_color):
        for row, col, new_color in to_color:
            self.colors[row][col] = new_color                
            match new_color:
                case Color.WHITE:
                    self.canvas.itemconfig(self.cells[row][col], fill="white")
                case Color.GREEN:
                    self.canvas.itemconfig(self.cells[row][col], fill="green")
                case Color.BLUE:
                    self.canvas.itemconfig(self.cells[row][col], fill="blue") 
                case Color.PURPLE:
                    self.canvas.itemconfig(self.cells[row][col], fill="purple")            
        self.canvas.update_idletasks()



    def toggle_cell(self, row, col):
        if self.colors[row][col] == Color.WHITE:
            self.canvas.itemconfig(self.cells[row][col], fill="black")
            self.colors[row][col] = Color.BLACK
        else:
            self.canvas.itemconfig(self.cells[row][col], fill="white")
            self.colors[row][col] = Color.WHITE

grid = CellGrid(20, 20, cell_size=20)
grid.mainloop()
