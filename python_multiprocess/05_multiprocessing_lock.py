"""Multiprocessing -- sharing memory with Lock."""
import time
import multiprocessing


def deposit(balance, lock):
    for i in range(100):
        time.sleep(0.01)
        lock.acquire()
        balance.value = balance.value + 1
        lock.release()


def withdraw(balance, lock):
    for i in range(100):
        time.sleep(0.01)
        lock.acquire()
        balance.value = balance.value - 1
        lock.release()


if __name__ == '__main__':
    NUM_RUNS = 20
    profit_values = []
    currency = 'gold bars'
    print('The output should always be 200 {}, because the balance.value gets locked.'.format(currency))
    print('The program will now run {} times...'.format(NUM_RUNS))
    for _ in range(NUM_RUNS):
        balance = multiprocessing.Value('i', 200)
        lock = multiprocessing.Lock()
        d = multiprocessing.Process(target=deposit, args=(balance, lock))
        w = multiprocessing.Process(target=withdraw, args=(balance, lock))

        d.start()
        w.start()

        d.join()
        w.join()

        if balance.value == 200:
            print('balance value is {}'.format(balance.value))
        else:
            off_by = balance.value-200
            profit_values.append(off_by)
            print('balance value is {} (ERROR: your bank account is off by {} {})'.format(balance.value, off_by, currency))
    profit = sum(profit_values)
    assert profit == 0
    print('{} == 0. If there is no error message, and all the results were 200, then it worked.'.format(profit))
