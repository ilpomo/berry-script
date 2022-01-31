import config
from concurrent.futures import ProcessPoolExecutor
from core import process_xml_file, process_zip_file, compress_machines
from datetime import datetime
from itertools import repeat
from typing import Dict, List, Tuple
from xml.etree import ElementTree


if __name__ == "__main__":

    xml_root = ElementTree.parse(source=config.XML_PATH).getroot()
    xml_tree: Dict[Tuple[str, str, str], List[str]] = {}  # {('name', 'size', 'sha1'): ['machine_0', ...]}

    t0 = datetime.now()

    with ProcessPoolExecutor(max_workers=config.MAX_CPU_CORES) as executor:

        # process xml tree in parallel
        for future in executor.map(process_xml_file, list(xml_root.findall("machine"))[:1000]):
            for name_size_sha1, machines in future.items():
                try:
                    xml_tree[name_size_sha1].extend(machines)

                except KeyError:
                    xml_tree[name_size_sha1] = machines

        # process zip files in parallel
        executor.map(process_zip_file, zip(sorted(config.ZIP_PATH.iterdir())[:1000], repeat(xml_tree)))

        # compress raw machines in parallel
        executor.map(compress_machines, list(config.DESTINATION_DIRECTORY_RAW.iterdir()))

    t1 = datetime.now()
    print(f"{datetime.now()} | process completed in {t1 - t0}")
