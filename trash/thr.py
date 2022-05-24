from threading import Thread as thrd

__all__ = ['Thr']


# Класс для всего содержимого либы
class Thr:
    # Собственно, декоратор
    def thread(fn):
        def thr(*args, **kwargs):
            thrd(target=fn, args=(*args,), kwargs={**kwargs, }).start()
            pass

        return thr

    pass
# конец файла
