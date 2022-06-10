import os
from src.decrypt_data import cfusdlog
import csv
from itertools import zip_longest

def write_data(file_name):
    # write data to .csv file

    d = []
    keys = []

    for k, v in logData.items():
        keys.append(k)
        d.append(v)

    export_data = zip_longest(*d, fillvalue = '')
    with open(file_name, 'w', encoding="ISO-8859-1", newline='') as resultFile: 
        wr = csv.writer(resultFile)
        wr.writerow(keys)
        wr.writerows(export_data)

def receive_path_file(file):
    y=os.path.join(root, file)
    return y

def edit_time():

    r = csv.reader(open(n))
    lines = list(r)
    first_value=float(lines[1][0])

    for i in range(1, len(lines)):
        lines[i][0]=float(lines[i][0])
        lines[i][0]=lines[i][0]-first_value

    with open(n,'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(lines)

if __name__ == '__main__':

    # np.set_printoptions(threshold=10000)

    for root, dirs, files in os.walk(os.getcwd()):
        for f in files:
            if f.find("log0")>=0:

                x=receive_path_file(f)
                z=os.path.dirname(x)

                logData = cfusdlog.decode(x)
                logData = logData['fixedFrequency']

                n=str(x+".csv")
                write_data(n)
                edit_time()