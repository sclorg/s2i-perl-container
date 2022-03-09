s/^Listen 80/Listen 0.0.0.0:8080/
s/^User apache/User default/
s/^Group apache/Group root/
s%^DocumentRoot "/var/www/html"%DocumentRoot "/opt/app-root/src"%
s%^<Directory "/var/html"%<Directory "/opt/app-root/src"%
s%^ErrorLog "logs/error_log"%ErrorLog "|/usr/bin/cat"%
s%CustomLog "logs/access_log"%CustomLog "|/usr/bin/cat"%
