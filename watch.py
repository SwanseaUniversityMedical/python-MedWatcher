from watchgod.main import watch
from watchgod.watcher import PythonWatcher, Change


def main():
    for changes in watch('./in', watcher_cls=PythonWatcher):
        if(list(changes)[0][0] == Change.added):
            print('new file in')


if __name__ == "__main__":
    main()
