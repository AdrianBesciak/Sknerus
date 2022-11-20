living_room:
	python3 window.py 1 0 14 15 &
	python3 lamp.py 1 4 &
	python3 radiator.py 1 18 &
	python3 thermometer_bpm280.py 1

bathroom:
	python3 boiler.py 2 18 &
	python3 lamp.py 2 15 &
	python3 window.py 1 0 14 15

hall:
	python3 lamp.py 3 15 &
