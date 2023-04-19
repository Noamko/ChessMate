set -e
set -o pipefail

arduino-cli compile --fqbn arduino:avr:mega board.ino -v --only-compilation-database --build-path "tmp"
mv tmp/compile_commands.json .
rm -rf tmp