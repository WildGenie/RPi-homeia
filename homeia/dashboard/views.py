#################
#### imports ####
#################

from flask import render_template, Blueprint, request, flash, redirect, url_for

################
#### config ####
################

dashboard_blueprint = Blueprint('dashboard', __name__)


################
#### routes ####
################

# use decorators to link the function to a url
@dashboard_blueprint.route('/')
def index():
    return render_template('dashboard/index.html')