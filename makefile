make living_room:
    python3 window.py 1 0 14 15
	echo 'Window node is started'
	python3 lamp.py 1 4
	echo 'Lamp node is started'
	python3 radiator.py 1 18
	echo 'Radiator node is started'
	python3 thermometer_bpm280.py 1
	echo 'Thermometer node is started'

make bathroom:
    python3 boiler.py 2 boiler_pin
	python3 lamp.py 2 led_pin
	python3 window.py 1 0 servo_pin, switch_pin

make hall:
    python3 lamp.py 3 led_pin