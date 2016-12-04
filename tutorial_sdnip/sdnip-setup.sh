#!/bin/bash
# sdnip-setup.sh
# 
# Runs as sdnip user.
#
# Sets up the SDN-IP tutorial.

export USER=sdnip

echo "Creating SDN-IP tutorial"

#--------------- Copy SDNIP code to home -----

cp -r /home/mininet/onos/tools/tutorials/sdnip /home/sdnip/
cp -r /home/sdnip/sdnip/configs /home/sdnip/
sudo -u mininet sh -c 'cp -r /home/sdnip/sdnip/configs/addresses.json /home/mininet/onos/tools/package/config'
sudo -u mininet sh -c 'cp -r /home/sdnip/sdnip/configs/sdnip.json /home/mininet/onos/tools/package/config'


#--------------- Add iptables rule for BGP-ONOS communication -----

echo "sudo iptables -A PREROUTING -t nat -i root-eth0 -p tcp --dport 2000 -j DNAT --to 10.0.3.11:2000 " >> /home/sdnip/.xprofile

DESKTOP=/home/${USER}/Desktop

mkdir -p ${DESKTOP}

cat > ${DESKTOP}/ONOS << EOF
[Desktop Entry]
Encoding=UTF-8
Type=Application
Name=ONOS
Name[en_US]=ONOS
Icon=konsole
Exec=/usr/bin/lxterminal -e '/home/mininet/apache-karaf-3.0.3/bin/client -u karaf -h 10.0.3.11'
Comment[en_US]=
EOF

cat > "${DESKTOP}/SDN-IP Mininet" << EOF
[Desktop Entry]
Encoding=UTF-8
Type=Application
Name=SDN-IP Mininet
Name[en_US]=SDN-IP Mininet
Icon=konsole
Exec=/usr/bin/lxterminal -e 'sudo mn --custom /home/sdnip/sdnip/tutorial.py --topo sdnip --controller remote,10.0.3.11 --nolistenport'
Comment[en_US]=
EOF

cat > ${DESKTOP}/Tutorial << EOF
[Desktop Entry]
Encoding=UTF-8
Type=Application
Name=SDN-IP Tutorial
Name[en_US]=SDN-IP Tutorial
Icon=internet-web-browser
Exec=/usr/bin/chromium-browser https://wiki.onosproject.org/display/ONOS/SDN-IP+Tutorial
Comment[en_US]=
EOF

cat > ${DESKTOP}/GUI << EOF
[Desktop Entry]
Encoding=UTF-8
Type=Application
Name=ONOS GUI
Name[en_US]=ONOS GUI
Icon=internet-web-browser
Exec=/usr/bin/chromium-browser http://10.0.3.11:8181/onos/ui/index.html#topo
Comment[en_US]=
EOF

cat > ${DESKTOP}/Wireshark << EOF
[Desktop Entry]
Encoding=UTF-8
Type=Application
Name=Wireshark
Name[en_US]=Wireshark
Icon=wireshark
Exec=/usr/bin/wireshark
Comment[en_US]=
EOF

cat > ${DESKTOP}/Reset << EOF
[Desktop Entry]
Encoding=UTF-8
Type=Application
Name=Reset
Name[en_US]=Reset
Icon=konsole
Exec=/usr/bin/lxterminal -t 'Resetting; please wait' -e '/bin/bash -c /home/mininet/reset-to-1.sh'
Comment[en_US]=
EOF
