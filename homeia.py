# -*- coding: utf-8 -*-
from functools import wraps
from flask import Flask, Markup, flash, render_template, redirect, url_for, jsonify, g, request, Response
from datetime import timedelta
import sqlite3
import datetime
import os
import socket
import miniupnpc
import subprocess
import wiringpi2 as wiringpi 
app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db/homeia.db'),
    DEBUG=True,
    SECRET_KEY='homeia_rocks',
    USERNAME='admin',
    PASSWORD='admin',
    WEBPORT=8080
))
app.config.from_envvar('HOMEIA_SETTINGS', silent=True)


def initUPNP():
  #UPNP setting up
  u = miniupnpc.UPnP()
  print 'inital(default) values :'
  print ' discoverdelay', u.discoverdelay
  print ' lanaddr', u.lanaddr
  print ' multicastif', u.multicastif
  print ' minissdpdsocket', u.minissdpdsocket
  u.discoverdelay = 200;
  #u.minissdpdsocket = '../minissdpd/minissdpd.sock'
  # discovery process, it usualy takes several seconds (2 seconds or more)
  print 'Discovering... delay=%ums' % u.discoverdelay
  print u.discover(), 'device(s) detected'
  # select an igd
  try:
    u.selectigd()
  except Exception, e:
    print 'Exception :', e
    sys.exit(1)
  # display information about the IGD and the internet connection
  print 'local ip address :', u.lanaddr
  print 'external ip address :', u.externalipaddress()
  print u.statusinfo(), u.connectiontype()
  print u.addportmapping(app.config['WEBPORT'], 'TCP', u.lanaddr, app.config['WEBPORT'], 'HOMEIA Web server', '')
  #END UPNP setting up


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == app.config['USERNAME'] and password == app.config['PASSWORD']

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

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
    return(ipaddr)

def getWanIPAddress():
    try:
      res = os.popen("curl -s http://ipecho.net/plain").readline()
    except:
      res = u.externalipaddress()
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
WIRINGPI_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 14, 15, 16, 17]
wiringData = {
      'wiring_pin_list' : WIRINGPI_list,
      'wiring_pin_mode' : [0, 1],
      'wiring_pin_states' : [{'label' : 'Off', 'value' : 0}, {'label' : 'On', 'value' : 1}]
    }

#settings = getSettings()
#app.config.update(WEBPORT=settings['WEBPORT'])

@app.route("/")
@requires_auth
def overview():
   overviewData = {
      'NetTime': getNetTime(),
      'macAddress' : getmac(),
      'LanIPaddress' : getLanIPAddress(),
      'WanIPaddress' : getWanIPAddress(),
      'temperature' : getCPUtemperature(),
      'lastReboot' : getLastReboot(), 
      'RaspberryPiRev' : wiringpi.piBoardRev()
      }
   return render_template('overview.html', **overviewData)

@app.route('/sysinfos')
def sysinfos():
    overviewData = {
      'NetTime': getNetTime(),
      'LanIPaddress' : getLanIPAddress(),
      'WanIPaddress' : getWanIPAddress(),
      'temperature' : getCPUtemperature(),
      'lastReboot' : getLastReboot()
      }
    return jsonify(overviewData)

@app.route("/playground")
def playground():
   return render_template('playground.html', **wiringData)

@app.route('/playground/wiring/<int:wp_id>/<int:wp_state>')
def wiring(wp_id, wp_state):
    wiringpi.wiringPiSetup()  
    if wp_id in WIRINGPI_list:
      wiringpi.pinMode(wp_id, 1)
      wiringpi.digitalWrite(wp_id, wp_state)
      message = Markup('GPIO <strong>'+ str(wp_id) +'</strong> switched to : '+ str(wp_state))
      flash(message, 'success')
    else:
      flash('Invalid WiringPi number', 'danger')
    return render_template('playground.html', **wiringData)

@app.route('/playground/i2c/<int:i2cAddr>/<i2cMode>/<int:i2cData>')
def i2c(i2cAddr, i2cMode, i2cData=None):

    # i2c = wiringpi2.I2C()
    # dev = i2c.setup(0x20) ( not sure about what to pass into the setup function, but presumably a device address? )
    # i2c.read(dev)

    i2c = wiringpi.I2C()
    dev = i2c.setup(0x20)
    
    i2cReturnedData = {
        'i2cAddress' : i2cAddr,
        #'i2cData' : i2c.read(dev)
        'i2cData' : 'returned data by I2C device'
    }

    message = Markup('I2C '+ str(i2cAddr) +' returned : <strong>'+ '(not implemented yet)' +'</strong>')
    flash(message, 'success')

    return render_template('playground.html', **i2cReturnedData)

@app.route('/settings')
def settings():
    settings = getSettings()
    settings_parameters = {
    'hostname' : socket.gethostname(),
    'ip_adress' : getLanIPAddress(),
    'webport' : 8080
    }
    return render_template('settings.html', **settings_parameters)

@app.route('/reboot')
def reboot():
    print u.deleteportmapping(app.config['WEBPORT'], 'TCP')
    flash('System is rebooting', 'warning')
    os.system("sudo shutdown -r now")
    return redirect(url_for('overview'))

@app.route('/shutdown')
def shutdown():
    print u.deleteportmapping(app.config['WEBPORT'], 'TCP')
    flash('System is shuting down', 'warning')
    os.system("sudo shutdown -h now")
    return redirect(url_for('overview'))


@app.route('/stopserver')
def stopserver():
    print u.deleteportmapping(app.config['WEBPORT'], 'TCP')
    shutdown_server()
    return 'Server shutting down...'

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=app.config['WEBPORT'], debug=True)