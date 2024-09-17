# sudoku.py
# Functionality: All the sudoku game commands in a SudokuGame class
# Created by Sai Chamarty
import discord
from discord.ext import commands
import random
import json

class SudokuGame:
    def __init__(self, initial_boards):
        self.initial_boards = initial_boards
        self.game_state = {}
    
    @staticmethod
    # load initial boards from JSON file
    def load_initial_boards(filename = 'initial_boards.json'):
        with open(filename, 'r') as file:
            data = json.load(file)
        return data['boards']
    
    # starts a sudoku game
    async def start_game(self, player_id):
        if player_id in self.game_state:
            return "You already have an ongoing Sudoku game! Use `!endsudoku` to end it before starting a new one."
        board = [row[:] for row in random.choice(self.initial_boards)]
        self.game_state[player_id] = {
            'board': board,
            'moves': 0
        }
        return f"Let's start the Sudoku game! Here is your board: \n{self.format_board(board)}"
    
    # ends an existing game
    async def end_game(self, player_id):
        if player_id in self.game_state:
            del self.game_state[player_id]
            return "Your Sudoku game has been ended."
        else:
            return "You don't have an ongoing Sudoku game."
        
    # formats the regular json board into embeddable format
    @staticmethod
    def format_board(board):
        # Map digits to emojis
        num_to_emoji = {
            1: "1️⃣",
            2: "2️⃣",
            3: "3️⃣",
            4: "4️⃣",
            None: "⬜"  # Use this for empty cells
        }
        index_emoji = {
            1: "𝟭",
            2: "𝟮",
            3: "𝟯",
            4: "𝟰"
        }

        formatted_board = "\t\t\t" + "\t  ".join(index_emoji[i+1] for i in range(4)) + "\n" 
        formatted_board += "\n"

        for idx, row in enumerate(board):
            formatted_row = f"{index_emoji[idx + 1]}\t\t" + "\t".join(num_to_emoji[cell] for cell in row)
            formatted_board += formatted_row + "\n"
            formatted_board += "\n"

        return formatted_board
    
    # checks if the board is valid or not
    def is_valid_move(self, player_id, row, col, number):
        board = self.game_state[player_id]['board']

        for i in range(4):
            if board[row][i] == number or board[i][col] == number:
                return False
            
        # calculate the starting row and column indices of the 2x2 subgrid
        start_row, start_col = 2 * (row // 2), 2 * (col // 2)

        # check if num is not in the 2x2 subgrid
        for i in range(2):
            for j in range(2):
                if board[start_row + i][start_col + j] == number:
                    return False
                
        # if num not found in row, column, and subgrid, the move is valid
        return True
    
    # checks if the board is full
    @staticmethod
    def is_board_complete(board):
        for row in board:
            if None in row:
                return False
        return True
    
    # places a number on [row, col] of the sudoku board
    async def placenum(self, player_id, row, col, number):
        if player_id not in self.game_state:
            return "You don't have an ongoing Sudoku game. Start a new game with `s.startsudoku`."
        
        state = self.game_state[player_id]
        board = state['board']

        if not (1 <= row <= 4 and 1 <= col <= 4 and 1 <= number <= 4):
            state['moves'] += 1
            return "Invalid input! Row, column, and number must be between 1 and 4."
        
        if not self.is_valid_move(player_id, row - 1, col - 1, number):
            state['moves'] += 1
            return "Invalid move! Number cannot be placed there."
        
        board[row - 1][col - 1] = number
        state['moves'] += 1

        if self.is_board_complete(board):
            result = f"Congratulations! You have completed the Sudoku puzzle in {state['moves']} moves:\n{self.format_board(board)}"
            del self.game_state[player_id]
            return result
        else:
            return f"Number placed! Here is your updated board:\n{self.format_board(board)}"
    
    # checks if the place [row, col] on the sudoku board is free or not
    def is_place_free(self, player_id, row, col):
        state = self.game_state[player_id]
        board = state['board']
        for i in range(4):
            for j in range(4):
                if i == row - 1 and j == col - 1:
                    if board[i][j] == None:
                        return True
                    else:
                        return False

    # remove a number from [row, col] of a sudoku board
    async def removenum(self, player_id, row, col):
        if player_id not in self.game_state:
            return "You don't have an ongoing Sudoku game. Start a new game with `s.startsudoku`."
        
        state = self.game_state[player_id]
        board = state['board']

        if not (1 <= row <= 4 and 1 <= col <= 4):
            state['moves'] += 1
            return "Invalid input! Row, column, and number must be between 1 and 4."
        if not self.is_place_free(player_id, row, col):
            state['moves'] += 1
            board[row - 1][col - 1] = None
            return f"Number removed! Here is your updated board:\n{self.format_board(board)}"
        else:
            state['moves'] += 1
            return "Nothing to remove. The place is free."

class sudoku10:
    def __init__(self, initial_boards):
        self.initial_boards = initial_boards
        self.channel_game_state = {}
    
    @staticmethod
    # load initial boards from the JSON file
    def load_initial_boards_9(filename = 'initial_boards.json'):
        with open(filename, 'r') as file:
            data = json.load(file)
        return data['boards10']
    
    #starts a 10x10 sudoku game
    async def start_game(self, channel_id):
        # Check if the game is already running in the channel
        if channel_id in self.channel_game_state:
            return "A Sudoku game is already ongoing in this channel! Use `s.end` to end it before starting a new one."
        board = [row[:] for row in random.choice(self.initial_boards)]
        # Initialize the game state for the channel
        self.channel_game_state[channel_id] = {
            'board': board,
            'moves': 0  # Tracks total moves made in the game
        }

        # Return a message with the formatted board
        return f"Let's start the 9x9 multiplayer Sudoku game! Here is the board:\n{self.format_board(board)}"
    
    # ends an existing game
    async def end_game(self, channel_id):
        if channel_id in self.channel_game_state:
            del self.channel_game_state[channel_id]
            return "Your multiplayer Sudoku game has been ended."
        else:
            return "This channel does not have an ongoing Sudoku game."
        
    # formats the regular json board into embeddable format
    @staticmethod
    def format_board(board):
        # Map digits to emojis
        num_to_emoji = {
            1: "1️⃣",
            2: "2️⃣",
            3: "3️⃣",
            4: "4️⃣",
            5: "5️⃣",
            6: "6️⃣",
            7: "7️⃣",
            8: "8️⃣",
            9: "9️⃣",
            None: "⬜"  # Use this for empty cells
        }

        formatted_board = ""
        formatted_row_index = "⬜ | 1️⃣ 2️⃣ 3️⃣ | 4️⃣ 5️⃣ 6️⃣ | 7️⃣ 8️⃣ 9️⃣"
        formatted_row_index += "\n---------------------------------------"
        formatted_board += formatted_row_index + "\n"

        for row_idx, row in enumerate(board):
            # Add a horizontal separator after every 3rd row (except for the first row)
            if row_idx % 3 == 0 and row_idx != 0:
                formatted_board += "---------------------------------------\n"
            
            formatted_row = f"{num_to_emoji[row_idx + 1]} | "  # Row index (emoji version)
            for col_idx, cell in enumerate(row):
                # Add a vertical separator after every 3rd column (except for the first column)
                if col_idx % 3 == 0 and col_idx != 0:
                    formatted_row += "| "
                formatted_row += num_to_emoji[cell] + " "
            
            # Add the formatted row to the final board
            formatted_board += formatted_row.strip() + "\n"

        return formatted_board


    def is_valid_move(self, channel_id, row, col, number):
        board = self.channel_game_state[channel_id]['board']

        for i in range(9):
            if board[row][i] == number or board[i][col] == number:
                return False
            
        # Calculate the starting row and column indices of the 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)

        # check if num is not in the 2x2 subgrid
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == number:
                    return False
        
        # if num not found in row, column, and subgrid, the move is valid
        return True

    # checks if the board is full
    @staticmethod
    def is_board_complete(board):
        for row in board:
            if None in row:
                return False
        return True
    

    # places a number on [row, col] of the sudoku board
    async def placenum(self, channel_id, row, col, number):
        if channel_id not in self.channel_game_state:
            return "You don't have an ongoing Sudoku game. Start a new game with `s.startsudoku`."
        
        state = self.channel_game_state[channel_id]
        board = state['board']

        if not (1 <= row <= 9 and 1 <= col <= 9 and 1 <= number <= 9):
            state['moves'] += 1
            return "Invalid input! Row, column, and number must be between 1 and 4."
        
        if not self.is_valid_move(channel_id, row - 1, col - 1, number):
            state['moves'] += 1
            return "Invalid move! Number cannot be placed there."
        
        board[row - 1][col - 1] = number
        state['moves'] += 1

        if self.is_board_complete(board):
            result = f"Congratulations! You have completed the Sudoku puzzle in {state['moves']} moves:\n{self.format_board(board)}"
            del self.channel_game_state[channel_id]
            return result
        else:
            return f"Number placed! Here is your updated board:\n{self.format_board(board)}"
        
    # checks if the place [row, col] on the sudoku board is free or not
    def is_place_free(self, player_id, row, col):
        state = self.channel_game_state[player_id]
        board = state['board']
        for i in range(9):
            for j in range(9):
                if i == row - 1 and j == col - 1:
                    if board[i][j] == None:
                        return True
                    else:
                        return False
    
    # remove a number from [row, col] of a sudoku board
    async def removenum(self, channel_id, row, col):
        if channel_id not in self.channel_game_state:
            return "You don't have an ongoing Sudoku game. Start a new game with `s.startsudoku`."
        
        state = self.channel_game_state[channel_id]
        board = state['board']

        if not (1 <= row <= 9 and 1 <= col <= 9):
            state['moves'] += 1
            return "Invalid input! Row, column, and number must be between 1 and 4."
        if not self.is_place_free(channel_id, row, col):
            state['moves'] += 1
            board[row - 1][col - 1] = None
            return f"Number removed! Here is your updated board:\n{self.format_board(board)}"
        else:
            state['moves'] += 1
            return "Nothing to remove. The place is free."