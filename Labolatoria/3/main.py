import os
import re


def count_word_occurrences(text, word):
    # Case-insensitive regex for finding words
    pattern = re.compile(r'\b{}\b'.format(re.escape(word)), re.IGNORECASE)
    occurrences = len(pattern.findall(text))
    return occurrences

def count(file_name, word, files_to_check, iteration_number):
    sum = 0
    iteration_number += 1
    with open(file_name, "r") as f:
        text = f.read()
        for line in text.split("\n"):
            if line.strip().startswith("\\input{"):
                files_to_check.append(line[7:-1])
                continue
            sum += count_word_occurrences(line, word)
        # Check if have to go deeper
        if len(files_to_check) == iteration_number:
            return sum
    pid = os.fork()

    if pid > 0:
        # Parent process
        status = os.wait()
        if os.WIFEXITED(status[1]):
            return sum + os.WEXITSTATUS(status[1])
    else:
        # Child process
        os._exit(count(files_to_check[iteration_number], word, files_to_check, iteration_number))

word = 'i'
print(f"Ilość wystąpień słowa '{word}':", count("plikA.txt", word, [], -1))