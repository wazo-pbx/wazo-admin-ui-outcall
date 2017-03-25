install:
	python setup.py install
	cp etc/wazo-admin-ui/conf.d/outcall.yml /etc/wazo-admin-ui/conf.d
	systemctl restart wazo-admin-ui

uninstall:
	pip uninstall wazo-admin-ui-outcall
	rm /etc/wazo-admin-ui/conf.d/outcall.yml
	systemctl restart wazo-admin-ui
