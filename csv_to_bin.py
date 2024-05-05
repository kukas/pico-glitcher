import os
filename = "data_final.csv"
with open(filename) as fin, open(f"{filename}.bin", "wb") as fout:
    for line in fin:
        _, byte = line.split(",")
        fout.write(int(byte).to_bytes(1, "big"))