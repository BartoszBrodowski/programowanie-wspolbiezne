import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
 

# Specjalny handler, który rozszerza klasę FileSystemEventHandler i zmienia 
# metodę on_modified tak aby obserwowała tylko plik text.txt
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("output.txt"):
            output = open('output.txt', 'r')
            result = output.readline()
            print(f'The value is: {result}')

if __name__ == "__main__":
    print('File observer started')
 
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
 
    # Tworzę Handler Eventów zmiany pliku
    event_handler = MyHandler()
 
    observer = Observer()
    # Potrzebujemy wprowadzić event_handler, który jest włączany gdy observer wykryje zmianę
    # Path to ścieżka folderu jaki będzie obserwowany, 
    # domyślnie jeśli nie jest podany mamy '.' czyli aktualny folder
    # Recursive = True, bo chcemy go obserwować rekursywnie, czyli wszystko pod nim
    observer.schedule(event_handler, path, recursive=True)
 
    observer.start()
    running = True
    try:
        while running:
            input_value = input('Input a number: ')
            with open('input.txt', 'w') as input_file:
                value = int(input_value)
                input_file.write(str(value))
            time.sleep(1)
            observer.stop()
            running = False
    except KeyboardInterrupt:
        observer.stop()
    observer.join()