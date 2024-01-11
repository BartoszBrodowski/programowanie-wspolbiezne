import threading

def sum_partial_list(lst, start, end, result, lock):
    partial_sum = sum(lst[start:end])
    with lock:
        result.append(partial_sum)

def main():
    big_list = list(range(1, 1000001))

    result = []
    lock = threading.Lock()

    num_threads = 4

    chunk_size = len(big_list) // num_threads
    print('Chunk size: ', chunk_size)

    threads = []

    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_threads - 1 else len(big_list)
        thread = threading.Thread(target=sum_partial_list, args=(big_list, start, end, result, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(result)
    print("Sum of all elements:", total_sum)

if __name__ == "__main__":
    main()
