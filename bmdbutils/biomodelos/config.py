from pathlib import Path
import configparser
import appdirs

CONFIG_DIR = Path(appdirs.user_config_dir("bmdbutils"))
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_FILE = CONFIG_DIR / "biomodelos"


def load_config():
    config = configparser.ConfigParser(interpolation=None)
    if CONFIG_FILE.exists():
        config.read(CONFIG_FILE)
    return config


def save_config(config):
    with CONFIG_FILE.open("w") as f:
        config.write(f)