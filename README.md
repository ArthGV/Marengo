# Marengo

Chess bot. Each bot is a module in `marengo/bots/` (v1.py, v2.py, ...) exposing `bot(board)`. Copy to start a new version.

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python play.py --bot v1   # play against a bot in the browser (--color black, --port N)
python play.py --bot v0_random --vs-random   # headless bot vs random
python -m marengo.uci --bot v1   # UCI (waits for stdin commands; for GUIs/tools) engine on stdin/stdout
```

Next steps: [lichess-bot](https://github.com/lichess-bot-devs/lichess-bot) to play online, `cutechess-cli`/`fastchess` + Stockfish (`UCI_LimitStrength`, `UCI_Elo`) to estimate Elo.
