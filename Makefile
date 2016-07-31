crontab:
	crontab config/crontab

install: crontab
	bin/install
