"""
Main entry point for running from command line.
"""
import os
import sys
import multiprocessing as mp
import tensorflow as tf
from logging import getLogger

_PATH_ = os.path.dirname(os.path.dirname(__file__))

if _PATH_ not in sys.path:
    sys.path.append(_PATH_)

logger = getLogger(__name__)

def setup_gpu():
    """配置 GPU 环境 (TensorFlow 1.x)"""
    # 检查 GPU 可用性
    gpu_available = tf.test.is_gpu_available(cuda_only=True)
    if gpu_available:
        gpu_name = tf.test.gpu_device_name()
        logger.info(f"GPU found: {gpu_name}, using GPU for training")
        # TensorFlow 1.x 默认会使用所有可用 GPU，无需手动设置内存增长
    else:
        logger.info("No GPU found, falling back to CPU")

if __name__ == "__main__":
    mp.set_start_method('spawn')
    sys.setrecursionlimit(10000)

    # 设置 GPU
    setup_gpu()

    from chess_zero import manager
    manager.start()