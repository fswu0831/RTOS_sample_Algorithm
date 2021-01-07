import pandas as pd
from tqdm import tqdm
from IPython.display import display
import warnings
import pprint
import time
warnings.simplefilter('ignore')

#ファイルのインポート
import evaluation as ev
import control_structure as cs
import race
import table as tb
import init_table as init
import creating_test as test
import os_operation as _os_

RESULTS_FILE_NAME='sample' #.csvつけない

# インポートする dir
path='data_buffer2/'

# エクスポートする dir
results_path='results_buffer2/'


files=_os_.get_files(path)
send_files=files['send_files']
recv_files=files['recv_files']


heading_results=('Task','Buffer','TestCase','SVAR','Def-Use','Plnv')
heading=('Thread','Port','Event','Index')
pre_results=pd.DataFrame({},columns=heading_results)
new_results=pd.DataFrame({},columns=heading_results)

for file in tqdm(range(len(recv_files))):
    print('-------{}回目-------'.format(file+1))
    RECEIVE_SHEET_NAME=path+recv_files[file]
    SEND_SHEET_NAME=path+send_files[file]
    
    Qs=[pd.DataFrame({})]
    Qr=[pd.DataFrame({})]
    Qr[0]=pd.read_csv(RECEIVE_SHEET_NAME,names=heading)
    Qs[0]=pd.read_csv(SEND_SHEET_NAME,names=heading)
    init.delete_diff(Qr,Qs)
    Qr[0]=init.init(Qr[0],'r')
    Qs[0]=init.init(Qs[0],'s')
    df_unique=init.append_unique(Qr,Qs)
    Qr_unique=df_unique['Qr']
    Qs_unique=df_unique['Qs']

    for way in range(2):
        if way==0:
            t_way=2
            combination=0 #0の場合は既存研究の方法、1の場合は組み合わせを考慮した手法
            ev_table=pre_results
        elif way==1:
            t_way=2
            combination=1
            ev_table=new_results
            Qr=Qr[:1]
            Qs=Qs[:1]
        else:
            print('プログラムを終了します') # shoudn't reach here
            break


        number=0 # 実験の回数
        check_digit=0

        race_set={}


        start = time.time()
        print("Creating race set",end='')
        race_set=race.creating_race_set(Qr,Qs,Qs_unique,race_set,combination)
        elapsed_time = time.time() - start
        print ("\nCreating race set took:{:.4g}".format(elapsed_time) + "[sec]")
        #pprint.pprint((race_set))


        start = time.time()
        print("Creating race table",end='')
        table=tb.construct_race_table(Qs,Qr,race_set,t_way)
        if t_way>1:
            table=tb.expand_table(Qr,Qs,race_set,table,t_way)
        elapsed_time = time.time() - start
        print ("\nCreating race table took:{:.4g}".format(elapsed_time) + "[sec]")
        table=table.astype('int64')

        check_digit=1

        start = time.time()
        results=test.create_new_testcase(number,check_digit,Qr,Qs,table,race_set,Qr_unique,Qs_unique)
        Qr=results['recv']
        Qs=results['send']
        elapsed_time = time.time() - start
        print ("Creating test case took:{:.4g}".format(elapsed_time) + "[sec]")
        print('The number of Test Case is {}.'.format(len(table)))


        evaluation=ev.evaluate(Qr,Qs)
        Q=pd.concat([Qs[0],Qr[0]]).sort_index()
        
        if way==0:
            pre_results=pre_results.append(evaluation,ignore_index=True)
        elif way==1:
            new_results=new_results.append(evaluation,ignore_index=True)
        else:
            print('error')
        
_os_.save_file(RESULTS_FILE_NAME,results_path,pre_results,new_results)
