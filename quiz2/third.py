import time
import random
from threading import Thread
from threading import BoundedSemaphore


# Семафоры для ограничения количества одновременных потоков
get_data_semaphore = BoundedSemaphore(10)
write_to_file_semaphore = BoundedSemaphore(5)
write_to_console_semaphore = BoundedSemaphore(1)


# Декоратор-обертка для применения семафоров
def semaphore_wrapper_maker(semaphore):
    def semaphore_wrapper(f):
        def wrapper(task_id):
            semaphore.acquire()
            f(task_id)
            semaphore.release()
        return wrapper
    return semaphore_wrapper


@semaphore_wrapper_maker(get_data_semaphore)
def get_data(task_id):
    print(f"processing get_data({task_id})")
    time.sleep(random.randint(1, 3))
    print(f"completed get_data({task_id})")


@semaphore_wrapper_maker(write_to_file_semaphore)
def write_to_file(task_id):
    print(f"processing write_to_file({task_id})")
    time.sleep(random.randint(1, 5))
    print(f"completed write_to_file({task_id})")


@semaphore_wrapper_maker(write_to_console_semaphore)
def write_to_console(task_id):
    print(f"processing write_to_console({task_id})")
    time.sleep(random.randint(1, 5))
    print(f"completed write_to_console({task_id})")


def handle_task(task_id):
    # 1. Выполняем get_data()
    # 2. Параллельно выполняем write_to_file() и write_to_console()

    get_data(task_id)
    to_file = Thread(target=write_to_file, args=(task_id,))
    to_console = Thread(target=write_to_console, args=(task_id,))

    to_file.start()
    to_console.start()

    to_file.join()
    to_console.join()


if __name__ == '__main__':
    # Параллельно обрабатываем каждый task_id
    threads = [Thread(target=handle_task, args=(task_id,)) for task_id in range(1, 21)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
