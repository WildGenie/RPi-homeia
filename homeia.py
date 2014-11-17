# -*- coding: utf-8 -*-
from flask import Flask, Markup, flash, render_template, redirect, url_for, jsonify, request
from datetime import timedelta
import datetime
import os
import socket
import subprocess
import RPi.GPIO as GPIO
app = Flask(__name__)
app.secret_key = 'homeia_rocks'

def getmac():
  # Return the MAC address of interface
  try:
    str = open('/sys/class/net/eth0/address', "r").readline()
  except:
    str = "00:00:00:00:00:00"
  return str[0:17]

def getLanIPAddress():
    arg='ip route list'
    p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
    data = p.communicate()
    split_data = data[0].split()
    ipaddr = split_data[split_data.index('src')+1]
    return ipaddr

def getWanIPAddress():
    res = os.popen("curl -s http://ipecho.net/plain").readline()
    return(res)

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

def getNetTime():
    res = os.popen("date '+%d/%m/%Y %X'").readline()
    return(res)


def getLastReboot():
    f = open('/proc/uptime', 'r')
    uptime_seconds = float(f.readline().split()[0])
    uptime_string = str(timedelta(seconds = uptime_seconds))
    return(uptime_string)


GPIO_list =  [4, 17, 18, 21, 22, 23, 24, 25]
BOARD_list = [7, 11, 12, 13, 15, 16, 18, 22]


@app.route("/")
def overview():
   overviewData = {
      'NetTime': getNetTime(),
      'macAddress' : getmac(),
      'LanIPaddress' : getLanIPAddress(),
      'WanIPaddress' : getWanIPAddress(),
      'temperature' : getCPUtemperature(),
      'lastReboot' : getLastReboot()
      }
   return render_template('overview.html', **overviewData)

@app.route('/sysinfos')
def sysinfos():
    overviewData = {
      'NetTime': getNetTime(),
      'macAddress' : getmac(),
      'LanIPaddress' : getLanIPAddress(),
      'WanIPaddress' : getWanIPAddress(),
      'temperature' : getCPUtemperature(),
      'lastReboot' : getLastReboot()
      }
    return jsonify(overviewData)


@app.route("/playground")
def playground():
   return render_template('playground.html')

@app.route('/playground/GPIO/<int:gpio_id>/ON')
def GPIO_ON(gpio_id):
    GPIO.setmode(GPIO.BCM)
    if gpio_id in GPIO_list:
      GPIO.setup(gpio_id, GPIO.OUT)
      GPIO.output(gpio_id, True)
      message = Markup('GPIO <strong>'+ str(gpio_id) +'</strong> switch ON')
      flash(message, 'success')
    else:
      flash('Invalid GPIO number', 'danger')
    return render_template('playground.html')


@app.route('/playground/GPIO/<int:gpio_id>/OFF')
def GPIO_OFF(gpio_id):
    GPIO.setmode(GPIO.BCM)
    if gpio_id in GPIO_list:
      GPIO.setup(gpio_id, GPIO.OUT)
      GPIO.output(gpio_id, False)
      message = Markup('GPIO <strong>'+ str(gpio_id) +'</strong> switch OFF')
      flash(message, 'success')
    else:
      flash('Invalid GPIO number', 'danger')
    return render_template('playground.html')

@app.route('/playground/BOARD/<int:pin_id>/ON')
def BOARD_ON(pin_id):
    GPIO.setmode(GPIO.BOARD)
    if pin_id in BOARD_list:
      GPIO.setup(pin_id, GPIO.OUT)
      GPIO.output(pin_id, True)
      message = Markup('PIN <strong>'+ str(pin_id) +'</strong> switch ON')
      flash(message, 'success')
    else:
      flash('Invalid Pin number', 'danger')
    return render_template('playground.html')

@app.route('/playground/BOARD/<int:pin_id>/OFF')
def BOARD_OFF(pin_id):
    GPIO.setmode(GPIO.BOARD)
    if pin_id in BOARD_list:
      GPIO.setup(pin_id, GPIO.OUT)
      GPIO.output(pin_id, False)
      message = Markup('PIN <strong>'+ str(pin_id) +'</strong> switch OFF')
      flash(message, 'success')
    else:
      flash('Invalid Pin number', 'danger')
    return render_template('playground.html')

@app.route('/settings')
def settings():
    settings_parameters = {
    'hostname' : socket.gethostname(),
    'ip_adress' : getLanIPAddress()
    }
    return render_template('settings.html', **settings_parameters)

@app.route('/reboot')
def reboot():
    flash('System is rebooting', 'warning')
    os.system("sudo shutdown -r now")
    return redirect(url_for('overview'))

@app.route('/shutdown')
def shutdown():
    flash('System is shuting down', 'warning')
    os.system("sudo shutdown -h now")
    return redirect(url_for('overview'))

# @app.route("/18/off")
# def action18off():
#     GPIO.output(12, False)
#     message = "GPIO 18 was turned off."
#     templateData = {
#         'message' : message,
#         'time' : timeString
#     }
#     return render_template('playground.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)