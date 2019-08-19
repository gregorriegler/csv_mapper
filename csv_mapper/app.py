import csv
from io import StringIO
import sys


def load_csv(text):
    reader = csv.reader(StringIO(text), delimiter=',')
    return list(reader)


def load_csv_from_file(filename):
    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        return list(reader)


def write_csv(content):
    output = StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    for row in content:
        writer.writerow(row)
    return output.getvalue()


def apply_rule(content, rule):
    column = int(rule[0])
    mode = rule[3]

    for row_number, row in enumerate(content):
        if row_number == 0: continue
        # split column into a word array (takes whitespace as the default delimiter)
        word_array = row[column].split();

        if mode == 'replace_column':
            for word in word_array:
                if word == rule[1]:
                    content[row_number][column] = rule[2]
                    break

        elif mode == 'replace_word':
            seperator = " "
            for word in word_array:
                if word == rule[1]:
                    word = rule[1]
            content[row_number][column] = seperator.join(word_array)




def map_content(content, rules):
    for rule in rules:
        apply_rule(content, rule)
    return content


def main(input_file, rules_file):
    source_file = load_csv_from_file(input_file)
    rules_file = load_csv_from_file(rules_file)
    output = map_content(source_file, rules_file)
    print(write_csv(output))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])