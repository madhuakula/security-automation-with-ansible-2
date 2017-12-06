#!/usr/bin/python
# Copyright (c) 2017 Akash Mahajan & Madhu Akula
# Apache License 2.0

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: OWASP ZAP Module 
short_description: Scan Web Targets with OWASP ZAP 
description:
    - Scan web targets using this OWASP ZAP.
    - By default it will spider and do a passive scan.
    - This requires OWASP ZAP to be hosted and configured already.
    - Written based on an idea for a chapter in Security Automation with Ansible2 book.
version_added: "2.4"
author: "Akash Mahajan (@makash on GitHub) and Madhu Akula (@madhuakula on Github)"
options:
    host:
        description:
            - The IP address/domain name with port number of the hosted OWASP ZAP instance
        required: true
    target:
        description:
            - The website that needs to be scanned by OWASP ZAP
        required: true
    apikey:
        description:
            - API Key value if the ZAP instance has one
        required: false
        default: null
    scantype:
        description:
            - Type of scan to be done by OWASP ZAP
        required: false
        default: passive
        choices:
          - passive
          - active
notes:
    - The module will indicate changed status if spidering and scanning take place
    - No authentication implemented so far
requirements:
    - Requires the following module to be installed 'python-owasp-zap-v2.4'
    - pip install python-owasp-zap-v2.4 will work
    - Tested with Python2.7 version
'''

EXAMPLES = '''
# Pass in a message
- name: Scan a website
    owasp_zap_test_module:
      host: "http://172.16.1.102:8080"
      target: "http://testphp.vulnweb.com"
      scantype: passive
    register: output
'''

RETURN = '''
changed:
    description: If changed or not (true if scan completed)
    type: bool
output:
    description: Output of OWASP ZAP scan
    type: JSON
target:
    description: Hostname of the web site that was scanned and attacked
    type: str
host:    
    description: Hostname of the OWASP ZAP scanner instance
    type: str
'''
try: 
    from zapv2 import ZAPv2
    HAS_ZAPv2 = True
except ImportError:
    HAS_ZAPv2 = False 

from ansible.module_utils.basic import AnsibleModule
import time

def run_module():
    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(
        host=dict(type='str', required=True),
        target=dict(type='str', required=True),
        apikey=dict(type='str',required=False,default=None),
        scantype=dict(default='passive', choices=['passive','active'])
    )

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if not HAS_ZAPv2:
        module.fail_json(msg = 'OWASP python-owasp-zap-v2.4 required. pip install python-owasp-zap-v2.4')
    
    if module.check_mode:
        return result
    
    host = module.params['host']
    target = module.params['target']
    scantype = module.params['scantype']
    apikey = module.params['apikey']

    # if apikey:
    #     apikey = module.params['apikey']
    
    zap = ZAPv2(apikey=apikey, proxies={'http':host,'https':host})
    zap.urlopen(target)
    try:
        scanid = zap.spider.scan(target)
        time.sleep(2)
        while (int(zap.spider.status(scanid)) < 100):
            time.sleep(2)
    except:
        module.fail_json(msg='Spidering failed')

    time.sleep(5)

    if scantype == 'active':
        try:
            scanid = zap.ascan.scan(target)
            while (int(zap.ascan.status(scanid)) < 100):
                time.sleep(5)
        except:
            module.fail_json(msg='Active Scan Failed')
    else:
        try:
            while (int(zap.pscan.records_to_scan) > 0):
                time.sleep(2)
        except:
            module.fail_json(msg='Passive Scan Failed')

    result['changed'] = True
    result['output'] = zap.core.alerts()
    result['target'] = target
    result['host'] = host

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()