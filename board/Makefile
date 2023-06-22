# Configuration
BOARD := uno
SRC := board.ino
AVR := arduino:avr
BUILD_DIR := build
SERIAL_PORT := /dev/$(shell ls /dev | grep -E -i 'usb' | head -n 1)
BOARD_TYPE := $(AVR):$(BOARD)
# Targets
.PHONY: build upload clean all
all: $(BOARD) upload
$(BOARD):
	@echo "Building..."
	mkdir -p $(BUILD_DIR)
	arduino-cli compile --fqbn $(BOARD_TYPE) $(SRC) -v --build-path $(BUILD_DIR)

upload:
	@echo "Uploading..."
	arduino-cli upload -p $(SERIAL_PORT) --fqbn $(BOARD_TYPE) $(SRC) -v --input-dir $(BUILD_DIR)

clean:
	@echo "Cleaning..."
	rm -rf $(BUILD_DIR)
