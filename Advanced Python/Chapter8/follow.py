import os
import time
def follow(file_path):
    try:
        with open(file_path,'r') as f:
            f.seek(0,os.SEEK_END)
            while True:
                line = f.readline()
                if line=='':
                    time.sleep(0.1)
                    continue
                yield line
    except GeneratorExit:
        print('Following Done')
