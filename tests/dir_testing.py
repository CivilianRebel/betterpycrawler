import os
import pathlib

p = pathlib.Path('../crawler_files')
for dir in p.glob('*'):
    print(str(dir))