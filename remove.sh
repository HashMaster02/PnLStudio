sudo systemctl stop findash_frontend.service
sudo systemctl stop findash_backend.service

sudo systemctl disable findash_frontend.service
sudo systemctl disable findash_backend.service

sudo rm /etc/systemd/system/findash_backend.service
sudo rm /etc/systemd/system/findash_frontend.service
