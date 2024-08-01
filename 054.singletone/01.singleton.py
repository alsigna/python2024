class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        # else: #! не удалять, иначе init будет вызываться каждый раз
        #     cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


class Watchdog(metaclass=Singleton):
    def __init__(self, threshold: int = 5) -> None:
        self.fails = 0
        self.threshold = threshold

    def __repr__(self) -> str:
        return f"<WD: threshold={self.threshold}>"


wd1 = Watchdog(threshold=10)
wd2 = Watchdog(threshold=20)

print(id(wd1) == id(wd2))
