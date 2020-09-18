import sys
import os

path = sys.argv[1]

for filename in os.listdir(path):
    if filename.endswith(".txt") and "old" not in filename:
        with open(os.path.join(path,filename),"r") as f:
            text = f.read()

        # print(text)
        text = text.replace('\\n','\n')
        with open(os.path.join(path,filename),"w") as f:
            f.write(text)