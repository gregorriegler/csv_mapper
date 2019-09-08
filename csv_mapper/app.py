from io import StringIO
import sys
import csv


def load_csv(text):
    reader = csv.reader(StringIO(text), delimiter=',')
    return list(reader)


def load_csv_from_file(filename):
    with open(filename, mode='r', encoding='utf-8-sig', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        return list(reader)


def write_csv_to_string(content):
    output = StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    for row in content:
        writer.writerow(row)
    return output.getvalue()


def write_csv(content, destination_file):
    with open(destination_file, 'w', newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for row in content:
            writer.writerow(row)


def apply_rule(content, rule):
    column = int(rule[0])
    mode = rule[1].lower()
    pattern = rule[2]
    replacement = rule[3]

    for row_number, row in enumerate(content):
        if row_number == 0 and mode != 'delete_column':
            continue

        if mode == 'replace_column':
            replace_column(row, column, pattern, replacement)

        elif mode == 'replace_word':
            replace_word(row, column, pattern, replacement)

        elif mode == 'delete_column':
            delete_column(row, column, pattern, replacement)

        else:
            raise NameError('Unknown mode!')


def replace_word(row, column, pattern, replacement):
    word_array = row[column].lower().replace(',', '').split(' ')
    words_to_replace_with = pattern.lower().split(' ')
    for word_number, word in enumerate(word_array):
        if len(words_to_replace_with) > 1:
            raise TypeError('Argument should be string not an array in mode: replace_word')

        if word == words_to_replace_with[0]:
            word_array[word_number] = replacement
    separator = " "
    row[column] = separator.join(word_array)


def replace_column(row, column, pattern, replacement):
    word_array = row[column].lower().replace(',', '').split(' ')
    words_to_replace_with = pattern.lower().split(' ')
    for word in word_array:
        if word in words_to_replace_with:
            words_to_replace_with.remove(word)
        if not words_to_replace_with:
            row[column] = replacement
            break


def delete_column(row, column, pattern, replacement):
    del row[column]


def map_content(content, rules):
    for rule_number, rule in enumerate(rules):
        try:
            apply_rule(content, rule)
        except Exception as e:
            print('Error[rule file] in line: {} -> {}'.format(rule_number + 1, e))
            continue
    return content


def main(args):
    src_file = load_csv_from_file(args[1])
    rules_file = load_csv_from_file(args[2])
    content = map_content(src_file, rules_file)

    if len(sys.argv) == 3:
        sys.stdout.write(write_csv_to_string(content))
    elif len(sys.argv) == 4:
        write_csv(content, args[3])
    else:
        raise Exception('Invalid Argument Count')


if __name__ == '__main__':
    main(sys.argv)
