from io import StringIO
import sys
import csv


def load_csv(text):
    reader = csv.reader(StringIO(text), delimiter=',')
    return list(reader)


def load_csv_from_file(filename):
    with open(filename, mode = 'r', encoding = 'utf-8-sig', newline = '') as csv_file:
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
    mode = rule[3].lower()
    
    for row_number, row in enumerate(content):
        if row_number == 0: continue
        #replace ',' with ' ' from content regardless of the outcome
        content[row_number][column].replace(',', '')
        #split column into a lower case word array without(whitespace as delimiter)
        word_array = row[column].lower().replace(',','').split(' ')

        wordsToReplaceWith = rule[1].lower().split(' ')

        if mode == 'replace_column':
            for word in word_array:
                if word in wordsToReplaceWith: wordsToReplaceWith.remove(word)
                if not wordsToReplaceWith:
                    content[row_number][column] = rule[2]
                    break

        elif mode == 'replace_word':
            for word_number, word in enumerate(word_array):
                if len(wordsToReplaceWith) > 1:
                    raise TypeError('Argument should be string not an array in mode: {}'.format(mode))

                if word == wordsToReplaceWith[0]:
                    word_array[word_number] = rule[2]

            seperator = " "
            content[row_number][column] = seperator.join(word_array)
        else:
            raise NameError('Unkown mode!')


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

    print(len(sys.argv))
    if len(sys.argv) == 3:
        sys.stdout.write(write_csv_to_string(content))
    elif len(sys.argv) == 4:
        write_csv(content, args[3])
    else:
        raise Exception('Invalid Argument Count')

if __name__ == '__main__':
    main(sys.argv)