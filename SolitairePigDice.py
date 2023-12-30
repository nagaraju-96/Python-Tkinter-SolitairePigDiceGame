# Learning Resources:
# - Wikipedia (game rules):https://en.wikipedia.org/wiki/Pig_(dice_game)
# - Python Official Documentation: https://docs.python.org/3/library/tkinter.html
# - Real Python Tkinter Tutorial: https://realpython.com/python-gui-tkinter/
# - Python GUI Programming with Tkinter on GeeksforGeeks: https://www.geeksforgeeks.org/python-gui-tkinter/
# - Stack Overflow Community: https://stackoverflow.com/questions/tagged/tkinter

# Import necessary libraries
import tkinter as tk
from tkinter import ttk, messagebox
import random

# Class representing the game logic of Two-Player Pig Dice
class PigDiceGame:
    def __init__(self, num_players):
        # Initialize players with their scores, current rolls, and round scores
        self.players = {i + 1: {"score": 0, "current_roll": 0, "round_scores": []} for i in range(num_players)}
        # Set the initial current player or None if no players
        self.current_player = 1 if self.players else None
        # Initialize round_winner to None
        self.round_winner = None

    def switch_player(self):
        # Switch to the next player in a circular manner
        num_players = len(self.players)
        self.current_player = (self.current_player % num_players) + 1

    def roll(self):
        # Generate a random dice roll
        roll = random.randint(1, 6)
        player_data = self.players[self.current_player]
        # Update current_roll with the dice roll
        player_data["current_roll"] = roll
        if roll == 1:
            # If the roll is 1, reset round_scores and switch to the next player
            player_data["round_scores"].append(0)
            player_data["round_scores"].clear()
            # Show a pop-up message when a player gets 1
            messagebox.showinfo("Bad Luck!", f"Player {self.current_player} got 1 Point, score is 0 for this round.")
            self.switch_player()
        else:
            # Add the non-1 roll to round_scores
            player_data["round_scores"].append(roll)

    def hold(self):
        player_data = self.players[self.current_player]
        # Add the sum of round_scores to the player's score
        player_data["score"] += sum(player_data["round_scores"])
        player_data["round_scores"] = []
        if player_data["score"] >= 100:
            # Check if the player's score is greater than or equal to 100 for a potential win
            if self.round_winner is None:
                self.round_winner = self.current_player
            else:
                # If round_winner already set, check and set the winner using get_round_winner()
                self.round_winner = self.get_round_winner()
                if self.round_winner is not None:
                    return True  # Game over
            # Switch to the next player after updating scores
            self.switch_player()
        else:
            # Switch to the next player if no winner
            self.switch_player()
        return False

    def get_round_winner(self):
        # Determine the winner of the round based on the highest score
        scores = [player_data["score"] for player_data in self.players.values()]
        max_score = max(scores)
        if scores.count(max_score) == 1:
            return scores.index(max_score) + 1
        else:
            return None

    def reset_game(self):
        # Reset the game state, including scores, current player, and round winner
        num_players = len(self.players)
        self.players = {i + 1: {"score": 0, "current_roll": 0, "round_scores": []} for i in range(num_players)}
        self.current_player = 1
        self.round_winner = None

# Class representing the GUI for Two-Player Pig Dice
class PigDiceGUI:
    def __init__(self, master):
        self.master = master
        # Set window title and size
        self.master.title("Two-Player Pig Dice")
        self.master.geometry("900x600")

        self.num_players = 2
        self.game = None

        # Create and pack widgets
        self.welcome_label = tk.Label(master, text="Welcome to Two-Player Pig Dice Game", font=("Helvetica", 16), pady=80)
        self.welcome_label.pack(pady=20)

        self.current_player_label = tk.Label(master, text="", font=("Helvetica", 14))
        self.current_player_label.pack()

        self.choose_players_button = tk.Button(master, text="Start Game", command=self.start_game, font=("Helvetica", 12))
        self.choose_players_button.pack()

        self.roll_button = tk.Button(master, text="Roll", command=self.roll, font=("Helvetica", 12))
        self.hold_button = tk.Button(master, text="Hold", command=self.hold, font=("Helvetica", 12))
        self.play_again_button = tk.Button(master, text="Play Again", command=self.play_again, font=("Helvetica", 12))

        self.dice_label = tk.Label(master, text="", font=("Helvetica", 16))
        self.total_scores_label = tk.Label(master, text="", font=("Helvetica", 14))

        self.roll_button.pack_forget()
        self.hold_button.pack_forget()
        self.play_again_button.pack_forget()

        self.dice_movement_label = tk.Label(master, text="", font=("Helvetica", 16))

        self.table_frame = ttk.Frame(master)
        self.table_frame.pack(side=tk.BOTTOM, pady=20)

        self.table_columns = ("Player", "Score", "Current Roll", "Round Scores")
        self.table = ttk.Treeview(self.table_frame, columns=self.table_columns, show="headings", height=2)
        for col in self.table_columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=100)

        # Add borders
        self.master.configure(bd=10)

    def start_game(self):
        self.num_players = 2
        self.game = PigDiceGame(self.num_players)

        self.choose_players_button.pack_forget()
        self.roll_button.pack(side=tk.LEFT, padx=120)
        self.hold_button.pack(side=tk.RIGHT, padx=120)
        self.show_game_interface()
        self.table.pack()

    def show_game_interface(self):
        # Hide welcome label and display other game interface elements
        self.welcome_label.pack_forget()
        self.current_player_label.pack(pady=10)
        self.total_scores_label.pack(pady=10)
        self.dice_movement_label.pack(pady=10)

        # Update labels and table
        self.update_dice_movement_label()
        self.update_total_scores_label()
        self.update_table()

    def play_again(self):
        # Display the "Start Game" button and hide other game buttons
        self.choose_players_button.pack()
        self.roll_button.pack_forget()
        self.hold_button.pack_forget()
        self.play_again_button.pack_forget()

        # Reset the game state and show the game interface
        self.game.reset_game()
        self.show_game_interface()

    def roll(self):
        # Roll the dice and update the display
        game_over = self.game.roll()
        if game_over:
            self.check_round_winner()
            self.roll_button.config(state=tk.DISABLED)
            self.hold_button.config(state=tk.DISABLED)

        self.update_display()

    def hold(self):
        # Hold the current score and update the display
        game_over = self.game.hold()
        if game_over:
            self.check_round_winner()
            self.roll_button.config(state=tk.DISABLED)
            self.hold_button.config(state=tk.DISABLED)
            self.play_again_button.pack()
        else:
            self.update_display()

    def check_round_winner(self):
        # Check and display the winner of the round
        if self.game.round_winner is not None:
            winner = self.game.round_winner
            messagebox.showinfo("Round Over!", f"Player {winner} wins this round!")

    def update_display(self):
        # Update labels and table based on the current game state
        current_player_data = self.game.players[self.game.current_player]
        self.dice_label.config(text=f"Dice Roll: {current_player_data['current_roll']}")
        self.update_dice_movement_label()
        self.update_total_scores_label()
        self.update_table()
        self.current_player_label.config(text=f"Current Player: {self.game.current_player}")

    def update_dice_movement_label(self):
        # Update the dice movement label
        current_player_data = self.game.players[self.game.current_player]
        self.dice_movement_label.config(text=f"Dice Movement: {current_player_data['current_roll']}")

    def update_total_scores_label(self):
        # Update the total scores label
        total_scores_text = "Total Scores:\n"
        for player, data in self.game.players.items():
            total_scores_text += f"Player {player}: {data['score']}    "
        self.total_scores_label.config(text=total_scores_text)

    def update_table(self):
        # Update the table with player data
        for child in self.table.get_children():
            self.table.delete(child)

        for player, player_data in self.game.players.items():
            values = [player, player_data['score'], player_data['current_roll'], player_data['round_scores']]
            self.table.insert("", "end", values=values)

        self.table["height"] = min(10, len(self.game.players) + 1)

# Main program execution
if __name__ == "__main__":
    root = tk.Tk()
    app = PigDiceGUI(root)
    root.mainloop()
