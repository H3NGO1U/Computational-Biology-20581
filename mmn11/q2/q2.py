
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import random 
import numpy as np 
from tkinter import messagebox

CITY_INITIAL_POLLUTION = 10
CITY_POLLUTION_PRODUCE = 0.0001
MAX_WIND_POWER = 10
MIN_WIND_POWER = 0
MID_WIND_POWER = 6
MAX_POLLUTION_LEVEL = 10
MIN_POLLUTION_LEVEL = 0
MID_POLLUTION_LEVEL = 6
MAX_TEMP = 50
MIN_TEMP = -9
MAX_CLOUD = 10
MIN_CLOUD = 0
MID_CLOUD = 6
CELL_SIZE = 60

def create_plots(pollution_measures, temp_measures, clouds_measures, wind_measures):
   iters = len(pollution_measures)
   dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq='D').strftime('%d-%m')[:iters]
   dates_for_plot = pd.date_range(start="2024-01-01", end="2024-12-31", freq='MS').strftime('%d-%m')
   data = {
      "Pollution Level": pollution_measures,
      "Temperature": temp_measures,
      "Cloudiness": clouds_measures,
      "Wind Power": wind_measures
   }
   df = pd.DataFrame(data, index=dates)
   fig, axes = plt.subplots(len(df.columns), 1, figsize=(12, 10))
   for i, column in enumerate(df.columns):
      axes[i].plot(df.index, df[column])
      axes[i].axhline(0, color='red', linestyle='--')
      axes[i].set_title(f"{column} Throughout a Year")
      axes[i].set_xticks(dates_for_plot)
      axes[i].set_xlim([df.index.min(), df.index.max()])      
   plt.tight_layout(pad=4)
   plt.show()


cell_types = ["Desert", "Sea", "City", "Forest", "Mountain"]

cell_colors = {"Desert": "orange", "Sea": "blue", "City": "gray", "Forest": "green", "Mountain":"#66480b"}
clouds_probs = {"Desert": 0.2, "Sea": 0.7, "City": 0.6, "Forest": 0.6, "Mountain":0.9}
rain_probs = {"Strong": 0.9, "Weak":0.5, "None":0}
wind_probs = {"Desert": 0.1, "Sea": 0.5, "City": 0.2, "Forest": 0.3, "Mountain":0.5}
directions = {
    "north": (0, -1),
    "north_east": (1, -1),
    "east": (1, 0),
    "south_east": (1, 1),
    "south": (0, 1),
    "south_west": (-1, 1),
    "west": (-1, 0),
    "north_west": (-1, -1)
}

pollution_levels = [{"level":"A", "color":"#2e6303"}, {"level":"A", "color":"#2e6303"}, {"level":"A", "color":"#2e6303"}, {"level":"B", "color":"#77e022"},{"level":"B", "color":"#77e022"}, {"level":"C", "color":"#c45b0a"},{"level":"C", "color":"#c45b0a"}, {"level":"D", "color":"#993003"}, {"level":"D", "color":"#993003"}, {"level":"E", "color":"#780905"}, {"level":"E", "color":"#780905"}]

def check_wind(cell, direction):
   return cell.wind_power()!="None" and cell.wind.direction==direction

def draw_cloud(canvas, row, col, clouds):
    x = col*CELL_SIZE
    y = row*CELL_SIZE
    offsetX = CELL_SIZE//6
    offsetY = CELL_SIZE//(4*6)
    ball_size = 1.5*offsetX
    if clouds=="Strong":
       color = "#3d3c3b" #gray
    elif clouds=="Weak":
       color = "white"
    else:
       return      
    canvas.create_oval(x+offsetX, y, x+offsetX+ball_size, y+ball_size, fill=color, outline=color)
    canvas.create_oval(x+2*offsetX, y, x+2*offsetX+ball_size, y+ball_size, fill=color, outline=color)
    canvas.create_oval(x+3*offsetX, y+2*offsetY, x +3*offsetX+ball_size, y +2*offsetY+ball_size, fill=color, outline=color)
    canvas.create_oval(x+2*offsetX, y+3*offsetY, x + 2*offsetX+ball_size, y+3*offsetY+ball_size, fill=color, outline=color)
    canvas.create_oval(x+offsetX, y+3*offsetY, x+offsetX+ball_size, y+3*offsetY+ball_size, fill=color, outline=color)
    canvas.create_oval(x, y+2*offsetY, x+ball_size, y+2*offsetY+ball_size, fill=color, outline=color)


def draw_rain(canvas, row, col, raining: bool, temp: int):
    if not raining:
       return 
    x = col*CELL_SIZE
    y = row*CELL_SIZE
    drop_length = CELL_SIZE//10
    offsetY = CELL_SIZE//2
    offsetX = CELL_SIZE//2-drop_length
    color = "black" if temp>0 else "white"
    canvas.create_line(x+offsetX+2*drop_length, y+offsetY, x+offsetX+2*drop_length, y+offsetY+drop_length, fill=color, width=1)
    canvas.create_line(x+offsetX, y+offsetY, x+offsetX, y+offsetY+drop_length, fill=color, width=1)
    canvas.create_line(x+offsetX+drop_length,y+ offsetY, x+offsetX+drop_length, y+offsetY+drop_length, fill=color, width=1)
    canvas.create_line(x+offsetX+2*drop_length, y+offsetY+drop_length*2, x+offsetX+2*drop_length, y+offsetY+drop_length*3, fill=color, width=1)
    canvas.create_line(x+offsetX, y+offsetY+drop_length*2, x+offsetX,y+ offsetY+drop_length*3, fill=color, width=1)
    canvas.create_line(x+offsetX+drop_length, y+offsetY+drop_length*2, x+offsetX+drop_length,y+ offsetY+drop_length*3, fill=color, width=1)

class Wind:
   def __init__(self, power: int, direction: str):
      if not isinstance(power, int):
         power = 0
      self.power = min(max(power, MIN_WIND_POWER), MAX_WIND_POWER) # Normalize the value

      if direction in directions:
        self.direction = direction
      else:
        self.direction = "-"

def draw_wind(canvas, wind: Wind, row, col):
  x = col*CELL_SIZE
  y = row*CELL_SIZE
  if wind.direction == "-":
      return
  arrow_length = CELL_SIZE//4
  if power(wind.power, MID_WIND_POWER)=="Strong":
    canvas.create_line(x+0.6*CELL_SIZE, y + 0.8*CELL_SIZE,x + 0.6*CELL_SIZE + directions[wind.direction][0]*arrow_length, y + 0.8*CELL_SIZE + directions[wind.direction][1]*arrow_length, fill="black", width=2, arrow=tk.LAST) 

  canvas.create_line(x+0.8*CELL_SIZE, y + 0.8*CELL_SIZE,x + 0.8*CELL_SIZE + directions[wind.direction][0]*arrow_length, y + 0.8*CELL_SIZE + directions[wind.direction][1]*arrow_length, fill="black", width=2, arrow=tk.LAST) 
         
def draw_temperature(canvas, row, col, temperature: int):
    x = col*CELL_SIZE
    y = row*CELL_SIZE
    canvas.create_text(x+CELL_SIZE//6, y+CELL_SIZE//2, text=str(int(temperature))+"°", fill="black", font=("Arial", CELL_SIZE//6))

def draw_pollution(canvas, row, col, pollution_level: int): 
   x = col*CELL_SIZE
   y = row*CELL_SIZE  
   canvas.create_text(x+CELL_SIZE*0.8, y+CELL_SIZE//2, text=pollution_levels[int(pollution_level)]["level"], fill=pollution_levels[int(pollution_level)]["color"], font=("Arial", CELL_SIZE//6, "bold"))

def power(parameter, MID_VALUE):
      if parameter == 0:
         return "None"
      elif parameter < MID_VALUE:
          return "Weak" 
      else:
         return "Strong"

# to get from the neighbor something by wind
# e.g pollution or clouds      
def get_neighbors(value, wind_power):
   if value=="Strong" and wind_power=="Strong":
      return 0.2
   if value=="Weak" and wind_power=="Strong" or value=="Strong":
      return 0.01
   return 0
   
def normalize(data):
   return (data - np.mean(data)) / np.std(data)  
   
class EnvironmentCell:
    def __init__(self, type: str, temp: int, wind: Wind, pollution_level: int, clouds: int, rain: bool = False):
        self.type = type
        self.temp = min(max(temp, MIN_TEMP), MAX_TEMP)
        self.wind = wind
        self.pollution_level = min(max(pollution_level, MIN_POLLUTION_LEVEL), MAX_POLLUTION_LEVEL)
        self.clouds = min(max(clouds, MIN_CLOUD), MAX_CLOUD)
        self.rain = rain

    def clouds_power(self):
       return power(self.clouds, MID_CLOUD)
    
    def pollution_power(self):
       return power(self.pollution_level, MID_POLLUTION_LEVEL)
    
    def wind_power(self):
       return power(self.wind.power, MID_WIND_POWER)
           
    def next_type(self):
      cur_type_index = cell_types.index(self.type)
      next_type_index = (cur_type_index+ 1) % len(cell_types)
      self.type = cell_types[next_type_index]
      return self.type
       
class TheWorld(tk.Tk):
   def __init__(self):
    super().__init__()
    self.running = False
    self.title("The World is WARMING")
    self.cells = [
               [EnvironmentCell(type="Forest", temp=20, wind=Wind(1, "north"), pollution_level=0, clouds=0), EnvironmentCell(type="Forest", temp=20, wind=Wind(3, "north_west"), pollution_level=0, clouds=0), EnvironmentCell(type="Desert", temp=20, wind=Wind(3, "north"), pollution_level=0, clouds=7), EnvironmentCell(type="Mountain", temp=20, wind=Wind(6, "east"), pollution_level=0, clouds=7), EnvironmentCell(type="Mountain", temp=20, wind=Wind(3, "north"), pollution_level=0, clouds=1), EnvironmentCell(type="Mountain", temp=20, wind=Wind(3, "north"), pollution_level=0, clouds=1)],
               [EnvironmentCell(type="City", temp=20, wind=Wind(0, "-"), pollution_level=CITY_INITIAL_POLLUTION, clouds=7), EnvironmentCell(type="City", temp=20, wind=Wind(3, "west"), pollution_level=CITY_INITIAL_POLLUTION, clouds=0),EnvironmentCell(type="Sea", temp=20, wind=Wind(3, "north"), pollution_level=0, clouds=7), EnvironmentCell(type="Sea", temp=20, wind=Wind(0, "-"), pollution_level=0, clouds=1), EnvironmentCell(type="City", temp=20, wind=Wind(3, "north_west"), pollution_level=CITY_INITIAL_POLLUTION, clouds=1), EnvironmentCell(type="Mountain", temp=20, wind=Wind(3, "north"), pollution_level=0, clouds=1)],
               [EnvironmentCell(type="City", temp=20, wind=Wind(0, "-"), pollution_level=CITY_INITIAL_POLLUTION, clouds=3), EnvironmentCell(type="City", temp=20, wind=Wind(3, "west"), pollution_level=CITY_INITIAL_POLLUTION, clouds=1), EnvironmentCell(type="Mountain", temp=20, wind=Wind(7, "north_west"), pollution_level=0, clouds=7), EnvironmentCell(type="Sea", temp=20, wind=Wind(1, "north_west"), pollution_level=0, clouds=7), EnvironmentCell(type="City", temp=20, wind=Wind(5, "north_west"), pollution_level=CITY_INITIAL_POLLUTION, clouds=1),EnvironmentCell(type="Mountain", temp=20, wind=Wind(3, "north"), pollution_level=0, clouds=1)],
               [EnvironmentCell(type="Forest", temp=20, wind=Wind(1, "north_west"), pollution_level=0, clouds=0), EnvironmentCell(type="City", temp=20, wind=Wind(0, "-"), pollution_level=CITY_INITIAL_POLLUTION, clouds=0), EnvironmentCell(type="City", temp=20, wind=Wind(0, "-"), pollution_level=CITY_INITIAL_POLLUTION, clouds=7), EnvironmentCell(type="Sea", temp=20, wind=Wind(3, "north"), pollution_level=0, clouds=0), EnvironmentCell(type="Sea", temp=20, wind=Wind(0, "-"), pollution_level=0, clouds=0), EnvironmentCell(type="Mountain", temp=20, wind=Wind(3, "north"), pollution_level=0, clouds=1)],
               [EnvironmentCell(type="Forest", temp=20, wind=Wind(1, "north_west"), pollution_level=0, clouds=0), EnvironmentCell(type="Forest", temp=20, wind=Wind(3, "north_west"), pollution_level=0, clouds=0), EnvironmentCell(type="Desert", temp=20, wind=Wind(3, "north"), pollution_level=0, clouds=4), EnvironmentCell(type="Mountain", temp=20, wind=Wind(7, "north_west"), pollution_level=0, clouds=7),EnvironmentCell(type="Mountain", temp=20, wind=Wind(3, "north"), pollution_level=0, clouds=1), EnvironmentCell(type="Mountain", temp=20, wind=Wind(3, "north"), pollution_level=0, clouds=1)],
               [EnvironmentCell(type="Forest", temp=20, wind=Wind(1, "north_west"), pollution_level=0, clouds=0), EnvironmentCell(type="Forest", temp=20, wind=Wind(3, "north_west"), pollution_level=0, clouds=0), EnvironmentCell(type="Desert", temp=20, wind=Wind(3, "north"), pollution_level=0, clouds=4),EnvironmentCell(type="Forest", temp=20, wind=Wind(1, "north_west"), pollution_level=0, clouds=7), EnvironmentCell(type="Forest", temp=20, wind=Wind(1, "north_west"), pollution_level=0, clouds=1), EnvironmentCell(type="Mountain", temp=20, wind=Wind(3, "north"), pollution_level=0, clouds=1)],
               [EnvironmentCell(type="Forest", temp=20, wind=Wind(1, "north_west"), pollution_level=0, clouds=0), EnvironmentCell(type="Forest", temp=20, wind=Wind(3, "north_west"), pollution_level=0, clouds=0), EnvironmentCell(type="Desert", temp=20, wind=Wind(3, "north"), pollution_level=0, clouds=4), EnvironmentCell(type="Sea", temp=-9, wind=Wind(3, "north"), pollution_level=0, clouds=7), EnvironmentCell(type="Sea", temp=-9, wind=Wind(0, "-"), pollution_level=0, clouds=1),EnvironmentCell(type="Mountain", temp=20, wind=Wind(3, "north"), pollution_level=0, clouds=1)],
               [EnvironmentCell(type="Forest", temp=20, wind=Wind(1, "north_west"), pollution_level=0, clouds=0), EnvironmentCell(type="Forest", temp=20, wind=Wind(3, "north_west"), pollution_level=0, clouds=0), EnvironmentCell(type="Desert", temp=20, wind=Wind(3, "north"), pollution_level=0, clouds=4), EnvironmentCell(type="Sea", temp=-9, wind=Wind(3, "north"), pollution_level=0, clouds=7), EnvironmentCell(type="Sea", temp=-9, wind=Wind(0, "-"), pollution_level=0, clouds=1), EnvironmentCell(type="Mountain", temp=20, wind=Wind(3, "north"), pollution_level=0, clouds=1)]
         ]
    
    self.rows = len(self.cells)
    self.cols = len(self.cells[0])
    self.drawn_cells = [[None for _ in range(self.cols)] for _ in range(self.rows)]     
    self.canvas = tk.Canvas(self, width=self.cols * CELL_SIZE, height=self.rows * CELL_SIZE)
    self.canvas.pack()
    self.create_grid()
    button_frame = tk.Frame(self)
    button_frame.pack(pady=10)
    run_button = tk.Button(button_frame, text="Run And Draw Each Step", command=self.run_auto_with_draw)
    run_button.grid(row=0, column=0, padx=5)
    start_button = tk.Button(button_frame, text="Step", command=self.update_world_and_draw)
    start_button.grid(row=0, column=1, padx=0)
    run_auto_button = tk.Button(button_frame, text="Run Automatic - Draw Final", command=self.run_auto_no_draw)
    run_auto_button.grid(row=0, column=2, padx=5)
    plot_button = tk.Button(button_frame, text="Show Plots", command=self.measure)
    plot_button.grid(row=0, column=3, padx=5)
    label = tk.Label(button_frame, text="Number of Iterations: ", font=("Arial", 12), fg="darkblue")
    label.grid(row=1, column=0, padx=5)
    self.iterations= tk.Entry(button_frame, width= 5)
    self.iterations.grid(row=1, column=1, padx=5)

   def create_grid(self):
      for row in range(self.rows):
          for col in range(self.cols):
              x1 = col * CELL_SIZE
              x2 = x1 + CELL_SIZE
              y1 = row * CELL_SIZE
              y2 = y1 + CELL_SIZE
              cell = self.cells[row][col]
              if cell.type == "Sea" and cell.temp <= 0:
                 color = "#81dff0"
              else:
                 color = cell_colors[cell.type]  
              cell = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
              self.drawn_cells[row][col] = cell
              self.canvas.tag_bind(cell, "<Button-1>") 
              draw_temperature(self.canvas, row, col, self.cells[row][col].temp)
              draw_pollution(self.canvas, row, col, self.cells[row][col].pollution_level)
              draw_wind(self.canvas, self.cells[row][col].wind, row, col)
              draw_cloud(self.canvas, row, col, self.cells[row][col].clouds_power())
              draw_rain(self.canvas, row, col, self.cells[row][col].rain, self.cells[row][col].temp)
      self.canvas.update_idletasks()

   # def toggle_cell(self, row, col):
   #    self.canvas.itemconfig(self.drawn_cells[row][col], fill=cell_colors[self.cells[row][col].type])
   def run_auto_with_draw(self):
      try:
         iters = int(self.iterations.get())
      except Exception:
         iters = 0 
      if iters>50:
         messagebox.showerror("Error", "To draw more than 50 iterations is crazy - be more moderate")
         return      
      for i in range(iters):
         self.after(100, self.update_world_and_draw())

   def run_auto_no_draw(self):
      try:
         iters = int(self.iterations.get())
      except Exception:
         iters = 0  
      if iters==0:
         return    
      for i in range(iters-1):
         self.update_world()
      self.update_world_and_draw()   

   def stop(self):
      self.running = False

   def measure(self):
      iters = 365  
      pollution_measures = [0 for _ in range(iters+1)]
      temp_measures = [0 for _ in range(iters+1)]
      clouds_measures = [0 for _ in range(iters+1)]
      wind_measures = [0 for _ in range(iters+1)]   
      pollution_measures[0]=np.mean([cell.pollution_level for row in self.cells for cell in row])
      temp_measures[0]= np.mean([cell.temp for row in self.cells for cell in row])
      clouds_measures[0]= np.mean([cell.clouds for row in self.cells for cell in row])
      wind_measures[0]= np.mean([cell.wind.power for row in self.cells for cell in row])
      
      pollution_std = [0 for _ in range(iters+1)]
      temp_std = [0 for _ in range(iters+1)]
      clouds_std = [0 for _ in range(iters+1)]
      wind_std = [0 for _ in range(iters+1)]   
      pollution_std[0]=np.std([cell.pollution_level for row in self.cells for cell in row])
      temp_std[0]= np.std([cell.temp for row in self.cells for cell in row])
      clouds_std[0]= np.std([cell.clouds for row in self.cells for cell in row])
      wind_std[0]= np.std([cell.wind.power for row in self.cells for cell in row])
  
      for i in range(iters):
         if i==iters-1:
            self.update_world_and_draw()
         else:
            self.update_world()   
         pollution_measures[i+1]= np.mean([cell.pollution_level for row in self.cells for cell in row])
         temp_measures[i+1]= np.mean([cell.temp for row in self.cells for cell in row])
         clouds_measures[i+1]= np.mean([cell.clouds for row in self.cells for cell in row])
         wind_measures[i+1]= np.mean([cell.wind.power for row in self.cells for cell in row])
         pollution_std[i+1]= np.std([cell.pollution_level for row in self.cells for cell in row])
         temp_std[i+1]= np.std([cell.temp for row in self.cells for cell in row])
         clouds_std[i+1]= np.std([cell.clouds for row in self.cells for cell in row])
         wind_std[i+1]= np.std([cell.wind.power for row in self.cells for cell in row])
      print("----------------------------------------------------------------")
      print("Wind Avarage:", wind_measures)
      print("Wind STD:", wind_std)
      print("----------------------------------------------------------------")
      print("Pollution Avarage:", pollution_measures)
      print("Pollution STD:", pollution_std)
      print("----------------------------------------------------------------")
      print("Temperature Avarage:", temp_measures)
      print("Temperature STD:", temp_std)
      print("----------------------------------------------------------------")      

      create_plots(normalize(pollution_measures), normalize(temp_measures), normalize(clouds_measures), normalize(wind_measures))
   
   def update_world(self):
        new_cells = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for row in range(self.rows):
           for col in range(self.cols):
              cur_cell = self.cells[row][col]
              new_cells[row][col] = EnvironmentCell(cur_cell.type, self.adjust_temp(row, col), self.adjust_wind(row, col), self.adjust_pollution(row, col), self.adjust_clouds(row, col), self.adjust_rain(row, col))
        self.cells = new_cells
        
   def update_world_and_draw(self):
      self.update_world()
      self.create_grid()

   def adjust_clouds(self, row, col):
      cell = self.cells[row][col]
      clouds = cell.clouds
      if random.random() < clouds_probs[cell.type]:
          clouds+=1
      if cell.wind_power()=="Strong":
         clouds-=2
      elif cell.wind_power()=="Weak":
         clouds-=1

      #neighbors
      if row>0:
         if check_wind(self.cells[row-1][col], "south"):
            clouds+=get_neighbors(self.cells[row-1][col].clouds_power(), self.cells[row-1][col].wind_power()) 

         if col>0 and check_wind(self.cells[row-1][col-1], "south_east"):
            clouds+=get_neighbors(self.cells[row-1][col-1].clouds_power(), self.cells[row-1][col].wind_power()) 

         if col<self.cols-1 and check_wind(self.cells[row-1][col+1], "south_west"):
            clouds+=get_neighbors(self.cells[row-1][col+1].clouds_power(), self.cells[row-1][col+1].wind_power()) 

      #bottom
      if row<self.rows-1:
         if check_wind(self.cells[row+1][col], "north"):
            clouds+=get_neighbors(self.cells[row+1][col].clouds_power(), self.cells[row+1][col].wind_power()) 
         
         if col>0 and check_wind(self.cells[row+1][col-1], "north_east"):
            clouds+=get_neighbors(self.cells[row+1][col-1].clouds_power(), self.cells[row+1][col-1].wind_power()) 

         if col<self.cols-1 and check_wind(self.cells[row+1][col+1], "north_west"):
            clouds+=get_neighbors(self.cells[row+1][col+1].clouds_power(), self.cells[row+1][col+1].wind_power()) 

      if col>0 and check_wind(self.cells[row][col-1], "east"):
         clouds+=get_neighbors(self.cells[row][col-1].clouds_power(), self.cells[row][col-1].wind_power()) 

      if col<self.cols-1 and check_wind(self.cells[row][col+1], "west"):
         clouds+=get_neighbors(self.cells[row][col+1].clouds_power(), self.cells[row][col+1].wind_power())  

      if cell.rain:
         clouds-=1
      return max(min(clouds, MAX_CLOUD), MIN_CLOUD)
   
   def adjust_pollution(self, row, col):
      cell = self.cells[row][col]
      pollution = cell.pollution_level
      if cell.type=="City":
          pollution+=CITY_POLLUTION_PRODUCE
      if cell.wind_power()=="Strong":
         pollution-=0.02
      elif cell.wind_power()=="Weak":
         pollution-=0.01
      #neighbors   
      # top
      if row>0:
         if check_wind(self.cells[row-1][col], "south"):
            pollution+=get_neighbors(self.cells[row-1][col].pollution_power(), self.cells[row-1][col].wind_power()) 

         if col>0 and check_wind(self.cells[row-1][col-1], "south_east"):
            pollution+=get_neighbors(self.cells[row-1][col-1].pollution_power(), self.cells[row-1][col].wind_power()) 

         if col<self.cols-1 and check_wind(self.cells[row-1][col+1], "south_west"):
            pollution+=get_neighbors(self.cells[row-1][col+1].pollution_power(), self.cells[row-1][col+1].wind_power()) 

      #bottom
      if row<self.rows-1:
         if check_wind(self.cells[row+1][col], "north"):
            pollution+=get_neighbors(self.cells[row+1][col].pollution_power(), self.cells[row+1][col].wind_power()) 
         
         if col>0 and check_wind(self.cells[row+1][col-1], "north_east"):
            pollution+=get_neighbors(self.cells[row+1][col-1].pollution_power(), self.cells[row+1][col-1].wind_power()) 

         if col<self.cols-1 and check_wind(self.cells[row+1][col+1], "north_west"):
            pollution+=get_neighbors(self.cells[row+1][col+1].pollution_power(), self.cells[row+1][col+1].wind_power()) 

      if col>0 and check_wind(self.cells[row][col-1], "east"):
         pollution+=get_neighbors(self.cells[row][col-1].pollution_power(), self.cells[row][col-1].wind_power()) 

      if col<self.cols-1 and check_wind(self.cells[row][col+1], "west"):
         pollution+=get_neighbors(self.cells[row][col+1].pollution_power(), self.cells[row][col+1].wind_power())  

      if cell.rain:
         pollution-=0.05
      return min(max(pollution, MIN_POLLUTION_LEVEL), MAX_POLLUTION_LEVEL)         
               
   def adjust_rain(self, row, col):
      cell = self.cells[row][col]
      cell.clouds-=1
      if cell.clouds<=0:
         ans = False
      else: 
        ans = random.random() < rain_probs[cell.clouds_power()]
      cell.clouds+=1
      return ans  
 
   def adjust_temp(self, row, col):
      cell = self.cells[row][col]
      temperature = cell.temp
      match pollution_levels[int(cell.pollution_level)]["level"]:
         case "B":
            temperature+=0.02
         case "C":
            temperature+=0.03
         case "D":
            temperature+=0.04
         case "E":
            temperature+=0.05  
      if cell.wind_power()=="Strong":
         temperature-=0.0002
      elif cell.wind_power()=="None":
         temperature+=0.0002
      if cell.rain:
         temperature-= 0.0002
      return min(max(temperature, MIN_TEMP), MAX_TEMP)
    
   def adjust_wind(self, row, col): 
      cell = self.cells[row][col]
      new_wind_power = cell.wind.power-1 if cell.wind.power>0 else 0
      if "north" in cell.wind.direction:
         new_wind_powerY = -(new_wind_power)
      elif "south" in cell.wind.direction:
         new_wind_powerY = new_wind_power
      else:
         new_wind_powerY = 0
      if "west" in cell.wind.direction:
         new_wind_powerX = -(new_wind_power)
      elif "east" in cell.wind.direction:
         new_wind_powerX = new_wind_power
      else:
         new_wind_powerX = 0   

      # top
      if row>0:
         if check_wind(self.cells[row-1][col], "south"):
            new_wind_powerY+=self.cells[row-1][col].wind.power-1

         if col>0 and check_wind(self.cells[row-1][col-1], "south_east"):
            new_wind_powerX+=self.cells[row-1][col-1].wind.power-1
            new_wind_powerY+=self.cells[row-1][col-1].wind.power-1

         if col<self.cols-1 and check_wind(self.cells[row-1][col+1], "south_west"):
            new_wind_powerX-=self.cells[row-1][col+1].wind.power-1
            new_wind_powerY+=self.cells[row-1][col+1].wind.power-1

      #bottom
      if row<self.rows-1:
         if check_wind(self.cells[row+1][col], "north"):
            new_wind_powerY-=self.cells[row+1][col].wind.power-1

         if col>0 and check_wind(self.cells[row+1][col-1], "north_east"):
            new_wind_powerX+=self.cells[row+1][col-1].wind.power-1
            new_wind_powerY-=self.cells[row+1][col-1].wind.power-1

         if col<self.cols-1 and check_wind(self.cells[row+1][col+1], "north_west"):
            new_wind_powerX-=self.cells[row+1][col+1].wind.power-1
            new_wind_powerY-=self.cells[row+1][col+1].wind.power-1

      if col>0 and check_wind(self.cells[row][col-1], "east"):
         new_wind_powerX+=self.cells[row][col-1].wind.power-1

      if col<self.cols-1 and check_wind(self.cells[row][col+1], "west"):
         new_wind_powerX-=self.cells[row][col+1].wind.power-1

      if new_wind_powerX==0 and new_wind_powerY==0 and random.random() < wind_probs[cell.type]:
         direction = random.random()
         power = int(random.random()*10)
         if direction<0.25:
            new_wind_powerX-=power
         elif direction<0.5:
            new_wind_powerX+=power
         elif direction<0.75:
            new_wind_powerY-=power
         else:
            new_wind_powerY+=power        
               
      direction = ""
      if new_wind_powerY>0:
         if new_wind_powerX>0:
            direction = "south_east"
         elif new_wind_powerX == 0:
            direction = "south"
         else:
            direction = "south_west"
      elif new_wind_powerY==0:
         if new_wind_powerX>0:
            direction = "east"
         elif new_wind_powerX == 0:
            direction = "-"
         else:
            direction = "west"
      else:
         if new_wind_powerX>0:
            direction = "north_east"
         elif new_wind_powerX == 0:
            direction = "north"
         else:
            direction = "north_west"  
      if new_wind_powerX == 0:
         new_wind_power = abs(new_wind_powerY)
      elif new_wind_powerY == 0:
         new_wind_power = abs(new_wind_powerX)
      else:                      
         new_wind_power = min(abs(new_wind_powerX), abs(new_wind_powerY))
      return Wind(max(min(new_wind_power, MAX_WIND_POWER), MIN_WIND_POWER), direction)     

automaton = TheWorld()
automaton.mainloop()



