My code is built up upon chess-alpha-zero, author: Zeta36.
Here is the link to the github repo: https://github.com/Zeta36/chess-alpha-zero

Here is a explaination of what I changed to the files:

1. In api_chess.py, I removed self.running and close(), also removed
try-except in _predict_batch_worker()
2. In model_chess.py, I added get_top_moves()
3. In player_chess.py, I added get_top_moves()
4. In run.py, I enabled GPU usage which matches with my environment.
 The default is CPU.
5. In manager.py, I added compete with stockfish option
6. I created completely new class: EnhancedChessModel,
which has features like SE blocks, Self-attention, etc.
7. Data I used is downloaded from FICS