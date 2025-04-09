@echo off
REM 设置 conda 的路径（如果未添加到环境变量中）
SET CONDA_PATH=C:\Users\LucasLiu\miniconda3

REM 初始化 conda（如果已将 conda 添加到环境变量，则可以省略）
CALL "%CONDA_PATH%\Scripts\activate.bat"

REM 激活你的 Conda 环境
CALL conda activate alpha-zero

REM 运行 ChessZero 的 UCI 模式
CALL python src/chess_zero/run.py --cmd uci