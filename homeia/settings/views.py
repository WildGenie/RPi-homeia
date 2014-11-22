#################
#### imports ####
#################

from flask import render_template, Blueprint, request, flash, redirect, url_for

# Import the database object from the main app module
from homeia import db

################
#### config ####
################

settings_blueprint = Blueprint('settings', __name__)


################
#### routes ####
################

# use decorators to link the function to a url
@settings_blueprint.route('/settings')
def index():
    return render_template('settings/index.html')