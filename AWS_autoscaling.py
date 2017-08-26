from random import randrange

from flask import Flask, render_template, request
import time
import pymysql
import os
import hashlib
import memcache
from flask import Flask, render_template

app = Flask(__name__)

def connection():
    conn = pymysql.connect(host= ,
                           port= ,
                           user= ,
                           password= ,
                           db= ,
                           local_infile=True
                           )
    return conn

def createtable():
    start_time = time.time()
    print("in create table")
    conn = connection()
    cur = conn.cursor()
    cur.execute('drop table if exists Classes')
    conn.commit()

    query = """CREATE TABLE Classes (
                    `Major` VARCHAR(4) CHARACTER SET utf8,
                    `Course` INT,
                    `Section` INT,
                    `Course_Title` VARCHAR(31) CHARACTER SET utf8,
                    `Instructor` VARCHAR(12) CHARACTER SET utf8,
                    `Day_s` VARCHAR(4) CHARACTER SET utf8,
                    `Start_time` VARCHAR(8) CHARACTER SET utf8,
                    `End_Time` VARCHAR(8) CHARACTER SET utf8,
                    `Max` INT,
                    `Enrolled` INT
                );"""
    print("hi")
    cur.execute(query)
    load_file = app.root_path + '/classes.csv'
    query = """ LOAD DATA LOCAL INFILE '/home/ubuntu/quiz7/Classes.csv' INTO TABLE
                   Classes FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED
                   BY '"' Lines terminated by '\r\n' IGNORE 1 LINES """
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()
    end_time = time.time()
    print(end_time - start_time)
    return "hi done"

@app.route('/result', methods=['POST', 'GET'])
def dbcount():
    print('hi')
    display = []
    if request.method == 'GET':
        mytext = request.args.get('text1','')
        mytext1 = request.args.get('text2','')
        conn = connection()
        print(mytext)
        cur = conn.cursor()
        quer = 'select count(*) from Classes'
        cur.execute(quer)
        res = cur.fetchall()
        print(res[0])
        conn.commit()
        cur.close()
        conn.close()
    return render_template('result.html')



@app.route('/')
def hello_world():
    dbcount()
    #createtable()

    return render_template('main.html')

port = os.getenv('PORT', '80')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(port))