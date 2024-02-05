import json
import os
from pathlib import Path, PurePosixPath


def __main__():
    eat = []
    not_eat = []

    for name in os.listdir(Path("data/eating")):
        eat_dictionary = dict()
        eat_dictionary["name"] = name.split('.')[0]
        eat_dictionary["path"] = str(PurePosixPath(Path("eating") / name))
        eat.append(eat_dictionary)

    with Path("data/eat_json.txt").open("w", encoding="UTF-8") as folder:
        json.dump(eat, folder)

    for name in os.listdir(Path("data/not_eating")):
        not_eat_dictionary = dict()
        not_eat_dictionary["name"] = name.split(".")[0]
        not_eat_dictionary["path"] = str(PurePosixPath(Path("not_eating") / name))
        not_eat.append(not_eat_dictionary)
    with Path("data/not_eat_json.txt").open("w", encoding="UTF-8") as folder:
        json.dump(not_eat, folder)
