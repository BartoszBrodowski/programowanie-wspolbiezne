import os
import time

TEXT_END_SIGN = '$'
open('bufor.txt', 'a')
initial_metadata = os.stat('bufor.txt')

lockfile = os.path.isfile('temp/lockfile.txt')
if lockfile:
    os.remove('temp/lockfile.txt')

print('Server listening')
while True:
    try:
        current_metadata = os.stat('bufor.txt')
        # Check modification time and file size
        if current_metadata.st_mtime != initial_metadata.st_mtime or current_metadata.st_size != initial_metadata.st_size:
            with open('bufor.txt', 'r+') as bufor:
                output_file = bufor.readline().strip()
                elements = [line.split() for line in bufor.readlines()]
                elements_flattened = [item.replace(TEXT_END_SIGN, '') for sublist in elements for item in sublist if item != TEXT_END_SIGN]
                print(' '.join(elements_flattened))
                new_text = input('Provide new text: ')

                with open(output_file, 'w') as output:
                    output.write(new_text + TEXT_END_SIGN)
                os.remove('temp/lockfile.txt')
            initial_metadata = current_metadata
    except FileNotFoundError:
        print('File not found')
        break
    time.sleep(0.5)

