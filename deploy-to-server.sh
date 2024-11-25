
#!bin/bash

# -avzt
# -r: recursive (implied by -a)
# -a: archive ensures that symbolic links, devices, attributes, permissions, ownerships etc are preserved
# -z: zip/compress files during transfer
# -t: preserve times
# --dry-run to just list out the files without actually transferring
# --exclude=PATTERN (take one pattern each but can be included multiple times)

rsync -avzt \
-e "ssh -i ~/.ssh/id_rsa_taylorvananne" \
--exclude "__pycache__/" \
--exclude "/venv/" \
--exclude ".git/" \
--exclude "/db" \
--exclude "/db.csv" \
./ \
taylor@taylorvananne.com:~/repos/trafficpatterns/
