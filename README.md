# nrpe_check_postgrey
nrpe plugin for postgrey

create a cron job as root "* * * * * python /usr/lib/nagios/plugins/check_greylist.py --cron 1 > /dev/null"

then use it from nrpe custom command (adjust limits to suit your needs)
command[check_greylist]=/usr/lib/nagios/plugins/check_greylist.py -c 40 -w 10
