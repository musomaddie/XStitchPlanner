# Get from basic latin
FULL_LENGTH = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF]


def add_characters(result_list, prefix, indices):
    result_list.extend([chr(prefix + FULL_LENGTH[i]) for i in indices])


def from_basic_latin():
    result = []
    full_lines_starters = [0x0030, 0x0040, 0x0050, 0x0060]
    result.extend([chr(0x0000 + 0x0020 + v) for v in FULL_LENGTH[1:]])
    result.extend(
        [chr(0x0000 + f + fl) for f in full_lines_starters for fl in FULL_LENGTH]
    )
    result.extend([chr(0x0070 + v) for v in FULL_LENGTH[:-1]])
    return result


def from_basic_latin_supplement_1():
    result = []
    add_characters(result, 0x00A0, [3, 4, 5, 6, 7, 9, 11, 12, 14])
    add_characters(result, 0x00B0, [1, 5, 6, 11])
    add_characters(result, 0x00C0, [6])
    add_characters(result, 0x00D0, [8, 14, 15])
    add_characters(result, 0x00F0, [7])
    print("".join(result))
    return result


def get_all_characters():
    char_list = []
    char_list.extend(from_basic_latin())
    char_list.extend(from_basic_latin_supplement_1())

    return char_list


if __name__ == '__main__':
    get_all_characters()
    # [print(c) for c in get_all_characters()]
