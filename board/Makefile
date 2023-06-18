# Configuration
BOARD_TYPE := arduino:avr:mega
SRC := board.ino
BUILD_DIR := build
SERIAL_PORT := /dev/$(shell ls /dev | grep -E -i 'ACM' | head -n 1)

# Targets
.PHONY: build upload clean all

build:
	@echo "Building..."
	mkdir -p $(BUILD_DIR)
	./arduino-cli compile --fqbn $(BOARD_TYPE) $(SRC) -v --build-path $(BUILD_DIR)

upload:
	@echo "Uploading..."
	./arduino-cli upload -p $(SERIAL_PORT) --fqbn $(BOARD_TYPE) $(SRC) -v --input-dir $(BUILD_DIR)

clean:
	@echo "Cleaning..."
	rm -rf $(BUILD_DIR)

all: build upload
