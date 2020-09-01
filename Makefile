.PHONY: mac linux clean-mac clean-linux

APP=random-wsg-bg
FILENAME=$(APP).py
INSTALL_PATH=/usr/local/bin/$(APP)

MAC_SERVICE_FILENAME=$(APP).plist
MAC_SERVICE_INSTALL_PATH=~/Library/LaunchAgents/$(MAC_SERVICE_FILENAME)
LINUX_SERVICE_FILENAME=$(APP).service
LINUX_SERVICE_INSTALL_PATH=/etc/systemd/system/$(LINUX_SERVICE_FILENAME)


mac:
	cp ${FILENAME} ${INSTALL_PATH}
	cp ${MAC_SERVICE_FILENAME} ${MAC_SERVICE_INSTALL_PATH}
	chmod 644 ${MAC_SERVICE_INSTALL_PATH}
	launchctl load ${MAC_SERVICE_INSTALL_PATH}
	launchctl start $(APP)

linux:
	cp  ${INSTALL_PATH}
	cp $(LINUX_SERVICE_FILENAME) ${LINUX_SERVICE_INSTALL_PATH}
	systemctl daemon-reload
	systemctl start $(LINUX_SERVICE_FILENAME)
	systemctl enable $(LINUX_SERVICE_FILENAME)

clean-mac:
	launchctl unload $(MAC_SERVICE_INSTALL_PATH)
	launchctl stop $(APP)
	rm -rf $(MAC_SERVICE_INSTALL_PATH)

clean-linux:
	rm -rf $(INSTALL_PATH)
	rm -rf $(LINUX_SERVICE_INSTALL_PATH)
	systemctl daemon-reload
	systemctl stop $(LINUX_SERVICE_FILENAME)
	systemctl disable $(LINUX_SERVICE_FILENAME)
