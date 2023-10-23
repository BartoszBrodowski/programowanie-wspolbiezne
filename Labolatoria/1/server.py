import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
 

# Specjalny handler, który rozszerza klasę FileSystemEventHandler i zmienia 
# metodę on_modified tak aby obserwowała tylko plik text.txt
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("input.txt"):
            input = open("input.txt", 'r')
            output = open('output.txt', 'w')
            value = input.readline()
            int_value = int(value)
            new_value = int_value * 2
            output.write(str(new_value))
            input.close()
            output.close()
            time.sleep(1)

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
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()