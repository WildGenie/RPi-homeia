#################
#### imports ####
#################

from flask import render_template, Blueprint, request, flash, redirect, url_for

################
#### config ####
################

boilerplate_blueprint = Blueprint('boilerplate', __name__)


################
#### routes ####
################

# use decorators to link the function to a url
@boilerplate_blueprint.route('/')
def index():
    return render_template('boilerplate/index.html')