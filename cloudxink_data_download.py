import subprocess
import datetime
import os
import functools
import time
import shutil
from multiprocessing import Pool


def wget_download(url, target_dir):
    command = 'wget -q -P %s %s' % (target_dir, url)
    try:
        return subprocess.call(command, shell=True)
    except Exception as e:
        with open(file_dir + '/' + run_date + '_error.log') as f:
            f.write('error while download %s: %s \n' % (url, e))
            # with open ('/log/')


run_date = str(datetime.date.today())
start_time = datetime.datetime.now()
file_dir = 'cloudxink_sync_log'
check_url = u'http://open.cloudxink.com/mtm/sync.txt'
check_file = 'sync.txt'
last_update_file = 'last_update.txt'
log_file = 'job_log.txt'

if not os.path.exists(file_dir):
    os.mkdir(file_dir)
# if os.path.exists(file_dir + '/' + check_file):
#     print 'delete old check file'
#     os.remove(file_dir + '/' + check_file)
    # time.sleep(5)
# check if need to download
# wget_download(check_url,file_dir)
with open(file_dir + '/' + check_file, 'r') as f:
    new_date = f.readline().strip()  # skip 1st line
    url_list = [url.strip() for url in f]
with open(file_dir + '/' + last_update_file, 'r') as f:
    last_update_date = f.readline().strip()
    print 'last:'+last_update_date
# download
total = len(url_list)
success = 0
fail = 0
retry = 0
print new_date
print last_update_date
if new_date > last_update_date or last_update_date == '':
    p = Pool(processes=5)
    if  os.path.exists(file_dir+'/'+new_date):
        shutil.rmtree(file_dir+'/'+new_date)
    wget_download_dir = functools.partial(wget_download, target_dir=file_dir+'/'+new_date)
    return_code_list = p.map(wget_download_dir, url_list)
    for code in return_code_list:
        if code == 0:
            success += 1
        else:
            fail += 1
    with open(file_dir + '/' + log_file, 'a+') as f:
        f.write('%s,Success,Total %s,Suc %s,Fail %s \n' % (run_date, total, success, fail))
    with open(file_dir + '/' + last_update_file, 'w') as f:
        f.write(new_date + '\n')

else:
    with open(file_dir + '/' + log_file, 'a+') as f:
        f.write(','.join([run_date, 'Success,No New Data\n']))
print 'success ' + str(success)
print 'fail ' + str(fail)
