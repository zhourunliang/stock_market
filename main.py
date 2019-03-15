import urllib.request as urlrequest,os
import time
import csv
import pymysql
import re

import config

def single_get_first(unicode1):
    str1 = unicode1.encode('gbk')
    try:
        ord(str1)
        return str1.decode('gbk')
    except:
        asc = str1[0] * 256 + str1[1] - 65536
        if asc >= -20319 and asc <= -20284:
            return 'a'
        if asc >= -20283 and asc <= -19776:
            return 'b'
        if asc >= -19775 and asc <= -19219:
            return 'c'
        if asc >= -19218 and asc <= -18711:
            return 'd'
        if asc >= -18710 and asc <= -18527:
            return 'e'
        if asc >= -18526 and asc <= -18240:
            return 'f'
        if asc >= -18239 and asc <= -17923:
            return 'g'
        if asc >= -17922 and asc <= -17418:
            return 'h'
        if asc >= -17417 and asc <= -16475:
            return 'j'
        if asc >= -16474 and asc <= -16213:
            return 'k'
        if asc >= -16212 and asc <= -15641:
            return 'l'
        if asc >= -15640 and asc <= -15166:
            return 'm'
        if asc >= -15165 and asc <= -14923:
            return 'n'
        if asc >= -14922 and asc <= -14915:
            return 'o'
        if asc >= -14914 and asc <= -14631:
            return 'p'
        if asc >= -14630 and asc <= -14150:
            return 'q'
        if asc >= -14149 and asc <= -14091:
            return 'r'
        if asc >= -14090 and asc <= -13119:
            return 's'
        if asc >= -13118 and asc <= -12839:
            return 't'
        if asc >= -12838 and asc <= -12557:
            return 'w'
        if asc >= -12556 and asc <= -11848:
            return 'x'
        if asc >= -11847 and asc <= -11056:
            return 'y'
        if asc >= -11055 and asc <= -10247:
            return 'z'
        return ''


def getPinyin(string):
    if string == None:
        return None
    lst = list(string)
    charLst = []
    for l in lst:
        charLst.append(single_get_first(l))
    return ''.join(charLst)

def cleanField(string):
    return re.sub('[^\w]', '',string)

# ROE = 归属于母公司所有者的净利润/归属于母公司股东权益合计

def download(code='000725'):

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


def create_tab_sql(code='000725', type='lrb'):
    '''
    生成表语句
    '''
    file = 'download\\{}\\{}.csv'.format(type, code)
    with open(file, 'r') as f:  
        reader = csv.reader(f)
        fields = []
        fields_pinyin = []
        for row in reader:
            # print(len(row))
            if len(row) > 1:
                fields.append(row[0])
                py_name = cleanField(getPinyin(row[0]))
                if py_name in fields_pinyin:
                    fields_pinyin.append('{}_2'.format(py_name))
                else:
                    fields_pinyin.append(py_name)
                
        # print(fields)
        # print(fields_pinyin)
        sql = "CREATE TABLE `{}` (".format(type)
        sql += "`id` int(11) unsigned NOT NULL AUTO_INCREMENT,"
        sql += "`code` varchar(24) DEFAULT '' COMMENT '{}',".format(code)
        for k in range(len(fields)):
            sql += "`{}` varchar(24) DEFAULT '' COMMENT '{}',".format(fields_pinyin[k], fields[k])
        sql += "PRIMARY KEY (`id`)"
        sql += ") ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4; "
        # print(sql)
        return sql
    return False

def insert_tab_sql(code='000725', type='lrb'):
    '''
    生成表插入语句
    '''
    file = 'download\\{}\\{}.csv'.format(type, code)
    
    with open(file, mode='r') as f:  
        reader = csv.reader(f)
        fields = []
        fields_pinyin = []
        csv_list = []
        for c_row in reader:
            if len(c_row) > 1:
                fields.append(str(c_row[0]))
                py_name = cleanField(getPinyin(c_row[0]))
                if py_name in fields_pinyin:
                    fields_pinyin.append('{}_2'.format(py_name))
                else:
                    fields_pinyin.append(py_name)

                csv_list.append(c_row)
        # print(csv_list)

        row_len = len(csv_list)
        # print('row_len={}'.format(row_len))

        col_len = len(csv_list[0])-1
        # print('col_len={}'.format(col_len))

        # print(csv_list[row_len-1][col_len-2])

        new_list = []
        for i in range(1, col_len):
            # print(i)
            line = []
            for j in range(0, row_len):
                line.append(csv_list[j][i])
            # print(line)
            new_list.append(line)
        # print(new_list)
        # print(fields)

        sql  = 'INSERT INTO {}  ('.format(type)
        sql += '`code`,'
        for i in range(len(fields_pinyin)):
            if i is not len(fields_pinyin)-1:
                sql += '`{}`,'.format(fields_pinyin[i])
            else:
                sql += '`{}`'.format(fields_pinyin[i])
        sql += ')  VALUES'  

        for i in range(len(new_list)):
            sql += '("{}",'.format(code)
            for j in range(len(new_list[i])):
                if j is not len(new_list[i])-1:
                    sql += '"{}",'.format(new_list[i][j])
                else:
                    sql += '"{}"'.format(new_list[i][j])
            if i is not len(new_list)-1:
                sql += '),'
            else:
                sql += ')'
        # print(sql)
        return sql
    return False



def exc_sql(code='000725'):
    '''
    执行SQL语语句
    '''
    conn = pymysql.connect(host='127.0.0.1',user='root', passwd='123456', db='mysql', charset='utf8')
    cur = conn.cursor()
    cur.execute("USE stock")
    
    # 利润表
    sql = create_tab_sql('000725', 'lrb')
    cur.execute(sql)
    conn.commit()

    sql = insert_tab_sql('000725', 'lrb')
    cur.execute(sql)
    conn.commit()

    # 现金流量表
    sql = create_tab_sql('000725', 'xjllb')
    cur.execute(sql)
    conn.commit()

    sql = insert_tab_sql('000725', 'xjllb')
    cur.execute(sql)
    conn.commit()

    # 资产负债表
    sql = create_tab_sql('000725', 'zcfzb')
    cur.execute(sql)
    conn.commit()

    sql = insert_tab_sql('000725', 'zcfzb')
    cur.execute(sql)
    conn.commit()
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    # download()
    # create_tab_sql('000725', 'xjllb')
    exc_sql()

