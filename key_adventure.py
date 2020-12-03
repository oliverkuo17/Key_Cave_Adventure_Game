import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
from PIL import Image, ImageTk

__author__ = "Yi-Chi (Oliver) Kuo"
__date__ = "30 oct 2020"

TASK_ONE = 1
TASK_TWO = 2
MASTERS = 3

GAME_LEVELS = {
    "game1.txt": 7,
    "game2.txt": 12,
    "game3.txt": 19
    }

PLAYER = "O"
KEY = "K"
DOOR = "D"
WALL = "#"
MOVE_INCREASE = "M"
SPACE = " "

DIRECTIONS = {
    "W": (-1, 0),
    "S": (1, 0),
    "D": (0, 1),
    "A": (0, -1)
    }

def load_game(filename):
    """Create a 2D array of string representing the dungeon to display.

    Parameters:
        filename (str): A string representing the name of the level.

    Returns:
        (list<list<str>>): A 2D array of strings representing the
            dungeon.
    """
    dungeon_map = []
    with open(filename,"r") as file:
        for lines in file:
            line = lines.strip('\n')
            dungeon_map.append(line)
    return dungeon_map

class AbstractGrid(tk.Canvas):
    """An abstract view class which inherits from tk.Canvas."""
    def __init__(self, master, rows, cols, width, height, **kwargs):
        """
        Constrctor of AbstractGrid.

        Parameters:
            master (tk.TK()): An instance of tkinter.TK
            rows (int): the number of rows in the grid
            cols (int): the number of columns in the grid
            width (int): the number of pixels for the width of the grid
            height (int): the number of pixels for the height of the grid
            **kwargs: Optional arguments
        """
        super().__init__(master, **kwargs)
        self._master = master
        self._rows = rows
        self._cols = cols
        self._width = width
        self._height = height
        self.config(width=width, height=height)
        self._cell_width = self._width//self._cols
        self._cell_height = self._height//self._rows

    def get_bbox(self, position):
        """Returns the bounding box for the (row, col) position."""
        row, col = position
        x0 = col * self._cell_width
        y0 = row * self._cell_height
        x1 = x0 + self._cell_width
        y1 = y0 + self._cell_height
        bbox = (x0,y0,x1,y1)
        return bbox

    def pixel_to_position(self,pixel):
        """
        Converts the x, y pixel position to a (row, col) position.

        Parameters:
            pixel(tuple<int, int>): pixel position

        Returns:
            position(tuple<int, int>): Returns a (row, col) position
        """
        x, y = pixel
        position = (y//self._cell_height, x//self._cell_width)
        return position

    def get_position_center(self, position):
        """
        Gets the graphics coordinates for the center of the cell
        at the given (row, col) position.

        Parameters:
            position(tuple<int, int>): (row, col) position

        Returns:
            position_center(tuple<int, int>): Returns a pixel position
            for the center of the cell
        """
        x0, y0, x1, y1 = self.get_bbox(position)
        position_center = ((x0 + x1)/2, (y0 + y1)/2)
        return position_center

    def annotate_position(self, position, text):
        """Annotates the cell at the given (row, col) position with the provided text."""
        self.create_text(self.get_position_center(position),text=text)

class DungeonMap(AbstractGrid):
    """Display of the dungeon"""
    def __init__(self, master, size, width, **kwargs):
        """
        Construct a view of the dungeon.

        Parameters:
            master (tk.TK()): An instance of tkinter.TK
            size (int): the number of rows and columns in the grid
            width (int): the number of pixels for the width
                and height of the grid
            **kwargs: Optional arguments
        """
        super().__init__(master, size, size, width, width, **kwargs)
        self._size = size

    def draw_grid(self, game_information, player_pos):
        """
        Displays the dungeon.

        parameter:
            game_information (dict<tuple<int, int>: Entity): Dictionary
                containing the position and the corresponding Entity
            player_pos (tuple<int, int>): The position of the Player
        """
        # Stores game_information in string and converts it into a list
        dungeon_grid = ""
        for i in range(self._size):
            rows = ""
            for j in range(self._size):
                position = (i, j)
                entity = game_information.get(position)

                if entity is not None:
                    char = entity.get_id()
                elif position == player_pos:
                    char = PLAYER
                else:
                    char = SPACE
                rows += char
            if i < self._size - 1:
                rows += '\n'
            dungeon_grid += rows
        dungeon_grid = dungeon_grid.split('\n')


        objects = {
            WALL:('Dark grey', None),
            KEY:('Yellow','Trash'),
            PLAYER:('Medium spring green', 'Ibis'),
            MOVE_INCREASE:('Orange', 'Banana'),
            DOOR:('Red', 'Nest')
            }

        # draw dungeon
        for rows in range(self._size):
            for cols in range(self._size):
                position = (rows,cols)
                grid = dungeon_grid[rows][cols]
                if grid in objects:
                    color, text = objects[grid][0], objects[grid][1]
                    self.create_rectangle(self.get_bbox(position),fill=color,outline='black')
                    self.annotate_position(position, text)

class AdvancedDungeonMap(AbstractGrid):
    """Display of the advanced dungeon"""
    def __init__(self, master, size, width, **kwargs):
        """
        Construct a view of the advanced dungeon.

        Parameters:
            master (tk.TK()): An instance of tkinter.TK
            size (int): The number of rows and columns in the grid
            width (int): The number of pixels for the width
                and height of the grid
            **kwargs: Optional arguments.
        """
        super().__init__(master, size, size, width, width, **kwargs)
        self._size = size
        self._cell_size = self._width//self._size

    def draw_grid(self, game_information, player_pos):
        """
        Displays the advanced dungeon.

        parameter:
            game_information (dict<tuple<int, int>: Entity): Dictionary
                containing the position and the corresponding Entity
            player_pos (tuple<int, int>): The position of the Player
        """
        dungeon_grid = ""
        for i in range(self._size):
            rows = ""
            for j in range(self._size):
                position = (i, j)
                entity = game_information.get(position)

                if entity is not None:
                    char = entity.get_id()
                elif position == player_pos:
                    char = PLAYER
                else:
                    char = SPACE
                rows += char
            if i < self._size - 1:
                rows += '\n'
            dungeon_grid += rows
        dungeon_grid = dungeon_grid.split('\n')

        # adds images and keeps references for later use
        image = Image.open('door.gif')
        image = image.resize((self._cell_size,self._cell_size))
        self._master.door_img = door_img = ImageTk.PhotoImage(image)

        image = Image.open('wall.gif')
        image = image.resize((self._cell_size,self._cell_size))
        self._master.wall_img = wall_img = ImageTk.PhotoImage(image)

        image = Image.open('player.gif')
        image = image.resize((self._cell_size,self._cell_size))
        self._master.player_img = player_img = ImageTk.PhotoImage(image)

        image = Image.open('key.gif')
        image = image.resize((self._cell_size,self._cell_size))
        self._master.key_img = key_img = ImageTk.PhotoImage(image)

        image = Image.open('moveIncrease.gif')
        image = image.resize((self._cell_size,self._cell_size))
        self._master.move_increase_img = move_increase_img = ImageTk.PhotoImage(image)

        image = Image.open('empty.gif')
        image = image.resize((self._cell_size,self._cell_size))
        self._master.empty_img = empty_img = ImageTk.PhotoImage(image)

        image_dict = {
            DOOR:door_img,
            WALL:wall_img,
            PLAYER:player_img,
            KEY:key_img,
            MOVE_INCREASE:move_increase_img,
            SPACE:empty_img
            }

        # draw advanced dungeon
        for rows in range(self._size):
            for cols in range(self._size):
                pixel_position = (cols*self._cell_width, rows*self._cell_width)
                cell = dungeon_grid[rows][cols]
                self.create_image(pixel_position, image=empty_img, anchor=tk.NW)
                if cell in image_dict:
                    self.create_image(pixel_position, image=image_dict[cell], anchor=tk.NW)

class KeyPad(AbstractGrid):
    """Display of the keypad"""
    def __init__(self, master, width, height, **kwargs):
        """
        Construct a view of the advanced dungeon.

        Parameters:
            master (tk.TK()): An instance of tkinter.TK
            width (int): The number of pixels for the width of the keypad
            height (int): The number of pixels for the height of the keypad
            **kwargs: Optional arguments.
        """
        super().__init__(master, 2, 3, width, height, **kwargs)

    def pixel_to_direction(self, pixel):
        """
        Converts the x, y pixel position to the direction of the arrow
        depicted at that position.

        Parameters:
            pixel(tuple<int, int>): pixel position

        Returns:
            keypad_direction(str): Returns keypad direction
        """
        position = self.pixel_to_position(pixel)
        keypad_direction = {(0,1):'W',(1,0):'A',(1,1):'S',(1,2):'D'}
        if position in keypad_direction:
            return keypad_direction[position]

    def draw_pad(self):
        """Displays the keypad."""
        keypad_position={'N':(0,1),'W':(1,0),'S':(1,1),'E':(1,2)}
        for direction, position in keypad_position.items():
            self.create_rectangle(self.get_bbox(position),fill='Dark grey')
            self.annotate_position(position, direction)

class StatusBar(tk.Frame):
    """Display of the status bar."""
    def __init__(self, master, move_count, **kwargs):
        """
        Construct a view of the status bar.

        Parameters:
            master (tk.TK()): An instance of tkinter.TK
            move_count (int): The moves remaining of the player
            **kwargs: Optional arguments.
        """
        super().__init__(master, **kwargs)
        self._master = master

        # Buttons
        self._frame1 = tk.Frame(self)
        self._frame1.pack(side=tk.LEFT, padx=40)

        self.new_game_button = tk.Button(self._frame1, text='New Game')
        self.new_game_button.pack(side=tk.TOP, pady=5)

        self.quit_game_button = tk.Button(self._frame1, text='Quit')
        self.quit_game_button.pack(side=tk.TOP)

        # Timer status
        self._frame2 = tk.Frame(self)
        self._frame2.pack(side=tk.LEFT)

        clock = Image.open("clock.gif")
        clock = clock.resize((40,60))
        clock_img = ImageTk.PhotoImage(clock)

        clock_display = tk.Label(self._frame2, image=clock_img)
        clock_display.image = clock_img
        clock_display.pack(side=tk.LEFT)

        timer_text = tk.Label(self._frame2,text='Time elapsed',font='None 10 bold')
        timer_text.pack(side=tk.TOP,pady=5)

        self._time_elapsed = tk.Label(self._frame2)
        self._time_elapsed.pack(side=tk.TOP)

        # MoveCount status
        self._frame3 = tk.Frame(self)
        self._frame3.pack(side=tk.LEFT,padx=60) ##

        lightning = Image.open("lightning.gif")
        lightning = lightning.resize((40,60))
        lightning_img = ImageTk.PhotoImage(lightning)

        lightning_display = tk.Label(self._frame3, image=lightning_img)
        lightning_display.image = lightning_img
        lightning_display.pack(side=tk.LEFT)

        moves_text = tk.Label(self._frame3,text='Moves left',font='None 10 bold')
        moves_text.pack(side=tk.TOP,pady=5)

        self._moves_left = tk.Label(self._frame3, text=f'{move_count} moves remaining')
        self._moves_left.pack(side=tk.TOP)


class AdvancedStatusBar(StatusBar):
    """Display of the advanced status bar."""
    def __init__(self, master, move_count, lives, **kwargs):
        """
        Construct a view of the advanced status bar.

        Parameters:
            master (tk.TK()): An instance of tkinter.TK
            move_count (int): The moves remaining of the player
            lives(int): initial number of lives
            **kwargs: Optional arguments.
        """
        super().__init__(master, move_count,**kwargs)

        # Lives status
        self._frame4 = tk.Frame(self)
        self._frame4.pack(side=tk.LEFT)

        lives = Image.open("lives.gif")
        lives = lives.resize((50,50))
        lives_img = ImageTk.PhotoImage(lives)

        lives_display = tk.Label(self._frame4, image=lives_img)
        lives_display.image = lives_img
        lives_display.pack(side=tk.LEFT)

        self._lives_text = tk.Label(self._frame4,text=f'Lives remaining: {lives}',font='None 10 bold')
        self._lives_text.pack(side=tk.TOP,pady=5)

        self.use_life_button = tk.Button(self._frame4, text="Use life")
        self.use_life_button.pack(side=tk.TOP)

class Entity:
    """ """

    _id = "Entity"

    def __init__(self):
        """
        Something the player can interact with
        """
        self._collidable = True

    def get_id(self):
        """ """
        return self._id

    def set_collide(self, collidable):
        """ """
        self._collidable = collidable

    def can_collide(self):
        """ """
        return self._collidable

    def __str__(self):
        return f"{self.__class__.__name__}({self._id!r})"

    def __repr__(self):
        return str(self)


class Wall(Entity):
    """ """

    _id = WALL

    def __init__(self):
        """ """
        super().__init__()
        self.set_collide(False)


class Item(Entity):
    """ """
    def on_hit(self, game):
        """ """
        raise NotImplementedError


class Key(Item):
    """ """

    _id = KEY

    def on_hit(self, game):
        """ """
        player = game.get_player()
        player.add_item(self)
        game.get_game_information().pop(player.get_position())


class MoveIncrease(Item):
    """ """

    _id = MOVE_INCREASE

    def __init__(self, moves=5):
        """ """
        super().__init__()
        self._moves = moves

    def on_hit(self, game):
        """ """
        player = game.get_player()
        player.change_move_count(self._moves)
        game.get_game_information().pop(player.get_position())


class Door(Entity):
    """ """
    _id = DOOR

    def on_hit(self, game):
        """ """
        player = game.get_player()
        for item in player.get_inventory():
            if item.get_id() == KEY:
                game.get_game_information().pop(player.get_position())
                game.set_win(True)
                return

class Player(Entity):
    """ """

    _id = PLAYER

    def __init__(self, move_count):
        """ """
        super().__init__()
        self._move_count = move_count
        self._inventory = []
        self._position = None

    def set_position(self, position):
        """ """
        self._position = position

    def get_position(self):
        """ """
        return self._position

    def change_move_count(self, number):
        """
        Parameters:
            number (int): number to be added to move count
        """
        self._move_count += number

    def moves_remaining(self):
        """ """
        return self._move_count

    def add_item(self, item):
        """Adds item (Item) to inventory
        """
        self._inventory.append(item)

    def get_inventory(self):
        """ """
        return self._inventory

class GameLogic:
    """ """
    def __init__(self, dungeon_name):
        """ """
        self._dungeon = load_game(dungeon_name)
        self._dungeon_size = len(self._dungeon)
        self._player = Player(GAME_LEVELS[dungeon_name])
        self._game_information = self.init_game_information()
        self._win = False

    def get_positions(self, entity):
        """ """
        positions = []
        for row, line in enumerate(self._dungeon):
            for col, char in enumerate(line):
                if char == entity:
                    positions.append((row, col))

        return positions

    def init_game_information(self):
        """ """
        player_pos = self.get_positions(PLAYER)[0]
        key_position = self.get_positions(KEY)[0]
        door_position = self.get_positions(DOOR)[0]
        wall_positions = self.get_positions(WALL)
        move_increase_positions = self.get_positions(MOVE_INCREASE)

        self._player.set_position(player_pos)

        information = {
            key_position: Key(),
            door_position: Door(),
        }

        for wall in wall_positions:
            information[wall] = Wall()

        for move_increase in move_increase_positions:
            information[move_increase] = MoveIncrease()

        return information

    def get_player(self):
        """ """
        return self._player

    def get_entity(self, position):
        """ """
        return self._game_information.get(position)

    def get_entity_in_direction(self, direction):
        """ """
        new_position = self.new_position(direction)
        return self.get_entity(new_position)

    def get_game_information(self):
        """ """
        return self._game_information

    def get_dungeon_size(self):
        """ """
        return self._dungeon_size

    def move_player(self, direction):
        """ """
        new_pos = self.new_position(direction)
        self.get_player().set_position(new_pos)

    def collision_check(self, direction):
        """
        Check to see if a player can travel in a given direction
        Parameters:
            direction (str): a direction for the player to travel in.

        Returns:
            (bool): False if the player can travel in that direction without colliding otherwise True.
        """
        new_pos = self.new_position(direction)
        entity = self.get_entity(new_pos)
        if entity is not None and not entity.can_collide():
            return True

        return not (0 <= new_pos[0] < self._dungeon_size and 0 <= new_pos[1] < self._dungeon_size)

    def new_position(self, direction):
        """ """
        x, y = self.get_player().get_position()
        dx, dy = DIRECTIONS[direction]
        return x + dx, y + dy

    def check_game_over(self):
        """ """
        return self.get_player().moves_remaining() <= 0

    def set_win(self, win):
        """ """
        self._win = win

    def won(self):
        """ """
        return self._win

class GameApp:
    """Communicator between the GameLogic and the View classes."""
    def __init__(self,master,task=TASK_ONE,dungeon_name="game2.txt"):
        """
        Constructor of the GameApp class.

        Parameters:
            master (tk.TK()): An instance of tkinter.TK
            task (constant): Constant used to decide the features of the game
            dungeon_name(str): The name of the file to load the level from
        """
        self._dungeon_name = dungeon_name
        self._game = GameLogic(dungeon_name)
        self._size = self._game.get_dungeon_size()
        self._master = master
        self._master.title("Key Cave Adventure Game")
        self._master.geometry("850x720")
        self._label = tk.Label(self._master, text="Key Cave Adventure Game",
                               bg='Medium spring green', font='None 16 bold')
        self._label.pack(side=tk.TOP,fill=tk.BOTH,ipady=10)
        self._moves = self._game.get_player().moves_remaining()
        self._task = task
        self._time_count = 0
        self._lives = 3

        # display dungeon based on task
        if self._task == TASK_ONE:
            self._display = DungeonMap(self._master, self._size,
                                       width=600, bg='light gray')
        else:
            self._display = AdvancedDungeonMap(self._master, self._size,
                                               width=600, bg='light gray')
            menubar = tk.Menu(self._master)
            self._master.config(menu=menubar)
            filemenu = tk.Menu(menubar)
            menubar.add_cascade(label="File", menu=filemenu)
            filemenu.add_command(label="Save game",command=self.save_file)
            filemenu.add_command(label="Load game",command=self.open_file)
            filemenu.add_command(label="New game", command=self.restart)
            filemenu.add_command(label="Quit", command=self.quit)
        if self._task == MASTERS:
            filemenu.add_command(label="High scores",command=self.high_scores_popup)

        self._display.pack(side=tk.TOP,anchor=tk.NW)
        self._display.bind_all("<Key>", self.key_press)
        self._keypad = KeyPad(self._master, width=200, height=100)
        self._keypad.place(x=610,y=350)
        self._keypad.bind("<Button-1>", self.pad_press)

        # display status bar based on task
        if self._task == TASK_TWO:
            self._status_bar = StatusBar(self._master, self._moves)

        elif self._task == MASTERS:
            self._status_bar = AdvancedStatusBar(self._master, self._moves, self._lives)
            self._status_bar._lives_text.config(text=f'Lives remaining: {self._lives}')
            self._status_bar.use_life_button.config(command=self.use_life)

        if self._task == TASK_TWO or self._task == MASTERS:
            self._status_bar.pack(side=tk.TOP,anchor=tk.W)
            self._status_bar.new_game_button.config(command=self.restart)
            self._status_bar.quit_game_button.config(command=self.quit)
            self._status_bar._moves_left.config(text=f'{self._moves} moves remaining')
            self.timer()

        # lists used to record in-game information
        self._last_position = []
        self._last_time = []
        self._last_key_state = []
        self._last_move_increase_state = []

        self._action = None
        self.draw()

    def timer(self):
        """
        Displaying the number of minutes and seconds the user
        has been playing the current game
        """
        second = self._time_count % 60
        minute = self._time_count // 60
        self._status_bar._time_elapsed.config(text=f'{minute}m {second}s')
        self._time_count += 1
        self._master.after(1000, self.timer)

    def use_life(self):
        """Undo the most recent move"""
        move_count = self._game.get_player().moves_remaining()
        initaial_moves = GAME_LEVELS[self._dungeon_name]
        if self._lives > 0 and move_count < initaial_moves:
            self._game._game_information = self._game.init_game_information()
            self._display.delete("all")
            self._lives -= 1
            self._game.get_player().change_move_count(1)
            self._game.get_player().set_position(self._last_position[-1])

            # last_key_state[i] == 0 means that the key is in the dungeon
            # last_key_state[i] == 1, otherwise.
            if self._last_key_state[-1] == 1 and self._last_key_state[-2] == 1:
                key_position = self._game.get_positions(KEY)[0]
                item = self._game.get_entity(key_position)
                self._game._player.add_item(item)
                del self._game._game_information[key_position]
            else:
                self._game.get_player()._inventory.clear()
            # last_move_increase_state[i] == 0 means that the move_increaseis in the dungeon
            # last_move_increase_state[i] == 1, otherwise.
            if self._last_move_increase_state[-1] == 1 and self._last_move_increase_state[-2] == 1:
                move_increase_position = self._game.get_positions(MOVE_INCREASE)[0]
                del self._game._game_information[move_increase_position]
            if self._last_move_increase_state[-1] == 1 and self._last_move_increase_state[-2] == 0:
                self._game.get_player().change_move_count(-5)

            self._status_bar._lives_text.config(text=f'Lives remaining: {self._lives}')
            self._status_bar._moves_left.config(text=f'{self._game.get_player().moves_remaining()} moves remaining')
            # update the in-game information lists
            self._last_key_state = self._last_key_state[:-1:]
            self._last_move_increase_state = self._last_move_increase_state[:-1:]
            self._time_count = self._last_time[-1]
            self._last_time = self._last_time[:-1:]
            self._last_position = self._last_position[:-1:]

            self.draw()

    def play(self):
        """Handles the player interaction."""
        player = self._game.get_player()
        direction = self._action
        if direction in DIRECTIONS:
            player.change_move_count(-1)

            if not self._game.collision_check(direction):
                self._last_position.append(player.get_position())
                self._game.move_player(direction)

                entity = self._game.get_entity(player.get_position())
                if entity is not None:
                    entity.on_hit(self._game)

            if self._task == TASK_TWO or self._task == MASTERS:
                # record in-game information for saving/undo
                # if entity in the dungeon, append(0), otherwise, append(1)
                self._last_time.append(self._time_count)
                if self._game.get_positions(MOVE_INCREASE)[0] in self._game.get_game_information():
                    self._last_move_increase_state.append(0)
                else:
                    self._last_move_increase_state.append(1)
                if self._game.get_positions(KEY)[0] in self._game.get_game_information():
                    self._last_key_state.append(0)
                else:
                    self._last_key_state.append(1)
                self._status_bar._moves_left.config(text=f'{player._move_count} moves remaining')

            self.draw()

            if self._game.won():
                self.endgame_won()

            if self._game.check_game_over():
                self.endgame_lost()

    def draw(self):
        """Displays the dungeon and the keypad."""
        self._display.delete("all")
        game_information = self._game.get_game_information()
        player = self._game.get_player()
        player_pos = player.get_position()
        self._display.draw_grid(game_information, player_pos)
        self._keypad.draw_pad()

    def endgame_won(self):
        """Handle the end of game if player won."""
        if self._task == TASK_ONE:
            self._master.update_idletasks()
            tk.messagebox.showinfo("You won!", "You have finished the level!")

        elif self._task == TASK_TWO:
            self._master.update_idletasks()
            if tk.messagebox.askyesno("You won!",
            f"You have finished the level with a score of {self._time_count}.\n\nWould you like to play again?"):
                self.restart()

        elif self._task == MASTERS:
            score = self._time_count
            minute = score // 60
            second = score % 60
            player_name = tk.simpledialog.askstring("You won!",
            f"You won in {minute}m and {second}s! Enter your name:")
            top3 = []

            # read/create high scores file
            try:
                with open("high_scores.txt", "r") as fd:
                    for i in fd.readlines():
                        record = i.split(",")
                        top3.append((str(record[0]), int(record[1])))
            except:
                open("high_scores.txt", 'w+').close()

            # update top3 list if needed
            top3.append((player_name, score))
            top3 = sorted(top3, key=lambda x: x[1])[:3:]
            # update high scores file
            open("high_scores.txt", 'w+').close()
            with open("high_scores.txt", 'a') as fd:
                for i in range(len(top3)):
                    fd.write(f"{top3[i][0]},{top3[i][1]}\n")

    def endgame_lost(self):
        """Handle the end of game if player lost."""
        if self._task == TASK_ONE:
            tk.messagebox.showinfo("You lost!", "You have lost the game!")

        else:
            if tk.messagebox.askyesno("You lost", "Would you like to play again?"):
                self.restart()

    def key_press(self, e):
        """Reaction when the keyboard key is pressed."""
        self._action = e.char
        self.play()

    def pad_press(self, e):
        """Reaction when the keypad key is pressed."""
        self._action = self._keypad.pixel_to_direction((e.x, e.y))
        self.play()

    def restart(self):
        """Reset the game to the initial."""
        self._time_count = 0
        self._display.delete("all")
        self._game = GameLogic(self._dungeon_name)
        self._status_bar._moves_left.config(text=f'{self._game.get_player()._move_count} moves remaining')
        if self._task == MASTERS:
            self._lives = 3
            self._status_bar._lives_text.config(text=f'Lives remaining: {self._lives}')
        self.draw()

    def quit(self):
        """Destroy the window."""
        if tk.messagebox.askyesno("Quit?","Are you sure you would like to quit?"):
            self._master.destroy()

    def save_file(self):
        """Saves all the information needed into a file."""
        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        # 0 means that entity is still in the dungeon, otherwise, 1.
        if self._game.get_positions(MOVE_INCREASE)[0] in self._game.get_game_information():
            MoveIncrease_status = 0
        else:
            MoveIncrease_status = 1
        if self._game.get_positions(KEY)[0] in self._game.get_game_information():
            Key_status = 0
        else:
            Key_status = 1

        player = self._game.get_player()
        player_x, player_y = player.get_position()
        move_count = player.moves_remaining()

        save_information = [
            self._task,
            player_x,
            player_y,
            MoveIncrease_status,
            Key_status,
            self._time_count,
            move_count
            ]

        if self._task == MASTERS:
            lives = self._lives
            save_information.append(lives)

        fd = open(filename, 'w')
        for value in save_information:
            fd.write(f"{value}\n")
        fd.close()

    def open_file(self):
        """Load saved game."""
        try:
            filename = filedialog.askopenfilename()
            fd = open(filename, 'r')
            saved_info = fd.read().splitlines()
            saved_info = [int(i) for i in saved_info]
            player_position = (saved_info[1], saved_info[2])
            move_count = saved_info[6]
            self.restart()
            self._task = saved_info[0]
            self._time_count = saved_info[5]
            self._game.get_player().set_position(player_position)
            self._game.get_player()._move_count = move_count
            self._status_bar._moves_left.config(text=f'{move_count} moves remaining')
            # check move_increase state, 1 means the entity is not in the dungeon
            if saved_info[3] == 1:
                move_increase_position = self._game.get_positions(MOVE_INCREASE)[0]
                del self._game._game_information[move_increase_position]
            # check key state, 1 means the entity is not in the dungeon
            if saved_info[4] == 1:
                key_position = self._game.get_positions(KEY)[0]
                item = self._game.get_entity(key_position)
                self._game._player.add_item(item)
                del self._game._game_information[key_position]

            if self._task == MASTERS:
                self._lives = saved_info[7]
                self._status_bar._lives_text.config(text=f'Lives remaining: {self._lives}')
            self.draw()
        except:
            tk.messagebox.showwarning("Warning!", "This is not a valid file")

    def high_scores_popup(self):
        """Displays the leaderboard"""
        popup = tk.Toplevel(self._master)
        popup.title("Top 3")
        label = tk.Label(popup, text="High Scores",bg='Medium spring green', font='None 16 bold' )
        label.pack(side=tk.TOP,fill=tk.BOTH, ipady=5)

        top3 = []
        with open("high_scores.txt", "r") as fd:
            for i in fd.readlines():
                tmp = i.split(",")
                top3.append((str(tmp[0]), int(tmp[1])))
        try:
            first_place = tk.Label(popup,text=f"{top3[0][0]}: {top3[0][1]}s")
            first_place.pack()
            second_place = tk.Label(popup,text=f"{top3[1][0]}: {top3[1][1]}s")
            second_place.pack()
            third_place = tk.Label(popup,text=f"{top3[2][0]}: {top3[2][1]}s")
            third_place.pack()
        except:
            pass
        done_button = tk.Button(popup, text='Done', command=popup.destroy)
        done_button.pack()

def main():
    root = tk.Tk()
    app = GameApp(root,task=TASK_ONE,dungeon_name="game2.txt")
    root.mainloop()

if __name__ == "__main__":
    main()
