import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.board = [' '] * 9
        self.current_player = 'X'
        self.buttons = []
        self.game_mode = None
        self.create_mode_selection()

    def create_mode_selection(self):
        self.clear_window()
        tk.Label(self.root, text="Choose Game Mode:").pack(pady=10)
        tk.Button(self.root, text="Player vs Player", command=lambda: self.start_game('PVP')).pack(pady=5)
        tk.Button(self.root, text="Player vs AI", command=lambda: self.start_game('PVE')).pack(pady=5)

    def start_game(self, mode):
        self.game_mode = mode
        self.board = [' '] * 9
        self.current_player = 'X'
        self.clear_window()

        frame = tk.Frame(self.root)
        frame.pack()
        for i in range(9):
            button = tk.Button(frame, text=' ', font=('Arial', 36), height=2, width=5,
                               command=lambda i=i: self.make_move(i))
            button.grid(row=i//3, column=i%3)
            self.buttons.append(button)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.buttons.clear()

    def make_move(self, index):
        if self.board[index] != ' ':
            return
        self.board[index] = self.current_player
        self.buttons[index]['text'] = self.current_player

        if self.check_winner(self.current_player):
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            self.ask_play_again()
            return
        elif ' ' not in self.board:
            messagebox.showinfo("Game Over", "It's a tie!")
            self.ask_play_again()
            return

        self.current_player = 'O' if self.current_player == 'X' else 'X'

        if self.game_mode == 'PVE' and self.current_player == 'O':
            self.root.after(500, self.ai_move)

    def ai_move(self):
        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                score = self.minimax(self.board, 0, False)
                self.board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i

        if best_move is not None:
            self.make_move(best_move)

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner('O'):
            return 1
        elif self.check_winner('X'):
            return -1
        elif ' ' not in board:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'O'
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'X'
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ' '
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        wins = [(0,1,2), (3,4,5), (6,7,8),
                (0,3,6), (1,4,7), (2,5,8),
                (0,4,8), (2,4,6)]
        return any(self.board[a]==self.board[b]==self.board[c]==player for a,b,c in wins)

    def ask_play_again(self):
        if messagebox.askyesno("Play Again?", "Do you want to play again?"):
            self.create_mode_selection()
        else:
            self.root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
