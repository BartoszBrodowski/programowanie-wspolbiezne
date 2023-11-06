import os
import time
import re
from multiprocessing import Value

def count_word_occurrences(text, word):
    # Case-insensitive regex for finding words
    pattern = re.compile(r'\b{}\b'.format(re.escape(word)), re.IGNORECASE)
    occurrences = len(pattern.findall(text))
    return occurrences

def process_file(file_name, word, shared_value):
    # global total_occurrences
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip().startswith("\\input{"):
                pid = os.fork()
                # Child process
                if pid == 0:
                    included_file_name = line.strip()[7:-1]
                    process_file(included_file_name, word)
                    os._exit(shared_value)
                else:
                    _, status = os.wait()
            else:
                print(line)
                occurences = count_word_occurrences(line, word)
                print(occurences)
                shared_value.value += occurences

def main(filename, word):
    total_occurrences = Value(word, 0)
    process_file(filename, word, total_occurrences)
    print(f"Total occurrences of '{word}' in '{filename}' and included files: {total_occurrences.value}")

if __name__ == '__main__':
    filename = "plikA.txt"
    word = "i"

    main(filename, word)