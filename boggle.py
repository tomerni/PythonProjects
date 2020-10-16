import tkinter as tki
from game import Game
import tkinter.messagebox as msg_box
import boggle_board_randomizer as boggle


class Board:
    def __init__(self, parent, game):

        self.parent = parent
        self.game = game

        # guess care:
        self.guessed_words = []
        self.word = ""
        self.pressed_buttons = []

        # game data
        self.game_time = self.game.time
        self.remaining = self.game_time
        self.board = boggle.randomize_board()
        self._score_val = tki.StringVar()
        self._score_val.set("0")
        self.lock = True

        self.frame = tki.Canvas(self.parent)
        self._init_photos()

    def _init_photos(self):
        """
        Initiates all of the photos on the board
        """
        self.background = tki.PhotoImage(file=r"space.gif")
        self.frame.pack(expand=True, fill="both")
        self.frame.create_image(0, 0, image=self.background, anchor="nw")
        self.headline = tki.PhotoImage(file=r"headline.gif")
        self.frame.create_image(0, 0, image=self.headline, anchor="nw")
        self.start_image = tki.PhotoImage(file="ok1.gif")
        self.start = tki.Button(self.frame,
                                image=self.start_image,
                                command=self._start_game)
        self.start.place(x=300, y=250)

    def _init_graphics(self):
        """
        Initiates all of the graphics
        """
        self.start.destroy()
        # buttons:
        self.button_frame = tki.Frame(self.frame)
        self.buttons = self._create_buttons()
        self.button_frame.place(x=70, y=200)

        # control panel:
        self._init_guess_panel()
        self._init_panel_buttons()
        self._init_score()
        self._init_clock()
        self._init_guesses_box()

    def _init_score(self):
        score = tki.Label(self.frame,
                          font=("Courier", 30),
                          textvariable=self._score_val,
                          bg="#104257",
                          fg="Yellow")
        score.place(x=500, y=120)

    def _init_clock(self):
        self.time_label = tki.Label(self.frame,
                                    text="",
                                    font=("helvetica", 17, "bold"),
                                    fg="lightblue",
                                    bg="#104257")
        self.time_label.place(x=500, y=480)
        self.hourglass = tki.PhotoImage(file="hourglass.gif")
        self.i = 1

        self.frame.create_image(480, 500, image=self.hourglass)

    def _init_guesses_box(self):
        self.guesses_box = tki.Listbox(self.frame,
                                       bg="Black",
                                       fg="White",
                                       relief="groove",
                                       font=("Courier", 15),
                                       width=15,
                                       height=12)
        self.guesses_box.activate(0)
        self.guesses_box.place(x=500, y=170)

    def _init_guess_panel(self):
        # word display
        self.lbl = tki.Label(self.frame,
                             fg="Yellow",
                             font=("Courier", 25, "bold"),
                             text=self.word,
                             bg="#104257")
        self.lbl.place(x=73, y=125)

    def _init_panel_buttons(self):
        self.remove_image = tki.PhotoImage(file="remove.gif")

        self.check_image = tki.PhotoImage(file="check.gif")

        self.reset_button = tki.Button(self.frame,
                                       image=self.remove_image,
                                       bg="Black",
                                       command=self._reset_word)

        self.check_button = tki.Button(self.frame,
                                       bg="Black",
                                       image=self.check_image,
                                       command=self._check)
        self.reset_button.place(x=400, y=120)
        self.check_button.place(x=20, y=120)

    def _create_buttons(self):
        """
        Creates the grid with the buttons
        """
        buttons = []
        for i in range(len(self.board)):
            row = []
            for j in range(len(self.board[0])):
                button = tki.Button(self.button_frame,
                                    text="",
                                    command=lambda x=self.board[i][j],
                                                   y=(i, j): self._press(x, y),
                                    bg="Black",
                                    fg="White",
                                    font=("Courier", 30),
                                    width=3)
                button.grid(row=i, column=j)
                row.append(button)
            buttons.append(row)
        return buttons

    def _color(self, coor):
        """
        Changes the color of the button according to the press
        """
        if self._approve_press(coor):
            return "Green"
        else:
            return "Red"

    def _start_game(self):
        """
        Starts the game when the user clicked on the starting button
        """
        self._init_graphics()
        self.lock = False
        # show the letters
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.buttons[i][j].config(text=self.board[i][j])
        # start the countdown
        self._countdown(self.parent)

    def _countdown(self, parent):
        """
        Starts the countdown
        """
        if self.remaining > 0:
            min = self.remaining // 60
            sec = str(self.remaining % 60)
            if int(sec) < 10:
                sec = str('0' + sec)
            self.time_label.config(text=f"0{str(min)}:{sec}")
            self.remaining = self.remaining - 1
            parent.after(1000, self._countdown, parent)
        else:
            self._times_up()

    def _times_up(self):
        """
        Pop a message to the user and waits for his answer. If the answer is
        yes starts a new game, else destroys the root
        """
        self.time_label.config(text='')
        flag = self._show_message(self.game.get_times_up_msg(), "End game")
        if flag == 'yes':
            self._reset_game()
        else:
            self.parent.destroy()

    def _press(self, letter, coor):
        """
        Checks if the letter that the user clicked is valid and if so updates
        the word variable and changes the color of the button.
        """
        button = self.buttons[coor[0]][coor[1]]
        if self._approve_press(coor):
            self.word += letter
            self.lbl.config(text=self.word.upper())
            button.config(bg="Orange")
            self.pressed_buttons.append(coor)

    def _approve_press(self, coor):
        """
        Checks if the press is valid according to the coordinates give. If the
        press is valid returns True else False
        """
        if self.lock:
            return False
        if coor not in self.pressed_buttons:
            if self.pressed_buttons:
                last = self.pressed_buttons[-1]
                if -1 <= last[0] - coor[0] <= 1 and -1 <= last[1] - coor[1]\
                        <= 1:
                    return True
                return False
            else:
                return True
        return False

    def _check(self):
        """
        Checks if the word that the user chose is correct
        """
        if self.word == '':
            return
        self.word = self.word.upper()  # To avoid Qu
        if self.game.is_correct_word(self.word):
            self.game.calc_score(self.word)
            self.set_score(self.game.get_score())
            self.guessed_words.append(self.word)
            self.guesses_box.insert(self.i, self.word)
            self._reset_word()
            self.i += 1
        else:
            self._reset_word()

    def _show_message(self, msg, title):
        """
        Shows the message when the time has ended and returns the user choice
        """
        return msg_box.askquestion(str(title), str(msg))

    def _reset_word(self):
        self._reset_colors()
        self.pressed_buttons = []
        self.word = ""
        self.lbl.config(text="")

    def _reset_colors(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.buttons[i][j].config(bg="Black")

    def _reset_game(self):
        """
        Resets the game if the user decided to play again
        """
        self.pressed_buttons = []
        self.word = ""
        self.lbl.config(text="")
        self.guessed_words = []
        self._init_guesses_box()
        self.board = boggle.randomize_board()
        self.buttons = self._create_buttons()
        self.game.set_score(0)
        self.game.set_used_words()
        self.remaining = self.game.get_time()
        self.lock = True
        self._score_val.set("0")

    def set_score(self, value):
        self._score_val.set(str(value))


if __name__ == '__main__':
    game = Game()
    root = tki.Tk()
    root.geometry("800x600")
    root.wm_title("Boggle Game")
    Board(root, game)
    root.mainloop()
