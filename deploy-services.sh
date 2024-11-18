
# Copy to systemd unit file dir
sudo cp ./traffic-job.service /etc/systemd/system/
sudo cp ./traffic-job.timer /etc/systemd/system/

# Change ownership to root
sudo chown root:root /etc/systemd/system/traffic-job.service
sudo chown root:root /etc/systemd/system/traffic-job.timer

# Reload systemctl daemon to pick up on the new services
sudo systemctl daemon-reload

# Enable the timer (it's optional to enable the service)
sudo systemctl enable traffic-job.timer
sudo systemctl status traffic-job.timer

