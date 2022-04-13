from pprint import pprint

stat_order = [
    "hlth", #0
    "fatg", #1
    "rslv", #2
    "init", #3
    "matk", #4
    "ratk", #5
    "mdef", #6
    "rdef"  #7
]


classes = {
    "tank": [0,2,6],
    "wrecker": [1,4,6],
    "spearman": [2,4,6],
    "sarge": [1,2,4],
    "archer": [3,5,7]
}

with open("broes.csv", "r") as f:
    broes = f.read()

bro_list = [ i.split(",") for i in broes.split("\n")]

bro_array = {}
for bro in bro_list:
    """
        "name",1,2,3,4,5
        {
            "name": eberecht,
            "helt": {
                "base": 0,
                "incr": 0
            },
        }
    """
    name = bro[0]
    stats = bro[1:]
    bro_array[name] = {}
    
    for count, value in enumerate(stats):
        if "+" in value:
            stuff = value.split('+')
            base = int(stuff[0])
            incr = int(stuff[1])
        else:
            base = int(value)
            incr = 0
        bro_array[name][stat_order[count]] = {
            "base": base,
            "incr": incr
        }


def level_broes(broes, iterations):
    for _, stats in broes.items():
        for _, stat_value in stats.items():
            normal_incr = iterations * 2
            special_incr = iterations * stat_value["incr"]
            stat_value["leveled"] = stat_value["base"] +  normal_incr + special_incr

    return broes


def print_score(name, score):
    bar = "▄" * score["leveled"]
    print(f"{name} - {bar} {score['leveled']} ({score['base']}+{score['incr']})")


def find_best(broes, choice, level):
    print(f"\n========== {choice.upper()} LEVEL {level} ==========")
    
    broes = level_broes(broes, level)
    class_score = classes[choice]
    stat0 = stat_order[class_score[0]]
    stat1 = stat_order[class_score[1]]
    stat2 = stat_order[class_score[2]]

    tmp_dict = {}
    for bro, stats in broes.items():
        total = int(stats[stat0]["leveled"]) + int(stats[stat1]["leveled"]) + int(stats[stat2]["leveled"])
        
        tmp_dict[bro] = {}
        tmp_dict[bro]["total"] = total
        tmp_dict[bro][stat0] = stats[stat0] #["leveled"]
        tmp_dict[bro][stat1] = stats[stat1] #["leveled"]
        tmp_dict[bro][stat2] = stats[stat2] #["leveled"]

    tmp_dict = {k: v for k, v in sorted(tmp_dict.items(), key=lambda item: item[1]["total"], reverse=True)}
    
    for bro, stats in tmp_dict.items():

        print()
        print(bro)
        print(f"Total: {stats['total']}")
        print_score(stat0, stats[stat0])
        print_score(stat1, stats[stat1])
        print_score(stat2, stats[stat2])
    # print()
    # print(cla)
    # for bro, score in bro_scores.items():
    #     print(bro, score)


########################################################################################


#print_stats()
find_best(bro_array, "tank", 5)
#find_best(bro_array, "tank", 10)
find_best(bro_array, "wrecker", 5)
#find_best(bro_array, "wrecker", 10)
find_best(bro_array, "sarge", 5)
#find_best(bro_array, "sarge", 10)
find_best(bro_array, "archer", 5)
#find_best(bro_array, "archer", 10)

