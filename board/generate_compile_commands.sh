set -e
set -o pipefail

arduino-cli compile --fqbn arduino:avr:uno board.ino -v --only-compilation-database --build-path "tmp"
mv tmp/compile_commands.json .
rm -rf tmp