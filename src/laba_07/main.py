import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.laba_07.app import Application
from src.laba_07.cli import CLI

def main():
    print("=" * 50)
    print("  ИНФОРМАЦИОННАЯ СИСТЕМА СОРЕВНОВАНИЙ")
    print("=" * 50)
    
    data_dir = Path(__file__).parent.parent.parent / "data"
    data_file = str(data_dir / "competitions.json")
    
    app = Application(data_file)
    print(f"Загружено соревнований: {len(app.get_all())}")
    
    cli = CLI(app)
    cli.run()

if __name__ == "__main__":
    main()