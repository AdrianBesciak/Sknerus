living_room:
	python3 window.py 1 0 14 15 &
	python3 lamp.py 1 4 &
	python3 radiator.py 1 18 &
	python3 thermometer_bpm280.py 1

bathroom:
	python3 boiler.py 2 boiler_pin &
	python3 lamp.py 2 led_pin &
	python3 window.py 1 0 servo_pin, switch_pin

hall:
	python3 lamp.py 3 led_pin &