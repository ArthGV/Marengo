"""Play against a bot in the browser:  python play.py --bot v3 [--color black]"""
import argparse
import random

import chess

from marengo.bots import available, load_bot
from marengo.gui import serve

parser = argparse.ArgumentParser()
parser.add_argument("--bot", default="v1", help=f"bot module in marengo/bots ({', '.join(available())})")
parser.add_argument("--color", choices=["white", "black"], default="white", help="your color")
parser.add_argument("--port", type=int, default=8000)
parser.add_argument("--vs-random", action="store_true", help="headless: bot (white) vs random mover")
args = parser.parse_args()
bot = load_bot(args.bot)

if args.vs_random:
    board = chess.Board()
    while not board.is_game_over():
        board.push(bot(board) if board.turn == chess.WHITE else random.choice(list(board.legal_moves)))
    print(board, "\n", board.result(), board.outcome().termination.name)
else:
    serve(bot, chess.WHITE if args.color == "white" else chess.BLACK, args.port)
