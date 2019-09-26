# cpgather
infogather tool

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
- domain.pickle (you won't need to perform portscan again everytime you run this tool)


### notes

- This tool will detect if you already have a domain.<tool> report and will skip that step. If you want to run that step, remove or rename that file

- This tool uses pickle (be aware of security implications) to dump nmap object report on file, and load it again everytime you run it. So the scan should be executed just 1 time.


### future

diminish dependency on other tools by creating it's own mechanisms
but still being able to feed the tool with those awesome tools

### motivation and why python instead of bash or go

Because I like python and I want to learn more of it. It's fun to code python.

### to be added soon

- certspotter
- crt.sh

