import os
import json
from pathlib import Path
from typing import Any, Dict

class FileManager:
    @staticmethod
    def ensure_dir(path: str):
        Path(path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def ensure_file(path: str, default_content: Any = None):
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                if default_content is not None:
                    if isinstance(default_content, dict):
                        json.dump(default_content, f, indent=2)
                    else:
                        f.write(str(default_content))
                else:
                    f.write('')

    @staticmethod
    def load_json(path: str) -> Dict:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_json(path: str, data: Dict):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
