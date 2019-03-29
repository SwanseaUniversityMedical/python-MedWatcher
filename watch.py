import json
import logging
import os.path
import subprocess

from watchgod.main import watch
from watchgod.watcher import Change, PythonWatcher

logger = logging.getLogger('watch')


def main():
    setEnv()

    for changes in watch('./in', watcher_cls=PythonWatcher):
        # if(list(changes)[0][0] == Change.add):
        if list(changes)[0][0] == Change.modified:
            entrypoint = list(changes)[0][1]

            config = str(entrypoint).replace(
                'medgate_entrypoint.py', 'config.json')
            pyVersion, appName = readConfig(config)

            requirements = str(entrypoint).replace(
                'medgate_entrypoint.py', 'requirements.txt')

            if os.path.exists(requirements):
                pipCmd = 'pip{} install -r {}'.format(pyVersion, requirements)

                if runCommand(pipCmd):
                    pyVersion = '' if pyVersion == 2 else 3
                    pyCmd = 'python{} {}'.format(pyVersion, entrypoint)
                    if runCommand(pyCmd):
                        done(appName, 'done')
                else:
                    done(appName, 'error')
            else:
                done(appName, 'error')
                logger.error('missing requirements for {}'.format(appName))


def done(name, type):
    f = open("./out/{}-{}".format(name, type), "w+")
    f.close()


def readConfig(path):
    with open(path) as json_file:
        data = json.load(json_file)
        return str(data['Env_version'])[0], data['Name']


def runCommand(cmd):
    result = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, universal_newlines=True)
    if result.returncode == 0:
        return True
    else:
        logger.error(result.stderr)
        return False


def setEnv():
    if os.environ.get('INPUT_DIR') is None:
        os.environ['INPUT_DIR'] = './input'

    if os.environ.get('OUTPUT_DIR') is None:
        os.environ['OUTPUT_DIR'] = './output'

    if os.environ.get('WATCH_PATTERN') is None:
        os.environ['WATCH_PATTERN'] = 'medgate_entrypoint.py'


if __name__ == '__main__':
    main()
