#Script to load in Siemens .rda files, save to database and do some pretty display/processing

import os, datetime
import subprocess

def call_tarquin(input_path,my_file_name,my_output_path):
    my_file_name_strip = my_file_name.strip('.rda')
    output_dir = os.path.join('output\\',my_file_name_strip+'_'+datetime.datetime.now().strftime('%Y%m%d_%H%M'))
    os.makedirs(output_dir,
                exist_ok=True)
    tarquin_cmd = [r'tarquin\\tarquin\\tarquin.exe',
                   '--input',
                   input_file_path + file_name,
                   '--format','rda',
                   '--output_txt',
                   my_output_path+my_file_name.strip('.rda')+'.txt']
    subprocess.call(tarquin_cmd)
    os.rename("plot.txt",os.join(output_dir,"plot.txt"))
    os.rename("results.txt", os.join(output_dir, "results.txt"))
    os.rename("gnuplot.txt", os.join(output_dir, "gnuplot.txt"))

input_file_path = r'data\\'
output_file_path = r'output\\'

for file_name in os.listdir(input_file_path):
    call_tarquin(input_file_path,file_name,output_file_path)