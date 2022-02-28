#################
#### imports ####
#################

from flask import render_template, Blueprint, request, flash, redirect, url_for, Markup
import wiringpi2 as wiringpi 

################
#### config ####
################

WIRINGPI_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 14, 15, 16, 17]
wiringData = {
      'wiring_pin_list' : WIRINGPI_list,
      'wiring_pin_mode' : [0, 1],
      'wiring_pin_states' : [{'label' : 'Off', 'value' : 0}, {'label' : 'On', 'value' : 1}]
    }


playground_blueprint = Blueprint('playground', __name__)


################
#### routes ####
################

# use decorators to link the function to a url
@playground_blueprint.route('/')
def index():
    return render_template('playground/index.html', **wiringData)

@playground_blueprint.route('/wiring/<int:wp_id>/<int:wp_state>')
def wiring(wp_id, wp_state):
    wiringpi.wiringPiSetup()
    if wp_id in WIRINGPI_list:
        wiringpi.pinMode(wp_id, 1)
        wiringpi.digitalWrite(wp_id, wp_state)
        message = Markup(
            f'GPIO <strong>{str(wp_id)}</strong> switched to : {str(wp_state)}'
        )

        flash(message, 'success')
    else:
        flash('Invalid WiringPi number', 'danger')
    return render_template('playground/index.html', **wiringData)

@playground_blueprint.route('/i2c/<int:i2cAddr>/<i2cMode>/<int:i2cData>')
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

    message = Markup(
        f'I2C {str(i2cAddr)} returned : <strong>(not implemented yet)'
        + '</strong>'
    )

    flash(message, 'success')

    return render_template('playground/index.html', **i2cReturnedData)