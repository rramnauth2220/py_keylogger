# author:       Rebecca Ramnauth
# last update:  07 January 2020

from datetime import datetime


def is_character(key):
    if " " in key:
        return False
    return True


def get_row_only(items, indx):
    content = []
    for item in items:
        content.append(item[indx])
    return content


def get_frequencies(content):
    frequencies = {}
    for item in content:
        if item not in frequencies.keys():
            frequencies[item] = 1
        else:
            frequencies[item] += 1
    return frequencies


def get_characters(items):
    character_items = []
    for item in items:
        if is_character(item[1]):
            character_items.append(item)
    return character_items


def get_substring(items, delimiter):
    words = []
    current_word = ""
    date_start = None
    for item in items:
        if is_character(item[1]) and not (delimiter in item[1]):
            current_word += item[1]
            if date_start is None:
                date_start = item[0]
        else:
            if not current_word.isspace() and date_start is not None:
                time_spent = (item[0] - date_start).total_seconds()
                words.append([time_spent, current_word])
                current_word = ""
                date_start = None
    return words


def main():
    log = open('keys.txt', 'r')
    lines = log.readlines()
    lines_clean = []
    content_clean = []

    count = 0
    # strip newline character
    for line in lines:
        items = line.strip().split(" --- ", 2)
        datetime_object = datetime.strptime(items[0], '%Y-%m-%d %H:%M:%S,%f')
        content_clean.append([datetime.strptime(items[0], '%Y-%m-%d %H:%M:%S,%f'), items[1]])
        # print("Line: {}, Date: {}, Content: {} is_Ascii={}".format(count, content_clean[count][0], content_clean[count][1], is_character(content_clean[count][1])))
        count = count + 1

    characters = get_frequencies(get_row_only(get_characters(content_clean), 1))
    print(characters["[Back]"])


# words = get_substring(content_clean, "[Return]")
# for word in words:
#	print(word[0], word[1])

if __name__ == "__main__":
    main()
# print(datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f'))
