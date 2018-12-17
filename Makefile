.PHONY: mac linux clean-mac clean-linux


mac:
	cp bgmac.plist ~/Library/LaunchAgents/bgmac.plist
	launchctl load ~/Library/LaunchAgents/bgmac.plist
	launchctl start bgmac 

linux:
	cp wsg-random-bg /usr/local/bin
	cp wsg-random-bg.service /etc/systemd/system
	systemctl daemon-reload
	systemctl start wsg-random-bg.service
	systemctl enable wsg-random-bg.service

clean-mac:
	launchctl stop bgmac
	rm -rf ~/Library/LaunchAgents/bgmac.plist

clean-linux:
	rm -rf /usr/local/bin/wsg-random-bg
	rm -rf /etc/systemd/system/wsg-random-bg.service
	systemctl daemon-reload
	systemctl stop wsg-random-bg.service
	systemctl disable wsg-random-bg.service
