#!/usr/bin/python

import socket
import time
import sys
import re
from datetime import datetime
from TempDB import insertAirTempHumid
from TempDB import insertLiquidTemp
from TempDB import insertPh
from DHT22Reader import readAirTemperatureHumidity
from TankTemperatureReader import readTankTemperature
from TankTemperatureReader import initTankTemp
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PhProbe import AtlasI2C

TANK = 1
xs = []
air_ys= []
humd_ys=[]
tank_ys=[]
ph_ys=[]
fig, ax = plt.subplots(4)

tankTemp=0
airHumid = 0
airTemp = 0
pH = 0
phProbe = AtlasI2C()

def animate(i, xs, air_ys, humd_ys, tank_ys, ph_ys):
			
	try:				
		now = datetime.now()
		tankTemp = readTankTemperature()
		currentHumid, currentTemp = readAirTemperatureHumidity()
		if currentHumid is not None:
			airHumid = currentHumid
			
		if currentTemp is not None:
			airTemp = currentTemp
			 		
		pHStr = phProbe.query("R")
		pHReading = re.findall('\d*\.?\d+',pHStr)
		pH = float(pHReading[0])
		nowStr = now.strftime("%Y-%m-%d %H:%M:%S")
		
		#Log the current state
		insertAirTempHumid(nowStr, airTemp, airHumid)
		insertPh(nowStr, pH)
		insertLiquidTemp(nowStr, TANK, tankTemp)
		
		#report 	
		print("Last reading: " + nowStr)
		print("Air Temp = {0:0.1f}C, Humidity = {1:0.1f}%".format(airTemp, airHumid))
		print("Tank Temp = {0:0.1f}C".format(tankTemp))
		print("pH = {0:0.2f}".format(pH))
		print("----------------------------------------------")
			
		#plot
		xs.append(datetime.now())
		air_ys.append(airTemp)
		humd_ys.append(airHumid)
		tank_ys.append(tankTemp)
		ph_ys.append(pH)
		
		xs = xs[-10000:]
		air_ys = air_ys[-10000:]
		humd_ys = humd_ys[-10000:]
		tank_ys = tank_ys[-10000:]
		ph_ys = ph_ys[-10000:]
		
		ax[0].clear()
		ax[0].plot(xs, air_ys)
		ax[1].clear()
		ax[1].plot(xs, humd_ys)
		ax[2].clear()
		ax[2].plot(xs, tank_ys)
		ax[3].clear()
		ax[3].plot(xs, ph_ys)
		
		plt.xticks(rotation=0, ha='right')
		plt.subplots_adjust(bottom=0.1)
		plt.title("Log")
		ax.flat[0].set(ylabel= "Air (C)")
		ax.flat[1].set(ylabel ="Humid (%)")
		ax.flat[2].set(ylabel="Tank (C)")
		ax.flat[3].set(ylabel="pH")
		print(phProbe.query("T," + str(tankTemp)))
		
	except Exception as error: 
		now = datetime.now()
		print("Error...", error, now.strftime("%Y-%m-%d %H:%M:%S"))
		sys.stdout.flush()						
					

UPDATE_INTERVAL_MS = 300000 #5 mins	
	

def main():
	#-- Main temp logger server 
	try:	
		print("Starting up logger")	
		initTankTemp()		
		ani = animation.FuncAnimation(fig, animate, fargs=(xs, air_ys, humd_ys, tank_ys, ph_ys), interval = UPDATE_INTERVAL_MS)
		plt.show()
		
	except Exception as error:
		print(error)	
		sys.stdout.flush()	
			
if __name__ == '__main__':
	main()
	
