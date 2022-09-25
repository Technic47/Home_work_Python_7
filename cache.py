import glob
import os


def delete():
    for file in glob.glob('cache/*'):
        os.remove(file)
