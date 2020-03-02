#!/usr/bin/env bash
#
#
# installer
############

export WDIR=$(pwd)

install_pynmap(){
    pip uninstall python-nmap
    cd /tmp
    git clone https://github.com/dogasantos/python-nmap.git
    cd python-nmap
    python setup.py install
}

install_photon() {
    if [ -d  /usr/share/photon ]
    then
        return 1
    fi
    echo "[*] Installing Photon Crawler"
    cd /usr/share
    git clone https://github.com/s0md3v/Photon.git photon >/dev/null 2>/dev/null
    pip install -r photon/requirements.txt >/dev/null 2>/dev/null
    echo "#!/bin/bash" > /usr/bin/photon
    echo "python3 /usr/share/photon/mod_photon.py \$@" >> /usr/bin/photon
    chmod 755 /usr/bin/photon
    echo "  + DONE"
}

install_gobuster(){
    if [ -d  ${GOPATH}/src/github.com/OJ/gobuster ]
    then
        return 1
    fi

    if [ -d  ${GOPATH} ]
    then
        echo "[*] Installing Gobuster"
        go get github.com/OJ/gobuster >/dev/null 2>/dev/null
        cd ${GOPATH}/src/github.com/OJ/gobuster/
        go build
        echo "  + DONE"
    fi
}

install_massdns(){
    if [ -d  /usr/share/massdns ]
    then
        return 1
    fi
    echo "[*] Installing massdns"
    cd /usr/share
    git clone https://github.com/blechschmidt/massdns.git >/dev/null 2>/dev/null
    cd massdns
    make >/dev/null 2>/dev/null
    make install >/dev/null 2>/dev/null
    echo "  + DONE"
}

install_masscan(){
    if [ -d  /usr/share/masscan ]
    then
        return 1
    fi
    echo "[*] Installing masscan"

    cd /usr/share
    git clone https://github.com/robertdavidgraham/masscan masscan >/dev/null 2>/dev/null
    cd masscan
    make >/dev/null 2>/dev/null
    make install >/dev/null 2>/dev/null
    echo "  + DONE"
}


install_subfinder(){
    if [ -d  ${GOPATH}/src/github.com/subfinder/subfinder ]
    then
        return 1
    fi
    if [ -d  ${GOPATH} ]
    then
        echo "[*] Installing subfinder"
        #cd /usr/local/
        go get github.com/subfinder/subfinder >/dev/null 2>/dev/null
        cd ${GOPATH}/src/github.com/subfinder/subfinder
        go build
        echo "  + NOTE: you must configure your subfinder with your own api keys"
        echo "  + Edit the  ~/.config/subfinder/config.json file and set your keys there"
        echo "  + DONE"
    fi

}

install_amass() {
    if [ -d  ${GOPATH}/src/github.com/OWASP/Amass ]
    then
        return 1
    fi
    if [ -d  ${GOPATH} ]
    then
        echo "[*] Installing Amass"

        cd ${GOPATH}/src/github.com/
        go get -u github.com/OWASP/Amass/... >/dev/null 2>/dev/null
        go install ./... >/dev/null 2>/dev/null
        echo "  + DONE"
    fi

}

install_wapp() {
    if [ -f  /usr/bin/wappalyzer ]
    then
        return 1
    fi
    echo "[*] Installing WappAlyzer"

    apt-get -y install nodejs npm >/dev/null 2>/dev/null
    npm i -g wappalyzer >/dev/null 2>/dev/null
    ln -s /usr/local/lib/node_modules/wappalyzer/cli.js /usr/bin/wappalyzer
    echo "  + DONE"
}

install_eyewitness() {
    if [ -d  /usr/share/eyewitness ]
    then
        return 1
    fi
    echo "[*] Installing EyeWitness"

    cd /usr/share/
    git clone https://github.com/FortyNorthSecurity/EyeWitness.git eyewitness >/dev/null 2>/dev/null
    echo "#!/bin/bash" > /usr/bin/eyewitness
    echo "python /usr/share/eyewitness/EyeWitness.py \$@" >> /usr/bin/eyewitness
    chmod 755 /usr/bin/eyewitness
    echo "  + DONE"
}

install_masstomap() {
    if [ -d  /usr/share/masstomap ]
    then
        return 1
    fi
    echo "[*] Installing Masstomap"

    cd /usr/share/
    git clone https://github.com/dogasantos/masstomap.git masstomap >/dev/null 2>/dev/null
    echo "#!/bin/bash" > /usr/bin/masstomap
    echo "python /usr/share/masstomap/masstomap.py \$@" >> /usr/bin/masstomap
    cd masstomap
    pip install -r requirements.txt
    chmod 755 /usr/share/masstomap/masstomap.py
    chmod 755 /usr/bin/masstomap
    echo "  + DONE"
}

install_linkfinder() {
    if [ -d  /usr/share/linkfinder ]
    then
        return 1
    fi
    echo "[*] Installing Linkfinder"

    cd /usr/share
    git clone https://github.com/GerbenJavado/LinkFinder.git linkfinder >/dev/null 2>/dev/null
    pip install jsbeautifier argparse >/dev/null 2>/dev/null
    echo "#!/bin/bash" >/usr/bin/linkfinder
    echo "python /usr/share/linkfinder/mod_linkfinder.py \$@" >> /usr/bin/linkfinder
    chmod 755 /usr/bin/linkfinder
    echo "  + DONE"

}
install_s3scanner(){
    if [ -d  /usr/share/s3scanner ]
    then
        return 1
    fi
    echo "[*] Installing s3scanner"
    cd /usr/share/
    git clone https://github.com/sa7mon/S3Scanner.git s3scanner >/dev/null 2>/dev/null
    cd s3scanner
    pip install -r requirements.txt >/dev/null 2>/dev/null
    apt-get -y install awscli >/dev/null 2>/dev/null
    echo "#!/bin/bash" >/usr/bin/s3scanner
    echo "python /usr/share/s3scanner/mod_s3scanner.py \$@" >> /usr/bin/s3scanner
    chmod 755 /usr/bin/s3scanner
    echo "  + NOTE: you must configure your awscli with your own aws key by using"
    echo "  + command: aws configure"
    echo "  + DONE"

}

install_wordlists(){
    echo "[*] Downloading Wordlists"
    dist=$(cat /etc/issue|head -n1|cut -f1 -d ' ')
    mkdir -p /usr/share/wordlists
    cd /usr/share/wordlists
    echo "  + RobotsDisallowed"
    git clone https://github.com/danielmiessler/RobotsDisallowed.git RobotsDisallowed >/dev/null 2>/dev/null
    echo "  + SecLists"
    git clone https://github.com/danielmiessler/SecLists.git SecLists >/dev/null 2>/dev/null
    echo "  + Brazillian pt_BR"
    git clone https://github.com/dogasantos/ptbr-wordlist.git ptbr-wordlist >/dev/null 2>/dev/null
    echo "  + Commonspeak2"
    mkdir commonspeak2
    cd commonspeak2
    wget -q https://raw.githubusercontent.com/assetnote/commonspeak2-wordlists/master/routes/rails-1k-sample-august-2018.txt
    wget -q https://raw.githubusercontent.com/assetnote/commonspeak2-wordlists/master/subdomains/subdomains.txt

}

#COMMIX_GIT="https://github.com/commixproject/commix.git"
#PARAMETH_GIT="https://github.com/maK-/parameth.git"
#AJUN_GIT="https://github.com/s0md3v/Arjun.git"  # NEEDS PYTHON 3.4

echo "[*] Installing gcc make and pcap"
apt-get -y install git gcc make libpcap-dev zlib1g-dev libjpeg-dev zlib1g-dev libjpeg-dev python-opencv python-lxml >/dev/null 2>/dev/null
echo "[*] Installing python dependencies"
pip install -r requirements.txt >/dev/null 2>/dev/null


install_photon
install_gobuster
install_massdns
#install_masscan
install_amass
install_wapp
install_eyewitness
install_subfinder
install_masstomap
install_linkfinder
install_s3scanner
#install_wordlists
install_pynmap
cd $WDIR
echo "  + DONE"




