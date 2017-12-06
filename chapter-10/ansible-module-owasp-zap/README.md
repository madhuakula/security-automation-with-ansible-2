# ansible-module-owasp-zap
Ansible module for OWASP ZAP using Python API to scan web targets for security issues

## Why use this?
A simple module to enable using Ansible to initiate web security scans using OWASP ZAP. 

## What 
This module enables you to interact with an already setup and configured ZAP instance to execute passive active scans against web targets for security tests.

## How
The module works with the OWASP ZAP API available when we have an existing running ZAP instance. This is similar to the [ZAP Baseline Scan](https://github.com/zaproxy/zaproxy/wiki/ZAP-Baseline-Scan) in the default settings. 

## Get Started 
### Start ZAP 

    docker run --name zap -u zap -p 8080:8080 -i owasp/zap2docker-stable zap.sh -daemon -host 0.0.0.0 -port 8080 -config api.disablekey=true -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true
  
_For testing, API key is disabled. Please change as per your requirement_

### Software Pre-requisites
Ensure that the OWASP ZAP Python client is installed

    pip install python-owasp-zap-v2.4
  
Assuming that `ansible` is already setup the following command will work if you don't want to copy the module to a path which is ANSIBLE_LIBRARY

    $ ANSIBLE_LIBRARY=. ansible -m owasp_zap_test_module localhost -a "host=http://ZAP-Proxy:PORT target=http://target-webapp"
  
If you want to specify an API KEY

    $ ANSIBLE_LIBRARY=. ansible -m owasp_zap_test_module localhost -a "host=http://ZAP-Proxy:PORT target=http://target-webapp apikey=SECRET-VALUE"
 
 If you want to run an Active scan
 
      $ ANSIBLE_LIBRARY=. ansible -m owasp_zap_test_module localhost -a "host=http://ZAP-Proxy:PORT target=http://target-webapp scantype=active"
      
### Sample Playbook 
A sample playbook you can use

        - name: Testing OWASP ZAP Test Module
          connection: local
          hosts: localhost
          tasks:
          - name: Scan a website
            owasp_zap_test_module:
              host: "http://ZAP-Proxy:PORT"
              target: "http://target-webapp"
              scantype: passive
            register: output
        - name: Print version
          debug:
            msg: "Scan Report: {{ output }}"






