run:
	python3 solution/server.py

test:
	./test-driver-bin/niova-candidate-test-driver_linux

test100:
	./test-driver-bin/niova-candidate-test-driver_linux -concurrency 100
