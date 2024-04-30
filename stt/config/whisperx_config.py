from dotenv import load_dotenv
from pathlib import Path
import os


class WhisperxConfig:
    def __init__(self,
                 path_to_env: str):
        path = Path(path_to_env)
        load_dotenv(path)
    
    def get_log_file_path(self) -> str:
        return os.getenv('log', 'data/logs/stt.log')
    def get_model_size(self) -> str:
        return os.getenv('model_size', 'medium')

    def get_device(self) -> str:
        return os.getenv('device', 'cpu')

    def get_compute_type(self) -> str:
        return os.getenv('compute_type', 'int8')

    def get_batch_size(self) -> int:
        return int(os.getenv('batch_size', 8))