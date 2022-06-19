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
    # print("".join(result))
    return result


def from_latin_extended_b():
    result = []
    add_characters(result, 0x0180, [2, 11, 15])
    add_characters(result, 0x0190, [4, 5, 12, 15])
    add_characters(result, 0x01A0, [2, 6, 9])
    add_characters(result, 0x01C0, [1, 2])
    add_characters(result, 0x0220, [1, 2])
    add_characters(result, 0x0230, [4, 5, 8, 9])
    return result


def from_armenian():
    result = []
    add_characters(result, 0x0530, [2, 9, 14])
    add_characters(result, 0x0540, [1, 3, 10])
    add_characters(result, 0x0550, [6])
    add_characters(result, 0x0560, [1])
    add_characters(result, 0x0570, [1, 9])
    add_characters(result, 0x0580, [3, 6, 13, 15])
    return result


def from_georgian():
    result = []
    add_characters(result, 0x10A0, [1, 3, 7, 9, 12])
    add_characters(result, 0x10B0, [2, 5, 14, 15])
    add_characters(result, 0x10C0, [4, 5])
    add_characters(result, 0x10D0, [1, 10, 14])
    add_characters(result, 0x10E0, [0, 10, 13])
    add_characters(result, 0x10F0, [1, 5, 6, 8, 11])
    # print(" ".join(result))
    return result


def from_phonetic_extensions():
    result = []
    add_characters(result, 0x1D10, [5])
    add_characters(result, 0x1D20, [5])
    add_characters(result, 0x1D70, [9, 11])
    print(" ".join(result))
    return result


def from_greek_and_coptic():
    result = []
    add_characters(result, 0x0370, [0, 2, 12, 13])
    add_characters(result, 0x0390, [4, 8])
    add_characters(result, 0x03A0, [0, 3, 6, 8, 9])
    add_characters(result, 0x03B0, [1, 2, 4, 5, 11, 13])
    add_characters(result, 0x03C0, [1, 3, 4, 6, 8, 9])
    add_characters(result, 0x03D0, [0, 6, 8, 15])
    add_characters(result, 0x03E0, [1, 2, 7, 10])
    return result


def get_all_characters():
    char_list = []
    char_list.extend(from_basic_latin())
    char_list.extend(from_basic_latin_supplement_1())
    char_list.extend(from_latin_extended_b())
    char_list.extend(from_greek_and_coptic())
    char_list.extend(from_armenian())
    char_list.extend(from_georgian())
    char_list.extend(from_phonetic_extensions())

    return char_list


if __name__ == '__main__':
    get_all_characters()
    # [print(c) for c in get_all_characters()]
