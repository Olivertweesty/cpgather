# cpgather
infogather tool

NOTE: this is still under development, then you can expect some buggy behavior.

cpgather is an automation tool designed to gather relevant information on a target domain and perform a few tasks.

You need to provide the target domain, and optionally a forward dns dump file.
cpgather will use other tools like sublist3r, amass, masscan, nmap, s3scanner, wappanalyzer and others, in order to gather all relevant info.

### You'll get the following files (reports):
- domain.amass
- domain.sublist3r
- domain.wayback
- domain.subfinder (bruteforce mode using bitquark wordlist, but you can specify your own wordlist via cli)
- domain.massdns
- domain.masscan
- domain.masscan.new (IP:port,port,port format for masscan report)
- domain.nmap.txt
- domain.nmap.xml
- domain.nmap.grep
- domain.hosts (list of all subdomains found on that domain)
- domain.ips (list of all ips found on that domain)
- domain.buckets (s3 buckets)
- domain.wapp (full weba pplication stack, from jquery to webserver)
- domain.web (full list of URLS found)
- domain.js.allfiles (full list with all javscript files found while scrapping the first page of each target. Targets are in uri format)
- domain.js.dirs (list of each directory that contains js files for all targets)
- domain.js.dirsuri (same as above, but full uri)


### notes

- This tool will detect if you already have a domain.<tool> report and will skip that step. If you want to run that step, remove or rename that file

- This tool uses pickle (be aware of security implications) to dump nmap object report on file, and load it again everytime you run it. So the scan should be executed just 1 time.

### motivation and why python instead of bash or go

While multitasking it's better to automate a few common tasks.
The simpler, the better

I've seen this being made through aliases and bash scripts, but I like to code my scripts in python. It's an opportunity to learn more aspects of Python coding and make of this a win/win.

