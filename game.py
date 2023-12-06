import pprint
import json
from typing import Any
import os.path
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
pp = pprint.PrettyPrinter(indent=4, width=41, compact=True)

# project5_edmonds_adventure_Syed.py
# Aaminah Syed, cs&115, fall 2023
# programming project #7 , 11/15/2023
# Program function: this program is a text-only game where the user inputs statements such as north, south, east, or west
#and will go to the next location that correstponts to that direction. The user may only exit (using x input) once they have been to every
#location, gone inside every building, talked to at least one npc, and has kept a vitality over 10. There are 25 locations total and 12 #buildings.
#NOTE PLEASE READ BEFORE PROCEEDING: This one has both the Tkinter and the JSON. It is not fully done (as in I have more ideas of what to add such as adding to the map) 
#and I might submit it again but the basic functions in this one work and I am pretty happy with it. I wil be submitting this along with the complete JSON with no tkinter.
#
#INTERNSHIP DEMO: This is a fully-functional interactive tour of Edmonds College campus. There are many features including: having vitality and having to 'refill' it, 
# the ability to talk to other characters, and also saving and loading the game so game play is not limited to one time and can be something that the player can come back to
# The Graphical User Interface is made with tkinter and is playable with a variety of button and pop-ups. There are remarks and other statements made in the game
# to make it a more enjoyable exeperience while also getting the player used to what the physical campus is like. The easy reading format of the user interface 
# makes it a simple game that isn't too mentally straining but rather a fun pass time.
# the project is made with object oriented programming in addition to using dictionaries, lists, and many methods to peice together the game, the loading feature is fully 
# implemented using JSON. I will be updating this game more often and features are not limited to the ones I have told but are just some of the basics.
# 
#RESUME PIECE: presented in class
#NEW FEATURES: I added another vitality refill station in the SEA building with energy drinks (fitting the theme of there being a gym).
#
#PERSONA: Mark is an software developer with two years experience who has volunteered to attend local career fairs, 
# primarily to help recruit #for summer internships. He works on an mainly web apps and has an eye for a good challenge.
# A BS CS grad from UW, he spends his free time #looking for strategies to win at games as fast as possible.

SAVED_FILE_NAME = "saved.json" 

WELCOME_MSG = """ ************
A shuttle drops you off in a parking area located in the BOTTOM RIGHT of campus. A sign ahead reads 'Welcome to Edmonds College'.
Type a direction (N,S,E,W) to go in to go to a different location..
to complete (win) this tour game and be able to leave, complete the tasks listed below.

***Tasks***
- Talk to at least one NPC.
^(the NPCs also provide extra hints that may be essential to winning!)
- Keep vitality above 10 at all times (to get out alive).
- Visit all 25 locations.
- Have fun!

There is a secret shortcut command that may also be used to move locations... if you can find it 

"""
HELP_MSG = """ 
BUTTON FUNCTIONS
north - go north               east - go east
south - go south               west - go west
in - go inside a building      out - leave a building
grab - get nutrients (MLT or SEA)
quit - exit the game           talk - talk to an NPC         
up - go upstairs               down - go downstairs
save - save current game       load - load a saved game
exit - done with game, exit    back - back to last location
"""
CLUE_MSG = """. 
Every time you move locations, your vitality will decrease by 10.
"""


P_DESC = "You are standing in a parking lot with cars, motorcycles, and shuttles. Trees and side walks surround the area. It is fall and the sidewalks are colorful with leaves."
C_DESC = "You are standing in an open area with walkways in all directions, in the middle there is a large abstract metal sculpture of two people embracing."
F_DESC = "You are standing in a grass playing field, striped for soccer"
G_DESC = "You have arrived at the golf course and got hit by a golf ball and have lost some extra vitality!"

SNH_DESC = "You are standing in front of a modern brick-sided 3-story building with large windows with a sign in front of it saying 'Snohomish Hall'"
MLT_DESC = "You are standing in front of a 3-story concrete building with a grand entry and stairs outside leading to the second floor with cafe with a sign in front of it saying 'Mountlake Terrace Hall'"
LYN_DESC = "You are standing in front of a tall 3-story building with a library on the second and third floor with a sign in front of it saying 'Lynnwood Hall'"
BRI_DESC = "You are standing in front of a 2-story building with many entrances from outside hallways with a sign in front of it saying 'Brier Hall'"
SQL_DESC = "You are standing in front of a building with a sign in front that says 'Snoqualmie Hall'"
MDL_DESC = "You are standing in front of a building with a sign in front that says 'Meadowdale Hall'"
MIC_DESC = "You are standing in front of a building with a sign in front that says 'Mill Creek Hall'"
ALD_DESC = "You are standing in front of a building with a sign in front that says 'Alderwood Hall'"
SEA_DESC = "You are standing in front of a building with a sign in front that says 'Seaview Hall'"
HZL_DESC = "You are standing in front of a building with a sign in front that says 'Hazel Miller Hall'"
MUK_DESC = "You are standing in front of a building with a sign in front that says 'Mukilteo Hall'"
WWY_DESC = "You are standing in front of a building with a sign in front that says 'Woodway Hall'"



SNH_DESC_F1 = "You enter into an interior courtyard with small tables and vending machines in the corner. Lab rooms open off the courtyard where you see Professor Bill McCoy standing beside a room"
BRI_DESC_F1 = "You enter into a common room with people chatting around you, the second floor is a hallway with many conference rooms"
LYN_DESC_F1 = "you enter the first floor with an entrance to the academic advising in front of you and stairs that lead to the library beside you."
MLT_DESC_F1 = "You enter into a bustling dining area with hallways leading off to classrooms. An espresso bar occupies most of one side of the dining area"
MDL_DESC_F1 = "You enter into Meadowdale Hall"
MUK_DESC_F1 = "You enter into Mukilteo Hall"
ALD_DESC_F1 = "You enter into Alderwood Hall"
SQL_DESC_F1 = "You enter into Snoqualmie Hall"
WWY_DESC_F1 = "You enter into Woodway Hall"
MIC_DESC_F1 = "You enter into Mill Creek Hall"
SEA_DESC_F1 = "You enter into a hall that leads to a basketball court and the gym. there is a vending machine to your left that contains energy drinks"
HZL_DESC_F1 = "You enter into a modern building with classrooms lining the halls and study areas in the center"

SNH_DESC_F2 = "you are on floor two in Snohomish Hall, there is long hallway with many classrooms"
BRI_DESC_F2 = "you are on floor two in Brier Hall, you are in front of a game room and a hallway with many conference rooms"
LYN_DESC_F2 = "you are on floor two in Lynnwood Hall, in front of you are double doors that lead to many different resource rooms"
MLT_DESC_F2 = "you are on floor two in Mountlake Terrace Hall, conference rooms line the hallways"
MDL_DESC_F2 = "you are on floor two in Meadowdale Hall"
MIC_DESC_F2 = "you are on floor two in Mill Creek Hall"
ALD_DESC_F2 = "you are on floor two in ALderwood Hall"
SQL_DESC_F2 = "you are on floor two in Snoqualmie Hall"
WWY_DESC_F2 = "you are on floor two in Woodway Terrace Hall"
MUK_DESC_F2 = "you are on floor two in Mukilteo Terrace Hall"
HZL_DESC_F2 = "you are on floor two in Hazel Miller, you see Cassandra, the MESA director, wave at you"

NPC_BRI = """
! Welcome to campus! I hope you are enjoying your tour! Remember that MLT has coffee for revitalization.
"""

NPC_LYN = """
thank you for seeing me. To leave campus after you have fulfilled all the tasks, you must go east from the starting point!!
"""

NPC_HZL = """
Well hello there! It's great to see you! hope you're enjoying your visit. 
"""

NPC_SNH = """
Hello there, thank you for seeing me. To leave campus after you have fulfilled all the tasks, you must go east from the starting point!!
"""
NOT_IN_BUILDING_ERROR = "That action requires to be in the building and you are not inside a building"

def output_error(msg):
    print("ERROR:", msg)
    game.show_error(msg)

def output_message(msg):
    print(msg)
    game.update_output_label(msg)

class GameStateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Location):
            return obj.name
        elif isinstance(obj,Player):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
    
class GameStateDecoder(json.JSONDecoder):
    def decode_object(self, obj):
        return super().decode_object(obj)

class Player:
    def __init__(self, name, current_location, last_location, inside_building = False, 
                 npc_interacted = False, dead = False, vitality = 100, upstairs = False, 
                 campus_visited_map = {
                    "C1": False, "C2": False, "C3": False, "C4": False,
                    "P1": True, "P2": False, "P3": False, "P4": False, "P5": False,
                    "F1": False, "F2": False, "F3": False, "G1": False,
                    "MLT": False, "SNH": False, "BRI": False, "LYN": False,
                    "ALD": False, "WWY": False, "MDL": False, "MIC": False, 
                    "SQL": False, "SEA": False, "HZL": False, "MUK": False,
                }
    ):
        if(name == ""):
            name = "Anonymous"
        self.name = name
        
        self.inside_building = inside_building
        self.npc_interacted = npc_interacted
        self.dead = dead
        self.vitality = vitality
        self.upstairs = upstairs

        self.current_location = current_location
        self.last_location = last_location
        
        self.campus_visited_map = campus_visited_map

    def check_all_visited(self):
        all_visited = True
        for loc in self.campus_visited_map:
            all_visited = all_visited and self.campus_visited_map[loc]
        return all_visited
    
    def print_visited_map(self):
        pp.pprint(self.campus_visited_map)

    def name(self):
        self.name

    def move(self, cmd):
        next_location = self.current_location.neighbors[cmd]
        if next_location == "":
            output_error("Can't go there")
        elif next_location == campus.P5 and self.current_location != campus.P4:
            self.current_location = campus.G1
            self.last_location = campus.G1
            self.post_move_actions()
        else:
            if self.inside_building == True:
                output_error(NOT_IN_BUILDING_ERROR)
            else:
                self.last_location = self.current_location
                self.current_location = next_location
                self.post_move_actions()

    def post_move_actions(self):
        if type(self.current_location) != Building:
            self.campus_visited_map[self.current_location.name] = True
        self.vitality -= 10
        game.update_vitality(self.vitality)
        game.update_campus_map(self.current_location.name)
        if self.vitality < 10:
            self.dead = True
            output_error("You are dead and your rotting corpse will be on campus forever, you are now roaming the campus as a ghost and may only leave once your vitality is at least 10.")
        output_message(self.current_location.desc)
        game.update_output_label(self.current_location.desc)

    def nav(self, cmd):
        if cmd == "i":
            if self.inside_building == True:
                output_error("you are already inside")
            elif self.current_location.category == "B":
                self.inside_building = True
                player.campus_visited_map[self.current_location.name] = True
                output_message(self.current_location.floor1_desc)
            else:
                output_error("You are not in a location that has a building to go inside")
        elif cmd == "o":
            if self.inside_building == True:
                self.inside_building = False
                output_message(self.current_location.desc)
            else:
                output_error("You are already outside")
        elif cmd == "u":
            if self.inside_building == True:
              output_message(self.current_location.floor2_desc)
              self.upstairs = True 
            else:
                output_error(NOT_IN_BUILDING_ERROR)
        elif cmd == "d":
            if self.inside_building == True and self.current_location.category == "B" and self.upstairs == True:
              output_message(self.current_location.floor1_desc)
              self.upstairs = False
            else:
                output_error("Cannot go down unless inside a building and upstairs already")
        else:
            output_error(NOT_IN_BUILDING_ERROR)

class Location:
    def __init__(self, name, category, descriptions):
        self.name = name
        self.neighbors = {}
        self.category = category
        self.desc = descriptions 
        
class Building(Location):
    def __init__(self, name, category, descriptions, floor1_desc, floor2_desc, npcs):
        super().__init__(name, category, descriptions)
        self.floor1_desc = floor1_desc
        self.floor2_desc = floor2_desc
        self.npcs = npcs

class Campus:
    def __init__(self):
        self.P1 = Location("P1", "P", P_DESC)
        self.P2 = Location("P2", "P", P_DESC)
        self.P3 = Location("P3", "P", P_DESC)
        self.P4 = Location("P4", "P", P_DESC)
        self.P5 = Location("P5", "P", P_DESC)
        self.C1 = Location("C1", "C", C_DESC)
        self.C2 = Location("C2", "C", C_DESC)
        self.C3 = Location("C3", "C", C_DESC)
        self.C4 = Location("C4", "C", C_DESC)
        self.F1 = Location("F1", "F", F_DESC)
        self.F2 = Location("F2", "F", F_DESC)
        self.F3 = Location("F3", "F", F_DESC)
        self.G1 = Location("G1", "G", G_DESC)

        self.BRI = Building("BRI", "B", BRI_DESC, BRI_DESC_F1, BRI_DESC_F2, NPC_BRI)
        self.MLT = Building("MLT", "B", MLT_DESC, MLT_DESC_F1, MLT_DESC_F2, "")
        self.LYN = Building("LYN", "B", LYN_DESC, LYN_DESC_F1, LYN_DESC_F2, NPC_LYN)
        self.SNH = Building("SNH", "B", SNH_DESC, SNH_DESC_F1, SNH_DESC_F2, NPC_SNH)
        self.HZL = Building("HZL", "B", HZL_DESC, HZL_DESC_F1, HZL_DESC_F2, NPC_HZL)
        self.SEA = Building("SEA", "B", SEA_DESC, SEA_DESC_F1, "", "")
        self.SQL = Building("SQL", "B", SQL_DESC, SQL_DESC_F1, SQL_DESC_F2, "")
        self.MDL = Building("MDL", "B", MDL_DESC, MDL_DESC_F1, MDL_DESC_F2, "")
        self.MIC = Building("MIC", "B", MIC_DESC, MIC_DESC_F1, MIC_DESC_F2, "")
        self.WWY = Building("WWY", "B", WWY_DESC, WWY_DESC_F1, WWY_DESC_F2, "")
        self.ALD = Building("ALD", "B", ALD_DESC, ALD_DESC_F1, ALD_DESC_F2, "")
        self.MUK = Building("MUK", "B", MUK_DESC, MUK_DESC_F1, MUK_DESC_F2, "")

    #row 1 (left to right)
        self.C4.neighbors = {"n": "", "s": self.C1, "e": self.F1, "w": ""}
        self.F1.neighbors = {"n": "", "s": self.SEA, "e": self.F2, "w": self.C4}
        self.F2.neighbors = {"n": "", "s": self.HZL, "e": self.F3, "w": self.F1}
        self.F3.neighbors = {"n": "", "s": self.SQL, "e": self.P5, "w": self.F2}
        self.P5.neighbors = {"n": "", "s": self.P4, "e": "", "w": self.F3}
    #row 2
        self.C3.neighbors = {"n": self.C4, "s": self.MIC, "e": self.SEA, "w": ""}
        self.SEA.neighbors = {"n": self.F1, "s": self.MDL, "e": self.HZL, "w": self.C3}
        self.HZL.neighbors = {"n": self.F2, "s": self.MLT, "e": self.SQL, "w": self.SEA}
        self.SQL.neighbors = {"n": self.F3, "s": self.BRI, "e": self.P4, "w": self.HZL}
        self.P4.neighbors = {"n": self.P5, "s": self.P3, "e": "", "w": self.SQL}
    #row 3
        self.MIC.neighbors = {"n": self.C3, "s": self.G1, "e": self.MDL, "w": ""}
        self.MDL.neighbors = {"n": self.SEA, "s": self.WWY, "e": self.MLT, "w": self.MIC}
        self.MLT.neighbors = {"n": self.HZL, "s": self.LYN, "e": self.BRI, "w": self.MDL}
        self.BRI.neighbors = {"n": self.SQL, "s": self.ALD, "e": self.P3, "w": self.MLT}
        self.P3.neighbors = {"n": self.P4, "s": self.P2, "e": "", "w": self.BRI}
    #row 4
        self.G1.neighbors = {"n": self.MIC, "s": self.C2, "e": self.WWY, "w": ""}
        self.WWY.neighbors = {"n": self.MDL, "s": self.C1, "e": self.LYN, "w": self.G1}
        self.LYN.neighbors = {"n": self.MLT, "s": self.MUK, "e": self.ALD, "w": self.WWY}
        self.ALD.neighbors = {"n": self.BRI, "s": self.SNH, "e": self.P2, "w": self.LYN}
        self.P2.neighbors = {"n": self.P3, "s": self.P1, "e": "", "w": self.ALD}
    #row 5 
        self.C2.neighbors = {"n": self.G1, "s": "", "e": self.C1, "w": ""}
        self.C1.neighbors = {"n": self.WWY, "s": "", "e": self.MUK, "w": self.C2}
        self.MUK.neighbors = {"n": self.LYN, "s": "", "e": self.SNH, "w": self.C1}
        self.SNH.neighbors = {"n": self.ALD, "s": "", "e": self.P1, "w": self.MUK}
        self.P1.neighbors = {"n": self.P2, "s": "", "e": "", "w": self.SNH}
    
    def location_by_name(self, location_name_str):
        return getattr(self, location_name_str)

    def map_string(self):
        return f"""
C 4: {player.campus_visited_map["C4"]} | F 1: {player.campus_visited_map["F1"]} | F 2: {player.campus_visited_map["F2"]} | F 3: {player.campus_visited_map["F3"]} | P 5: {player.campus_visited_map["P5"]}
C 3: {player.campus_visited_map["C3"]} | SEA: {player.campus_visited_map["SEA"]} | HZL: {player.campus_visited_map["HZL"]} | SQL: {player.campus_visited_map["SQL"]} | P 4: {player.campus_visited_map["P4"]}
MIC: {player.campus_visited_map["MIC"]} | MDL: {player.campus_visited_map["MDL"]} | MLT: {player.campus_visited_map["MLT"]} | BRI: {player.campus_visited_map["BRI"]} | P 3: {player.campus_visited_map["P3"]}
G  : {player.campus_visited_map["G1"]} | WWY: {player.campus_visited_map["WWY"]} | LYN: {player.campus_visited_map["LYN"]} | ALD: {player.campus_visited_map["ALD"]} | P 2: {player.campus_visited_map["P2"]}
C 2: {player.campus_visited_map["C2"]} | C 1: {player.campus_visited_map["C1"]} | MUK: {player.campus_visited_map["MUK"]} | SNH: {player.campus_visited_map["SNH"]} | P 1: {player.campus_visited_map["P1"]}

"""
    def print_campus_map(self):
        print(f"""
  n
w   e
  s
              
C 4: {player.campus_visited_map["C4"]} | F 1: {player.campus_visited_map["F1"]} | F 2: {player.campus_visited_map["F2"]} | F 3: {player.campus_visited_map["F3"]} | P 5: {player.campus_visited_map["P5"]}
C 3: {player.campus_visited_map["C3"]} | SEA: {player.campus_visited_map["SEA"]} | HZL: {player.campus_visited_map["HZL"]} | SQL: {player.campus_visited_map["SQL"]} | P 4: {player.campus_visited_map["P4"]}
MIC: {player.campus_visited_map["MIC"]} | MDL: {player.campus_visited_map["MDL"]} | MLT: {player.campus_visited_map["MLT"]} | BRI: {player.campus_visited_map["BRI"]} | P 3: {player.campus_visited_map["P3"]}
G  : {player.campus_visited_map["G1"]} | WWY: {player.campus_visited_map["WWY"]} | LYN: {player.campus_visited_map["LYN"]} | ALD: {player.campus_visited_map["ALD"]} | P 2: {player.campus_visited_map["P2"]}
C 2: {player.campus_visited_map["C2"]} | C 1: {player.campus_visited_map["C1"]} | MUK: {player.campus_visited_map["MUK"]} | SNH: {player.campus_visited_map["SNH"]} | P 1: {player.campus_visited_map["P1"]}

""")

class Game:
    def __init__(self, player):
        self.exit_allowed = False
        self.player = player

    def gui_setup(self, window):
        window.title("Edmond College Adventure")
        window.geometry('1080x640')
        self.display_vitality(window, player)
        self.command_center(window)
        self.display_output_label(window, f"Hello {player.name}\n{WELCOME_MSG}")
        self.display_campus_map(window, campus)
        self.display_move_widgets(window)
        self.display_nav_widgets(window)
        self.display_action_widgets(window)
        self.display_game_options(window)
        
        #self.display_commands(window)
        self.window = window
    
   # def display_commands(self, window):
        #output_label_frame = ttk.Frame(master = window, padding=(5, 5))
        #output_label_var = tk.StringVar()
        #output_label = ttk.Label(master = output_label_frame, text=HELP_MSG)

        #output_label_frame.pack(side="left", expand=False, fill="y")
        #output_label.pack(side="top")
        #output_label_var.set(output)
        #self.output_label_var = output_label_var

    def command_center(self, window):
        command_center = ttk.Frame(master = window, padding=5)
        command_label = ttk.Label(master = command_center, text = HELP_MSG, background='thistle', relief='groove')
        command_center.pack(side = "bottom", expand=False, fill=None)
        command_label.pack(side = "left", expand=False, fill=None)
        return command_center


    def display_game_options(self, window):
        style = ttk.Style()
        style.map("C.TButton",
            foreground=[('pressed', 'red'), ('active', 'blue')],
            background=[('pressed', '!disabled', 'black'), ('active', 'white')]
        )
        game_options_frame = ttk.Frame(master = window, padding=(2, 2))
        save_button = ttk.Button(master = game_options_frame, text = "Save", command = self.do_save, style = "C.TButton")
        load_button = ttk.Button(master = game_options_frame, text = "Load", command = self.do_load, style = "C.TButton")
        quit_button = ttk.Button(master = game_options_frame, text = "Quit", command = self.do_quit, style = "C.TButton",)
        
        game_options_frame.pack(side="left", expand=True, fill="x")
        quit_button.pack(side = "right", expand=True, fill="x")
        save_button.pack(side = "bottom", expand=True, fill="y")
        load_button.pack(side = "left", expand=True, fill="y")

        return game_options_frame
    
    def do_save(self):
        with open(SAVED_FILE_NAME, 'w') as file:
            file.write(json.dumps(player, cls=GameStateEncoder))
        game_saved = "Game Saved Successfully"
        output_message(game_saved)

    def do_load(self):
        if os.path.isfile(SAVED_FILE_NAME): 
            with open(SAVED_FILE_NAME, 'r') as file:
                data = file.read()
            decoded_data = json.loads(data, cls=GameStateDecoder)
            player = Player(**decoded_data)
            player.current_location = getattr(campus, player.current_location)
            player.last_location = getattr(campus, player.last_location)
            output_message(player.current_location)
        else: 
            no_saved_game_error = "no previous game was saved"
            output_error(no_saved_game_error)  
        
    def do_quit(self):
        choice = messagebox.askquestion(title= "Quit Confirmation", message="Are you sure you want to quit?")
        if choice == "yes":
            output_message("Bye!")
            exit()
    

    def display_action_widgets(self, window):
        action_widgets_frame = ttk.Frame(master = window)
        back_button = ttk.Button(master = action_widgets_frame, text = "Back", command = self.go_back, padding=(5, 5))
        talk_button = ttk.Button(master = action_widgets_frame, text = "Talk", command = self.do_talk, padding=(5, 5))
        grab_button = ttk.Button(master = action_widgets_frame, text = "Grab", command = self.do_grab, padding=(5, 5))
        exit_button = ttk.Button(master = action_widgets_frame, text = "Exit", command = self.do_exit, padding=(5, 5))
        
        action_widgets_frame.pack(side = "top", expand=False, fill="x")
        talk_button.pack(side = "top", expand=False, fill=None)
        grab_button.pack(side = "top", expand=False, fill=None)
        back_button.pack(side = "top", expand=False, fill=None)
        exit_button.pack(side = "top", expand=False, fill=None)
        return action_widgets_frame

    def do_talk(self):
        if player.current_location.category == 'B' and player.current_location.npcs != "":
            player.npc_interacted = True
            output_message("Hello " + player.name +  player.current_location.npcs)
        else:
            output_error("There is no npc near you")

    
    def do_exit(self):
        #output_error("You cannot exit yet")
        #output_message("Congrats")
        #if all visited, vitality more than 10, npc talked, then allow completion and exit
        if player.check_all_visited() != True:
            output_error("You have not visited all locations yet")
        elif player.vitality < 10:
            output_error("You don't have vitality to leave")
        elif player.dead == True:
            output_error("Dead people don't leave they quit and restart")
        elif player.current_location != campus.P1:
            output_error("You can only leave from P1")
        elif player.npc_interacted != True:
            output_error("You have not interacted with another character in the game")
        else:
            output_message("Congratulations you have successfully completed the game, a shuttle comes to whisk you away. Come visit again soon!")
            exit()

    def do_grab(self):
        if player.current_location == campus.MLT and player.inside_building == True:
            player.vitality = 100
            print("Vitality:", player.vitality)
            game.update_vitality(player.vitality)
            output_message("You have been revitalized, enjoy your coffee!")
        elif player.current_location == campus.SEA and player.inside_building == True:
            player.vitality = 100
            print("Vitality:", player.vitality)
            game.update_vitality(player.vitality)
            output_message("You have been fully revitalized, enjoy your energy drink!")
        else:
            output_error("You do not have access to any revitalization at this moment.")
    
    def nav_up(self):
        player.nav('u')

    def nav_down(self):
        player.nav('d')

    def nav_in(self):
        player.nav('i')

    def nav_out(self):
        player.nav('o')
    
    def display_nav_widgets(self, window):
        nav_widgets_frame = ttk.Frame(master = window, padding=(0, 20))
        nav_up_button = ttk.Button(master = nav_widgets_frame, text = "Up",command = self.nav_up)
        nav_down_button = ttk.Button(master = nav_widgets_frame, text = "Down", command = self.nav_down)
        nav_in_button = ttk.Button(master =  nav_widgets_frame, text = "In", command = self.nav_in)
        nav_out_button = ttk.Button(master =  nav_widgets_frame, text = "Out", command = self.nav_out)
        
        nav_widgets_frame.pack(side = "top", expand=False, fill="x")
        nav_up_button.pack(side = "top")
        nav_down_button.pack(side = "bottom")
        nav_in_button.pack(side = "right")
        nav_out_button.pack(side = "left")
        return nav_widgets_frame 

    def move_north(self):
        player.move('n')

    def move_south(self):
        player.move('s')

    def move_east(self):
        player.move('e')

    def move_west(self):
        player.move('w')

    def go_back(self):
        player.current_location = player.last_location
        player.last_location = player.current_location
        print("Vitality:",player.vitality)
        if player.vitality < 10:
            output_error("You are dead and your rotting corpse will be on campus forever, you may roam the campus as a ghost but will never be able to leave.")
        output_message(player.current_location.desc) 
        player.vitality -= 10

    def display_move_widgets(self, window):
        move_widgets_frame = ttk.Frame(master = window)
        move_north_button = ttk.Button(master = move_widgets_frame, text = "North", command = self.move_north)
        move_south_button = ttk.Button(master = move_widgets_frame, text = "South", command = self.move_south)
        move_east_button = ttk.Button(master = move_widgets_frame, text = "East", command = self.move_east)
        move_west_button = ttk.Button(master = move_widgets_frame, text = "West", command = self.move_west)
        move_widgets_frame.pack(side = "top", expand=False, fill="x")
        move_north_button.pack(side = "top")
        move_south_button.pack(side = "bottom")
        move_east_button.pack(side = "right")
        move_west_button.pack(side = "left")
        return move_widgets_frame

    def display_output_label(self, window, output):
        output_label_frame = ttk.Frame(master = window, padding=(5, 5),border=5, borderwidth=25)
        output_label_var = tk.StringVar()
        output_label = ttk.Label(master = output_label_frame, textvariable = output_label_var, width = 100, wraplength = 550)

        output_label_frame.pack(side="left", expand=False, fill="y")
        output_label.pack(side="top")
        output_label_var.set(output)
        self.output_label_var = output_label_var


    def display_vitality(self, window, player):
        style = ttk.Style()
        style.configure("BW.TLabel", foreground="black", background="white")
        style.configure("RW.TLabel", foreground="red", background="white")
        vitality_frame = ttk.Frame(master = window)
        vitality_number = tk.StringVar()
        vitality_label = ttk.Label(master = vitality_frame, text = "Vitality : ", style = "BW.TLabel")
        vitality_value = ttk.Label(master = vitality_frame, textvariable = vitality_number, style = "RW.TLabel")
        vitality_frame.pack(side = "top", expand = False, fill = "x")
        vitality_label.pack(side="left")
        vitality_value.pack(side="left")
        vitality_number.set(f"{player.vitality}")
        self.vitality_number = vitality_number
    
    def update_vitality(self, vitality):
        self.vitality_number.set(f"{vitality}")
    
    def update_output_label(self, new_label):
        self.output_label_var.set(new_label)

    def show_error(self, error_message):
        error_popup = messagebox.showerror(title="ERROR", message=error_message)

    def update_campus_map(self, current_location_name):

        #self.map_frame.configure(text=f"Current Location: {current_location_name}")
        self.frame_forget_children(self.map_frame)
        self.draw_campus_frame(self.map_frame, campus)
    
    def frame_forget_children(self, frame):
        for child in frame.winfo_children():
            child.pack_forget()

    def draw_campus_frame(self, map_frame, campus):
        row_frame = ttk.Frame(master = map_frame)
        row_frame.pack()
        
        self.row_starting_location = campus.location_by_name("P5")
        remaining_locations = 25
        self.current_location = self.row_starting_location
        
        while remaining_locations > 0:
            cell_background = "white"
            if player.current_location == self.current_location:
                cell_background = "orange"
            elif player.campus_visited_map[self.current_location.name] == True:
                cell_background = "green"
            map_label = ttk.Label(master = row_frame, text = self.current_location.name, 
                                  borderwidth=1, relief = "solid", width = 5, padding = 10, 
                                  background = cell_background)
            map_label.pack(side = "right")
            self.current_location = self.current_location.neighbors['w']
            if self.current_location == "":
                self.current_location = self.row_starting_location.neighbors['s']
                if self.current_location == "":
                    break
                self.row_starting_location = self.current_location
                row_frame = ttk.Frame(master = map_frame)
                row_frame.pack()
            remaining_locations -= 1
        
    def display_campus_map(self, window, campus):
        map_frame = ttk.LabelFrame(master = window, padding = (10, 2), text = "Campus Map: Green = Visited, Orange = Current")  
        map_frame.pack(side="right", expand=False, fill="both")
        self.draw_campus_frame(map_frame, campus)
        self.map_frame = map_frame

    def start(self):
        window = tk.Tk()
        window.resizable(False, False)
        self.gui_setup(window)
        window.mainloop()

       # self.greet()
       # self.input_loop()

    def greet(self):
        print("Hello", self.player.name)
        print(WELCOME_MSG)

    def take_user_input(self):
        PROMPT = "==> "
        user_input = input(PROMPT) + " "
        return user_input.lower()[0]
    
    def input_loop(self):
        while(self.exit_allowed == False):
            user_input = self.take_user_input()
            self.handle_user_input(user_input)

    def handle_user_input(self, user_input):
        global player

        move_commands = ['n', 'e', 'w', 's']
        nav_commands = ['i', 'o', 'u', 'd']

        if user_input in move_commands:
            player.move(user_input)
        elif user_input == 'v':
            self.do_save()
        elif user_input == 'l':
            self.do_load()          
        elif user_input == 'p':
            teleport_location = input("Where do you want to be teleported? ").upper()
            player.current_location = getattr(campus, teleport_location)
            player.post_move_actions()
        elif user_input in nav_commands:
            if player.current_location.category == "B":
                player.nav(user_input)
            else:
                print(NOT_IN_BUILDING_ERROR)
                output_error(NOT_IN_BUILDING_ERROR)
        elif user_input == 'h':
            print(HELP_MSG)
        elif user_input == 'q':
            self.do_quit()
        elif user_input == 'c':
            print(CLUE_MSG)
        elif user_input == 'b':
            self.go_back()
        elif user_input == 'x':
            #if all visited, vitality more than 10, npc talked, then allow completion and exit
            if player.check_all_visited() != True:
                output_message("You have not visited all locations yet")
            elif player.vitality < 10:
                output_message("You don't have vitality to leave")
            elif player.dead == True:
                output_message("Dead people don't leave they quit and restart")
            elif player.current_location != campus.P1:
                output_message("You can only leave from P1")
            elif player.npc_interacted != True:
                output_message("You have not interacted with another character in the game")
            else:
                output_message("Congratulations you have successfully completed the game, a shuttle comes to whisk you away. Come visit again soon!")
                exit()
        elif user_input == 't':
            self.do_talk()
        elif user_input == 'm':
            #player.print_visited_map()
            campus.print_campus_map()
        elif user_input == 'g':
            self.do_grab()
        print("DEBUG: User entered:", user_input, ", and you are now at:", player.current_location.name, "type:", player.current_location.category) #debug statement used to figure out where player is, and what they entered to get there, will not be there in final project



campus = Campus() 
starting_location = campus.P1
#player_name = input("What is your name? ")
player = Player("Player", starting_location, starting_location)
game = Game(player)
game.start()

