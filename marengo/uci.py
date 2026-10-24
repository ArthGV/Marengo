"""Minimal UCI wrapper so the bot plugs into GUIs, cutechess-cli and lichess-bot."""
import argparse
import sys

import chess

from marengo.bots import load_bot


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bot", default="v1")
    bot = load_bot(parser.parse_args().bot)
    board = chess.Board()
    for line in sys.stdin:
        tokens = line.split()
        if not tokens:
            continue
        cmd = tokens[0]
        if cmd == "uci":
            print("id name Marengo")
            print("id author ArthGV")
            print("uciok")
        elif cmd == "isready":
            print("readyok")
        elif cmd == "ucinewgame":
            board = chess.Board()
        elif cmd == "position":
            if tokens[1] == "startpos":
                board = chess.Board()
                rest = tokens[2:]
            else:  # position fen <6 fields> [moves ...]
                board = chess.Board(" ".join(tokens[2:8]))
                rest = tokens[8:]
            if rest[:1] == ["moves"]:
                for uci in rest[1:]:
                    board.push_uci(uci)
        elif cmd == "go":
            print(f"bestmove {bot(board).uci()}")
        elif cmd == "quit":
            break
        sys.stdout.flush()


if __name__ == "__main__":
    main()
