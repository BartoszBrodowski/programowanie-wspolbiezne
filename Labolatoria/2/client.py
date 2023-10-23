import os
import time

filename = input('Provide filename: ')
lockfile_exists = os.path.isfile('temp/lockfile.txt')
while lockfile_exists:
    lockfile_exists = os.path.isfile('temp/lockfile.txt')
    print('Server is busy')
    time.sleep(0.5)
with open(filename, 'r') as input:
    with open('bufor.txt', 'w') as bufor:
        bufor.write(input.read())
        if not lockfile_exists:
            open('temp/lockfile.txt', 'x')