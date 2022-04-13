from pprint import pprint
from copy import deepcopy
import yaml


def load_archetypes():
    """
    Function that opens archetypes.yml and returns a dictionary of archetypes.
    """
    with open('archetypes.yml', 'r') as f:
        archetypes = yaml.load(f, Loader=yaml.SafeLoader)
    return archetypes


def process_bro(bro):
    """
    Function that processes a bro's stats and returns a dictionary.
    If the stats contain a + sign, create a new key named stars with the number following that + sign.
    """
    bro_stats = {}
    for key, value in bro.items():
        if key == "name":
            continue
        bro_stats[key] = {}
        if '+' in str(value):
            bro_stats[key]["stat"] = int(value.split('+')[0])
            bro_stats[key]["stars"] = int(value.split('+')[1])
        else:
            bro_stats[key]["stat"] = int(value)
            bro_stats[key]["stars"] = 0
    return bro_stats


def level_bro(bro: dict, level: int, arch: dict):
    """
    Function that increments a bro's stats based on the stat's stars.
    The stats that are levelled are the ones defined in the archetype.
    If the stat is matk or mdef, it increments by 2 per level * 0.5 stars
    Any other stat increments by 3 per level * 0.5 stars
    """
    bro_score = 0
    arch_score = 0
    trained_bro = {
        "class": arch["name"],
        "level": level + 1,
        "score": 0,
        "stats": {}
    }

    for key, value in arch["main_stats"].items():
        trained_bro["stats"][key] = {
            "value": 0,
            # "pass": False
        }
        arch_score += value

    for key in trained_bro["stats"]:
        if key == "matk" or key == "mdef":
            modifier = 2
        else:
            modifier = 3

        stat = float(bro[key]["stat"]) + (level * modifier + (0.5 * bro[key]["stars"]))
        stat = round(stat)
        trained_bro["stats"][key]["value"] = stat

        # if stat >= arch["main_stats"][key]:
        #     trained_bro["stats"][key]["pass"] = True

        bro_score += stat

    trained_bro["score"] = f"{round(bro_score / arch_score * 100)}%"

    return trained_bro


def new_level(tmp_bro: dict, arch: dict, level: int) -> dict:
    def level_stat(stat_name: str, stat_value: dict):
        if stat_name == "matk" or stat_name == "mdef":
            modifier = 2
        else:
            modifier = 3

        stat = modifier + (0.5 * stat_value["stars"])
        stat = round(stat)
        print(f"Rolled {stat}")
        return stat

    total_count = 0
    count = 0
    while count < level:
        print(f"\nLEVEL {count+1}")
        point_counter = 0
        for arch_stat, arch_value in arch.items():
            print(f"\n{arch_stat}")
            if tmp_bro[arch_stat]["stat"] < arch_value:
                print(f'{tmp_bro[arch_stat]["stat"]} is smaller than {arch_value}')
                tmp = level_stat(arch_stat, tmp_bro[arch_stat])
                tmp_bro[arch_stat]["stat"] += tmp
                print(f'{tmp_bro[arch_stat]["stat"]}')
                point_counter += 1
                total_count += 1
            else:
                print(f'Skipping => {tmp_bro[arch_stat]["stat"]} > {arch_value}')
            if point_counter == 3:
                print("\nPoint counter reached, moving to next level")
                break
        if point_counter < 3:
            print("\nMoving to free assignment")
            for arch_stat, arch_value in arch.items():
                print(f"\n{arch_stat}")
                tmp = level_stat(arch_stat, tmp_bro[arch_stat])
                tmp_bro[arch_stat]["stat"] += tmp
                print(f'{tmp_bro[arch_stat]["stat"]}')
                point_counter += 1
                total_count += 1
                if point_counter == 3:
                    print("\nPoint counter reached, moving to next level (x)")
                    break
        count += 1

    print(f"Total count = {total_count}")
    return tmp_bro


archetypes = load_archetypes()

bro = {
    "name": "Ivar",
    "health": 63,
    "fatigue": "93+2",
    "resolve": 29,
    "initiative": 86,
    "matk": "51+1",
    "ratk": "42+2",
    "mdef": 5,
    "rdef": 5
}

final_broes = []

bro = process_bro(bro)

new_bro = []
new_bro.append({"level 1:": bro})

res = new_level(deepcopy(bro), archetypes[0]["main_stats"], 5)
adds = 0
for key, value in bro.items():
    adds += res[key]["stat"] - value["stat"]
    print(f'{key} - {value["stat"]} + {res[key]["stat"] - value["stat"]} = {res[key]["stat"]}')
print(f"adds: {adds}")

# for arch in archetypes:
#     new_bro.append({f"level 5 {arch['name']}": level_bro(bro, 4, arch)})
#     new_bro.append({f"level 11 {arch['name']}": level_bro(bro, 10, arch)})

# pprint(new_bro)
