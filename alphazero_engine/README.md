# RLChessEngine

Using RL to play the game of chess. 

## Codebase structure

bitboards
--bitboard.py
    --pieces.py
        --simple_pieces.py
            --pawns.py
            --kings.py
            --knights.py
        --sliding_pieces.py
            --bishops.py
            --rooks.py
            --queens.py
    --game_meta.py

note: plurality in naming convention is intentional, since bitboard operations move all pieces at once (there is no bitboard for an individual piece, a collection of pieces).
    

