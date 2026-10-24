import chess
import random


def bot(board: chess.Board) -> chess.Move:
    return random.choice(list(board.legal_moves))
