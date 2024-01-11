import threading
import math

starting_boundary = 2
ending_boundary = 20
num_threads = 3

def pierwsza(number):
    squareroot_number = math.ceil(math.sqrt(number))
    # There's no bigger divider of the number than it's square root
    for i in range(2, squareroot_number+1):
        if number % i == 0:
            return False
    return True

def thread_calculations(start, end, results, barrier, lock):
    local_results = []
    for num in range(start, end + 1):
        if pierwsza(num):
            local_results.append(num)
    with lock:
        results.extend(local_results)
    print(f"Thread finished calculations in range {start}-{end}")
    barrier.wait()
    print(f"Thread finished waiting after barrier in range {start}-{end}")



def initialize_threads(global_results, chunk_size, threads, barrier, lock):
    for i in range(num_threads):
        start = starting_boundary + i * chunk_size
        end = start + chunk_size - 1 if i < num_threads - 1 else ending_boundary
        thread = threading.Thread(target=thread_calculations, args=(start, end, global_results, barrier, lock))
        threads.append(thread)
        thread.start()


def main():
    threads = []
    chunk_size = (ending_boundary - starting_boundary + 1) // num_threads
    global_results = []
    barrier = threading.Barrier(num_threads + 1)
    lock = threading.Lock()

    initialize_threads(global_results, chunk_size, threads, barrier, lock)
    print("Waiting for threads to finish calculations")
    barrier.wait()

    print("Results:")
    print(global_results)

if __name__ == '__main__':
    main()