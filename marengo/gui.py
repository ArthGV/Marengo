"""Tiny local web GUI (stdlib only) to play against a bot in the browser."""
import json
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import chess

from marengo.bots import Bot

PAGE = (Path(__file__).parent / "gui.html").read_bytes()


class Game:
    def __init__(self, bot: Bot, human: chess.Color):
        self.bot, self.human = bot, human
        self.board = chess.Board()
        self.error = None
        self.last = None
        self.bot_reply()

    def bot_reply(self):
        self.error = None
        if self.board.is_game_over() or self.board.turn == self.human:
            return
        try:
            move = self.bot(self.board)
            if move not in self.board.legal_moves:
                raise ValueError(f"bot returned illegal move {move}")
            self.board.push(move)
            self.last = move.uci()
        except Exception as e:  # show bot bugs in the UI instead of crashing
            self.error = f"{type(e).__name__}: {e}"

    def play(self, uci: str):
        move = chess.Move.from_uci(uci)
        if chess.Move.from_uci(uci + "q") in self.board.legal_moves:
            move = chess.Move.from_uci(uci + "q")  # auto-queen
        if self.board.turn != self.human or move not in self.board.legal_moves:
            self.error = "illegal move"
            return
        self.board.push(move)
        self.last = move.uci()
        self.bot_reply()

    def state(self) -> dict:
        legal = {}
        if self.board.turn == self.human:
            for m in self.board.legal_moves:
                legal.setdefault(chess.square_name(m.from_square), []).append(chess.square_name(m.to_square))
        outcome = self.board.outcome()
        return {
            "fen": self.board.fen(),
            "human": "white" if self.human else "black",
            "legal": legal,
            "last": self.last,
            "error": self.error,
            "result": outcome.result() if outcome else None,
            "termination": outcome.termination.name if outcome else None,
        }


def serve(bot: Bot, human: chess.Color, port: int) -> None:
    game = Game(bot, human)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def send(self, body: bytes, ctype: str):
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path == "/state":
                self.send(json.dumps(game.state()).encode(), "application/json")
            else:
                self.send(PAGE, "text/html; charset=utf-8")

        def do_POST(self):
            nonlocal game
            data = json.loads(self.rfile.read(int(self.headers["Content-Length"])) or b"{}")
            if self.path == "/move":
                game.play(data["uci"])
            elif self.path == "/new":
                color = chess.WHITE if data.get("color", "white") == "white" else chess.BLACK
                game = Game(bot, color)
            self.send(json.dumps(game.state()).encode(), "application/json")

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}"
    print(f"Marengo GUI on {url} (Ctrl+C to stop)")
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
