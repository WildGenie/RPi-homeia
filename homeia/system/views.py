#################
#### imports ####
#################

from flask import render_template, Blueprint, request, flash, redirect, url_for
import os

################
#### config ####
################

system_blueprint = Blueprint('system', __name__)

from homeia.system.models import System

################
#### routes ####
################

# use decorators to link the function to a url

@system_blueprint.route('/system/reboot')
def reboot():
    #print u.deleteportmapping(app.config['WEBPORT'], 'TCP')
    flash('System is rebooting', 'warning')
    os.system("sudo shutdown -r now")
    return redirect(url_for('dashboard.index'))

@system_blueprint.route('/system/shutdown')
def shutdown():
    #print u.deleteportmapping(app.config['WEBPORT'], 'TCP')
    flash('System is shuting down', 'warning')
    os.system("sudo shutdown -h now")
    return redirect(url_for('dashboard.index'))

@system_blueprint.route('/system/stop')
def stop():
    #print u.deleteportmapping(app.config['WEBPORT'], 'TCP')
    System.shutdown_server()
    return 'Server shutting down...'