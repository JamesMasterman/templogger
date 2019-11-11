#!/usr/bin/python
import sqlite3
from sqlite3 import Error
from datetime import datetime

 
def create_connection():
	database = "temperaturelog.db"
	try:
		conn = sqlite3.connect(database)
		return conn
	except Exception as e:
		print(e)

	return None
	
def insertAirTempHumid(nowStr,temp, humidity):
	conn = create_connection();
	conn.isolation_level = None
	try:
		cursor = conn.cursor()
		sql = "INSERT INTO air_temperature(when_recorded, humidity, temperature) VALUES(?,?,?)"
		values = (nowStr, humidity, temp)
		cursor.execute(sql, values)
		conn.close()
	
	except Exception as error:
		print("DB insert failed with error ", error)
	
	return
	
def insertPh(nowStr, pH):
	conn = create_connection();
	conn.isolation_level = None
	try:
		cursor = conn.cursor()
		sql = "INSERT INTO ph(when_recorded, pH) VALUES(?,?)"
		values = (nowStr, pH)
		cursor.execute(sql, values)
		conn.close()
	
	except Exception as error:
		print("DB insert failed with error ", error)
	
	return
	
def insertLiquidTemp(nowStr, tank, temp):
	conn = create_connection();
	conn.isolation_level = None
	try:
		cursor = conn.cursor()
		sql = "INSERT INTO tank_temperature(when_recorded, tank, temperature) VALUES(?,?,?)"	
		values = (nowStr, tank, temp)
		cursor.execute(sql, values)
		conn.close()
	except Exception as error:
		print("DB insert failed with error ", error)
	
	return
 


 
