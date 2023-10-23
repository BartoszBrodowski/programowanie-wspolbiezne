import os
import multiprocessing

# Function to count occurrences of a word in a text
def count_word_occurrences(filename, word):
    with open(filename, 'r') as file:
        text = file.read()
    return text.count(word)

# Function to process a file and its included files
def process_file(filename, word):
    total_occurrences = 0

    def search_included_files(filename, word):
        nonlocal total_occurrences
        with open(filename, 'r') as file:
            for line in file:
                if line.strip().startswith("\\input{"):
                    included_filename = line.strip()[7:-1]
                    pid = os.fork()
                    if pid == 0:
                        with open(included_filename, 'r') as file:
                            total_occurrences += count_word_occurrences(file, word)
                            os._exit(0)
                    else:
                        os.waitpid(pid, 0)

                else:
                    total_occurrences += line.count(word)

    search_included_files(filename, word)

    return total_occurrences

def main(p, s):
    # Create a multiprocessing pool
    pool = multiprocessing.Pool()

    # Count occurrences in the main file and its included files
    total_occurrences = process_file(p, s)

    # Close the pool
    pool.close()
    pool.join()

    print(f"Total occurrences of '{s}' in '{p}' and included files: {total_occurrences}")

if __name__ == '__main__':
    p = "plikA.txt"  # Replace with the actual file name
    s = "Stoi"  # Replace with the word you want to count

    main(p, s)
