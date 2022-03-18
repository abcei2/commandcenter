
sudo apt update && sudo apt install supervisor
pip install virtualenv
sudo systemctl status supervisor
# clone this repo
cd commandcenter/
python -m venv .env
source .env/bin/activate
pip install flask pyserial
# we can go with env activated
sudo cp ./commander.conf /etc/supervisor/conf.d/commander.conf
ssh-keygen
ssh -i /home/pi/.ssh/id_rsa -N  -o "ServerAliveInterval 20" -o ExitOnForwardFailure=yes -R 5000:localhost:5000    root@207.246.118.54
sudo cp ./ratatunel5000.conf /etc/supervisor/conf.d/ratatunel5000.conf
mkdir ./data/logs/
sudo supervisorctl reread
sudo supervisorctl update

# install arduino-cli
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
nano ~/.bashrc
export PATH=$PATH:/home/pi/bin
source ~/.bashrc
arduino-cli config init
arduino-cli core install arduino:avr

cd commandcenter/
arduino-cli lib install DallasTemperature "Grove 4-Digit Display" Arduino_JSON
arduino-cli lib update-index
sudo usermod -a -G dialout $USER
arduino-cli compile -b arduino:avr:nano ECcontroler
arduino-cli upload -p /dev/ttyUSB0 -b arduino:avr:nano --verbose ECcontroler