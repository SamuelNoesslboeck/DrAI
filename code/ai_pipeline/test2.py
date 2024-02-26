import os

dirs = os.listdir()

for dir in dirs:
    for _, _, files in "./" + dir:
        for file in files:
            if file.endswith( ".py" ):
                