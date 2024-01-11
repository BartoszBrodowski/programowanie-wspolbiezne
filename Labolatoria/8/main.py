import threading

def sum_half_list(lst, start, end, result, lock):
    partial_sum = sum(lst[start:end])
    with lock:
        result.append(partial_sum)

def main():
    big_list = list(range(1, 1000001))

    result = []
    lock = threading.Lock()

    mid = len(big_list) // 2
    thread1 = threading.Thread(target=sum_half_list, args=(big_list, 0, mid, result, lock))
    thread2 = threading.Thread(target=sum_half_list, args=(big_list, mid, len(big_list), result, lock))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    total_sum = sum(result)
    print("Sum of all elements: ", total_sum)

if __name__ == "__main__":
    main()
