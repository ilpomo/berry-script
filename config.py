from pathlib import Path


XML_PATH = Path.home().joinpath('Downloads', 'mame0240.xml')
ZIP_PATH = Path.home().joinpath('Downloads', 'mame0239roms')

DESTINATION_DIRECTORY_RAW = Path.home().joinpath('Downloads', 'raw')
DESTINATION_DIRECTORY_ZIP = Path.home().joinpath('Downloads', 'zip')

for _ in (DESTINATION_DIRECTORY_RAW, DESTINATION_DIRECTORY_ZIP):
    if not _.is_dir():
        _.mkdir(parents=True, exist_ok=True)

MAX_CPU_CORES = 2
