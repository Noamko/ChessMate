set -e
set -o pipefail

arduino-cli compile --fqbn arduino:avr:mega board.ino -v
arduino-cli upload --fqbn arduino:avr:mega -p /dev/tty.usbmodem101 -v
screen /dev/tty.usbmodem101
