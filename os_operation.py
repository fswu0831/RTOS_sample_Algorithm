import os
import pandas as pd
import re

def save_file(RESULTS_FILE_NAME,results_path,table1,table2):
    RESULTS_FILE_NAME=RESULTS_FILE_NAME.split('.')[0]
    results_files=os.listdir(results_path)
    results_files=[s for s in results_files if s.startswith(RESULTS_FILE_NAME)]
    if results_files:
        RESULTS_FILE_NAME=RESULTS_FILE_NAME+'('+str(len(results_files)/2)+')'
    table1.to_csv(results_path+RESULTS_FILE_NAME+'-pre.csv',encoding='cp932')
    table2.to_csv(results_path+RESULTS_FILE_NAME+'-new.csv',encoding='cp932')
    

def get_files(path):
    files=os.listdir(path)
    send_files=[s for s in files if s.endswith('csv') and s.startswith('s')]
    recv_files=[s for s in files if s.endswith('csv') and s.startswith('r')]
    #send_files=send_files.sort()
    #recv_files=recv_files.sort()
    return {'send_files':send_files,'recv_files':recv_files}