import threading
import time


def foo(count: int) -> None:
    thr_name = threading.current_thread().name
    for i in range(count):
        print(f"[{thr_name}]: {i}")
        time.sleep(1)


thr1 = threading.Thread(
    target=foo,
    args=(5,),
    name="thr-1",
)

thr2 = threading.Thread(
    target=foo,
    kwargs={"count": 3},
    name="thr-2",
)

thr1.start()
thr2.start()

print("потоки запущены")


print(f"число активных потоков: {threading.active_count()}")
print(f"список всех потоков: {threading.enumerate()}")

main_thr = threading.main_thread()
print(f"имя потока: {main_thr.name}")
print(f"id потока: {main_thr.ident}")
