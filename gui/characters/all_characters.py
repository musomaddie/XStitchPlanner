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
    return result


def from_phonetic_extensions():
    result = []
    add_characters(result, 0x1D10, [5])
    add_characters(result, 0x1D20, [5])
    add_characters(result, 0x1D70, [9, 11])
    return result


def from_general_punctuation():
    result = []
    add_characters(result, 0x2010, [6])
    add_characters(result, 0x2020, [0, 1, 2])
    add_characters(result, 0x2030, [11, 12, 13, 15])
    add_characters(result, 0x2040, [0, 1, 2, 5, 6, 7, 10, 12, 13])
    add_characters(result, 0x2050, [0, 1, 2, 3, 6, 8, 9, 12])
    return result


def from_currency_symbols():
    result = []
    add_characters(result, 0x20A0, [0, 1, 4, 6, 9, 10, 13, 14])
    add_characters(result, 0x20B0, [1, 3, 4, 8, 9])
    return result


def from_arrows():
    result = []
    add_characters(result, 0x2190, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 15])
    add_characters(result, 0x21A0, [0, 1, 2, 3, 9, 10, 13, 15])
    add_characters(result, 0x21B0, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    add_characters(result, 0x21C0, [11, 12, 13, 15])
    add_characters(result, 0x21D0, [0, 1, 2, 3, 4, 14, 15])
    add_characters(result, 0x21E0, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    add_characters(result, 0x21F0, [0, 1, 2, 13, 14, 15])
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


def from_misc_tech():
    result = []
    add_characters(result, 0x2300, [2, 7])
    add_characters(result, 0x2310, [1, 2, 3, 4, 5, 6, 7, 8])
    add_characters(result, 0x2320, [5, 6, 7, 11, 12, 13])
    add_characters(result, 0x2330, [2, 6, 10, 13])
    add_characters(result, 0x2340, [9, 11])
    add_characters(result, 0x2350, [9, 10, 12, 13])
    add_characters(result, 0x2370, [11, 14])
    add_characters(result, 0x2380, [4, 6, 7, 8, 11, 12, 13])
    add_characters(result, 0x2390, [1, 4, 6])
    add_characters(result, 0x23C0, [1, 2, 3, 4, 5, 6, 15])
    add_characters(result, 0x23D0, [4, 9])
    add_characters(result, 0x23E0, [2, 3, 6])
    return result


def from_geometric_shapes():
    result = []
    add_characters(result, 0x25A0, [2, 3, 8])
    add_characters(result, 0x25B0, [1, 2, 3, 7, 13])
    add_characters(result, 0x25C0, [2, 7, 8, 9, 10, 13, 14])
    add_characters(result, 0x25D0, [0, 1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15])
    add_characters(result, 0x25E0, [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    add_characters(result, 0x25F0, [0, 1, 2, 3, 14])
    return result


def from_dingbats():
    result = []
    add_characters(result, 0x2700, [2, 4, 6, 7, 8, 9, 14, 15])
    add_characters(result, 0x2710, [0, 1, 2, 3, 4, 6, 7, 9, 12, 13, 14])
    add_characters(result, 0x2720, [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 14, 15])
    add_characters(result, 0x2730, [0, 1, 8, 11, 14, 15])
    add_characters(result, 0x2740, [0, 3, 4, 7, 8, 9])
    add_characters(result, 0x2750, [6, 11, 12, 13, 14])
    add_characters(result, 0x2760, [1, 2, 4, 5, 14, 15])
    add_characters(result, 0x2770, [6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    add_characters(result, 0x2790, [4, 5, 7, 12])
    add_characters(result, 0x27A0, [4])
    add_characters(result, 0x27B0, [0, 2, 3, 5, 8, 12, 14, 15])
    return result


def from_ancient_symbols():
    result = []
    add_characters(result, 0x10190, [2, 3, 6, 7, 10, 11])
    print(" ".join(result))
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
    char_list.extend(from_general_punctuation())
    char_list.extend(from_currency_symbols())
    char_list.extend(from_arrows())
    char_list.extend(from_misc_tech())
    char_list.extend(from_geometric_shapes())
    char_list.extend(from_dingbats())
    char_list.extend(from_ancient_symbols())

    return char_list


if __name__ == '__main__':
    get_all_characters()
    # [print(c) for c in get_all_characters()]
