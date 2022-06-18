# Get from basic latin

def from_basic_latin():
    result = []
    full_lines_starters = [0x0030, 0x0040, 0x0050, 0x0060]
    full_length = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF]
    result.extend([chr(0x0000 + 0x0020 + v) for v in full_length[1:]])
    result.extend(
        [chr(0x0000 + f + fl) for f in full_lines_starters for fl in full_length]
    )
    result.extend([chr(0x0070 + v) for v in full_length[:-1]])
    return result


def get_all_characters():
    char_list = []
    char_list.extend(from_basic_latin())
    print(" ".join(char_list))

    return char_list


if __name__ == '__main__':
    get_all_characters()
    # [print(c) for c in get_all_characters()]
