import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../decrypt_data'))
import cfusdlog
import csv
from itertools import zip_longest

def write_data(file_name):
    # write data to .csv file

    d = []
    keys = []

    for k, v in log_Data.items():
        keys.append(k)
        d.append(v)

    export_data = zip_longest(*d, fillvalue = '')
    with open(file_name, 'w', encoding="utf-8", newline='') as result_File: 
        wr = csv.writer(result_File)
        wr.writerow(keys)
        wr.writerows(export_data)

def receive_path_file(file):
    return os.path.join(root, file)

def fix_time(dict_log_Data):
    x = dict_log_Data["timestamp"]
    first_value = x[0]
    for n in range(0, len(x)):
        x[n] = x[n] - first_value

if __name__ == '__main__':

    for root, dirs, files in os.walk(os.getcwd()):
        for f in files:
            if f.find("log0")>=0:

                bin_filename = receive_path_file(f)

                log_Data = cfusdlog.decode(bin_filename)
                log_Data = log_Data['fixedFrequency']

                fix_time(log_Data)

                output_csv_filename = str(bin_filename+".csv")
                write_data(output_csv_filename)