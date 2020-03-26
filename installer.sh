#!/usr/bin/env bash
#
#
# installer
############

export WDIR=$(pwd)


prepare()
{
    export DEBIAN_FRONTEND=noninteractive
    apt-get update
    if [[ $HOSTTYPE == "arm64" ]]
    then
        apt-get -y install python-opencv python-lxml
    fi
    apt-get -y install nmap python python-pip vim
    apt-get -y install build-essential pkg-config



    export GOROOT=/usr/local/go
    export GOPATH=/usr/share/go
    export GOBIN=$GOPATH/bin
    export PATH=$PATH:$GOPATH:$GOBIN:$GOROOT/bin

    echo "GOROOT=/usr/local/go" >> ~/.bashrc
    echo "GOPATH=/usr/share/go" >> ~/.bashrc
    echo 'GOBIN=$GOPATH/bin' >> ~/.bashrc
    echo 'PATH=$PATH:$GOPATH:$GOBIN:$GOROOT/bin' >> ~/.bashrc

    cd /usr/local/
    if [[ $HOSTTYPE == "x86_64" ]]
    then
        export arch=amd64
        export GO111MODULE=auto
        if [[ ! -d $GOROOT ]]
        then
            mkdir -p ${GOROOT}
            mkdir -p ${GOPATH}
            echo "[*] Download and install Go"
            wget -q https://dl.google.com/go/go1.13.linux-amd64.tar.gz
            tar zxf go1.13.linux-amd64.tar.gz
        else
            echo "[*] Go is present, no need to download again"
        fi
    fi

    if [[ $HOSTTYPE == "arm64" ]]
    then
        export arch=arm64
        export GO111MODULE=on
        if [[ ! -d $GOROOT ]]
        then
            mkdir -p ${GOROOT}
            mkdir -p ${GOPATH}
            echo "[*] Download and install Go"
            wget -q https://dl.google.com/go/go1.13.linux-arm64.tar.gz
            tar zxf go1.13.linux-arm64.tar.gz
        else
            echo "[*] Go is present, no need to download again"
        fi
    fi
}


install_pynmap(){
    pip uninstall -y python-nmap
    cd /tmp
    git clone https://github.com/dogasantos/python-nmap
    cd python-nmap
    python setup.py install
    cd /tmp
    rm -rf python-nmap
}

install_crtsh(){
    cd /tmp
    git clone https://github.com/PaulSec/crt.sh
    cd crt.sh
    pip install -r requirements.txt
    python setup.py install
}

install_photon() {
    if [ -d  /usr/share/photon ]
    then
        return 1
    fi
    echo "[*] Installing Photon Crawler"
    cd /usr/share
    git clone https://github.com/s0md3v/Photon.git photon
    pip install -r photon/requirements.txt
    echo "#!/bin/bash" > /usr/bin/photon
    echo "python3 /usr/share/photon/mod_photon.py \$@" >> /usr/bin/photon
    chmod 755 /usr/bin/photon
    echo "  + DONE"
}


install_massdns(){
    if [ -d  /usr/share/massdns ]
    then
        return 1
    fi
    echo "[*] Installing massdns"
    cd /usr/share
    git clone https://github.com/blechschmidt/massdns.git
    cd massdns
    make
    make install
    echo "  + DONE"
}

install_masscan(){
    if [ -d  /usr/share/masscan ]
    then
        return 1
    fi
    echo "[*] Installing masscan"

    cd /usr/share
    git clone https://github.com/robertdavidgraham/masscan masscan
    cd masscan
    make
    make install
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
        go get github.com/projectdiscovery/subfinder/cmd/subfinder
        #go get github.com/subfinder/subfinder
        #cd ${GOPATH}/src/github.com/subfinder/subfinder
        #go build
        echo "  + NOTE: you must configure your subfinder with your own api keys"
        echo "  + Edit the  ~/.config/subfinder/config.json file and set your keys there"
        echo "  + DONE"
    fi

}

install_sublist3r(){

    if [ ! -d  /usr/share/Sublist3r ]
    then
        echo "[*] Installing Sublist3r"
        cd /usr/share/
        git clone https://github.com/aboul3la/Sublist3r.git
        cd /usr/share/Sublist3r
        pip install -r requirements.txt
        python setup.py install
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
        mkdir -p ${GOPATH}/src/github.com/
        cd ${GOPATH}/src/github.com/
        go get -u github.com/OWASP/Amass/...
        cd OWASP/Amass
        go install ./...
        echo "  + DONE"
    fi

}

install_wapp() {
    if [ -f  /usr/bin/wappalyzer ]
    then
        return 1
    fi
    echo "[*] Installing WappAlyzer"

    apt-get -y install nodejs npm jq
    npm i -g wappalyzer
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
    git clone https://github.com/FortyNorthSecurity/EyeWitness.git eyewitness
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
    git clone https://github.com/dogasantos/masstomap.git masstomap
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
    git clone https://github.com/GerbenJavado/LinkFinder.git linkfinder
    pip install jsbeautifier argparse
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
    git clone https://github.com/sa7mon/S3Scanner.git s3scanner
    cd s3scanner
    pip install -r requirements.txt
    apt-get -y install awscli
    echo "#!/bin/bash" >/usr/bin/s3scanner
    echo "python /usr/share/s3scanner/s3scanner.py \$@" >> /usr/bin/s3scanner
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
    git clone https://github.com/danielmiessler/RobotsDisallowed.git RobotsDisallowed
    echo "  + SecLists"
    git clone https://github.com/danielmiessler/SecLists.git SecLists
    #echo "  + Brazillian pt_BR"
    #git clone https://github.com/dogasantos/ptbr-wordlist.git ptbr-wordlist
    echo "  + Commonspeak2"
    git clone https://github.com/assetnote/commonspeak2-wordlists.git

}

#COMMIX_GIT="https://github.com/commixproject/commix.git"
#PARAMETH_GIT="https://github.com/maK-/parameth.git"
#AJUN_GIT="https://github.com/s0md3v/Arjun.git"  # NEEDS PYTHON 3.4

echo "[*] Installing gcc make and pcap"
apt-get -y install gcc wget curl make libpcap-dev zlib1g-dev libjpeg-dev
apt-get -y install python-opencv python-lxml python-pip



prepare
install_massdns
install_masscan
install_amass
install_wapp
#install_eyewitness
install_subfinder
install_sublist3r
install_masstomap
#install_linkfinder
install_s3scanner
install_wordlists
install_pynmap
install_crtsh
cd $WDIR

echo "[*] Installing python dependencies"
pip install -r requirements.txt

echo "  + DONE"
$SHELL