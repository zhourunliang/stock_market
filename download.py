import urllib.request as urlrequest,os
import time

import config

def download(code='000725'):
    '''
    下载文件
    '''
    print('正在下载#{}的资产负债表'.format(code))
    zcfzb_url = '{}{}.html?type=year'.format(config.download_pre_url_zcfzb, code)
    if not os.path.exists(config.save_folder_zcfzb):
        os.makedirs(config.save_folder_zcfzb)
    os.chdir(config.save_folder_zcfzb)
    urlrequest.urlretrieve(zcfzb_url,'{}.csv'.format(code))
    print("资产负债表下载完毕")
    time.sleep(3)

    print("正在下载#{}的利润表".format(code)) 
    lrb_url = '{}{}.html?type=year'.format(config.download_pre_url_lrb, code)
    if not os.path.exists(config.save_folder_lrb):
        os.makedirs(config.save_folder_lrb)
    os.chdir(config.save_folder_lrb)
    urlrequest.urlretrieve(lrb_url,'{}.csv'.format(code))
    print("利润表下载完毕")
    time.sleep(3)

    print("正在下载#{}的现金流量表".format(code))
    xjllb_url = '{}{}.html?type=year'.format(config.download_pre_url_xjllb, code)
    if not os.path.exists(config.save_folder_xjllb):
        os.makedirs(config.save_folder_xjllb)
    os.chdir(config.save_folder_xjllb)
    urlrequest.urlretrieve(xjllb_url,'{}.csv'.format(code))
    print("现金流量表下载完毕")
    time.sleep(3)

if __name__ == '__main__':
    download()