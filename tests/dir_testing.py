import glob

for d in glob.glob('../crawler_files/*'):
    print(type(d))