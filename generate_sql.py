import csv
import pymysql
import re

import config

from utils import (
    getPinyin,
    cleanField,
)

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
    exc_sql()