import os
import re

total_occurrences = 0

def count_word_occurrences(text, word):
    # Case-insensitive regex for finding words
    pattern = re.compile(r'\b{}\b'.format(re.escape(word)), re.IGNORECASE)
    occurrences = len(pattern.findall(text))
    return occurrences

def process_file(filename, word):
    global total_occurrences
    with open(filename, 'r') as file:
        for line in file:
            if line.strip().startswith("\\input{"):
                included_filename = line.strip()[7:-1]
                pid = os.fork()
                if pid == 0:
                    with open(included_filename, 'r') as included_file:
                        print('Enter file')
                        text = included_file.read()
                    occurrences = count_word_occurrences(text, word)
                    total_occurrences += occurrences
                    os._exit(occurrences)
                else:
                    process_file(included_filename, word)
                    # Wait so the result is in proper order (print not happening too early)
                    _, status = os.wait()
            else:
                total_occurrences += count_word_occurrences(line, word)

    return total_occurrences

def main(filename, word):
    total_occurrences = process_file(filename, word)
    print(f"Total occurrences of '{word}' in '{filename}' and included files: {total_occurrences}")

if __name__ == '__main__':
    filename = "plikA.txt"
    word = "z"

    main(filename, word)
