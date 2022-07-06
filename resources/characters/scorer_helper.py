import csv

from resources.characters.all_characters import get_all_characters

# New plan: save all the pairs to a file and copy them across
all_characters = get_all_characters()
for index_1, char_1 in enumerate(all_characters):
    these_chars = [[char_1, c] for c in all_characters[index_1 + 1:]]
    with open(f"resources/characters/scorer/pairs_{index_1}.csv", "w") as f:
        writer = csv.writer(f)
        for pair in these_chars:
            writer.writerow(pair)

quit()


# Get all the characters
# For each character loop through all the other characters
# then make a dict
# cry

def save_items(scores):
    # Just going to save it in a gross way and will fix later
    for key, value in scores.items():
        with open(f"resources/characters/calculated_scores_{key}.csv", "w") as f:
            writer = csv.writer(f)
            for pair in value:
                writer.writerow(pair)


all_characters = get_all_characters()

""" Scoring method 
5 categories - different to identical
1: different
2: similar idea
3: similar looking
4: very close (i.e. same letter, number, etc)
5: different rotation etc.
"""

scores = {
    1: [],
    2: [],
    3: [],
    4: [],
    5: []
}

for value in scores.keys():
    with open(f"resources/characters/calculated_scores_{value}.csv") as f:
        row_reader = csv.reader(f)
        scores[value] = [row for row in row_reader]

broken = False
for index, char_1 in enumerate(all_characters):
    already_seen = [
        pair[1] for value in scores.values() for pair in value if pair[0] == char_1
    ]
    if len(already_seen) == len(all_characters) - index - 1:
        continue
    next_index = len(already_seen) + index + 1
    # print(f"Next index {next_index}")
    for char_2 in all_characters[next_index:]:
        print(f"comparing {char_1} and {char_2}")
        try:
            score = int(input("Score? "))
            scores[score].append((char_1, char_2))
        except EOFError:
            broken = True
            break
    if broken:
        break
    save_items(scores)

save_items(scores)

# # Just going to save it in a gross way and will fix later
# for key, value in scores.items():
#     with open(f"resources/characters/calculated_scores_{key}.csv", "w") as f:
#         writer = csv.writer(f)
#         for pair in value:
#             writer.writerow(pair)
