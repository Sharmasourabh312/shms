import os

import mysql.connector as my
from traceback import format_exc
from datetime import datetime

from mysql.connector import DatabaseError


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
        print(binaryData)
    return binaryData

class dbmodel:
    def __init__(self):
        self.dbstatus=False
        self.conn = None
        self.cur = None
    
    def db_status(self):
        return self.dbstatus

    def close_db(self):
        try:
            if self.dbstatus:
                self.conn.close()
                self.dbstatus=False 
        except DatabaseError:
            print(format_exc())

    def open_db(self):
        try:
            # host='localhost',user='root',password='',database='shmsdata'
            self.conn = my.connect(host='localhost',user='heal',password='heal',database='healthy')
            self.cur = self.conn.cursor()
            db_status=True
        except DatabaseError:
            print("Some error ocure")
        
    def save_data(self,**d):
        status =None
        today = datetime.now()
        day = today.strftime("%m/%d/%Y")
        time = today.strftime("%I:%M %p")
        path = os.getcwd()
        str = path + "\manitecg.png"
        ptecg = convertToBinaryData(str)
        insert_blob_tuple = (ptecg)

        try:
            self.open_db()
            self.cur.execute('INSERT INTO health(id,temp,bp,bs,pr,ECG,day,Time)Values(%s,%s,%s,%s,%s,%s,%s,%s)',(d["adh"],d["temp"],d["bp"],d["bs"],d["pr"],insert_blob_tuple,day,time))
            self.conn.commit()
        except Exception:
            print(format_exc())

        else:
            status = 1
        finally:
            self.close_db()
            self.dbstatus = False
            return status
    def get_data(self,adh):
        if not self.dbstatus:
            self.open_db()
        try:
            self.cur.execute(
                "select id,temp,bp,bs,pr,day,time,ecg from health where ID = %s", (adh,))
        except Exception as e:
            print(e)
        finally:
            self.close_db()
            return self.cur.fetchall()

    def sign_up(self,Id,Name,contact,adress,dob):
        if not self.dbstatus:
            self.open_db()
        self.cur.execute("INSERT INTO user_data(id,Name,contact,address,date)Values(%s,%s,%s,%s,%s)",(Id,Name,contact,adress,dob))
        self.conn.commit()
        if self.dbstatus:
            self.close_db()

    def login_by_adh(self,adh):
        if not self.dbstatus:
            self.open_db()
        self.cur.execute("select id from user_data where ID = %s", (adh,))
        return self.cur.fetchone()

