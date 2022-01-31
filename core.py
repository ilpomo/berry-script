import config
from datetime import datetime
from hashlib import sha1
from pathlib import Path
from py7zr import SevenZipFile
from typing import Dict, List, Tuple
from xml.etree.ElementTree import Element


def process_xml_file(
    machine: Element
) -> Dict[Tuple[str, str, str], List[str]]:

    t0 = datetime.now()
    result = {}

    for row in machine:
        if row.tag == "rom" and row.attrib["status"] != "nodump":

            name_size_sha1 = (row.attrib["name"], row.attrib["size"], row.attrib["sha1"])

            try:
                result[name_size_sha1].append(machine.attrib["name"])

            except KeyError:
                result[name_size_sha1] = [machine.attrib["name"]]

    t1 = datetime.now()
    print(f"{datetime.now()} | processed in {t1 - t0} the xml machine {machine.attrib['name']}")

    return result


def process_zip_file(
    path_tree: Tuple[Path, Dict[Tuple[str, str, str], List[str]]]
) -> None:

    t0 = datetime.now()

    with SevenZipFile(path_tree[0], mode="r") as archive:

        for key, item in archive.readall().items():

            buffer = item.getbuffer()
            name_size_sha1 = (key, str(buffer.nbytes), sha1(buffer).hexdigest())

            try:
                for machine in path_tree[1][name_size_sha1]:

                    machine_path = config.DESTINATION_DIRECTORY_RAW.joinpath(machine)
                    if not machine_path.is_dir():
                        machine_path.mkdir(parents=True, exist_ok=True)

                    with machine_path.joinpath(key).open(mode='wb') as file:
                        file.write(buffer)

            except KeyError:
                pass

    t1 = datetime.now()
    print(f"{datetime.now()} | processed in {t1 - t0} the zip machine {path_tree[0].name}")


def compress_machines(
    path: Path
) -> None:

    t0 = datetime.now()

    with SevenZipFile(config.DESTINATION_DIRECTORY_ZIP.joinpath(f"{path.name}.7z"), 'w') as archive:
        archive.writeall(path, path.name)

    t1 = datetime.now()
    print(f"{datetime.now()} | compressed in {t1 - t0} the raw machine {path.name}")
