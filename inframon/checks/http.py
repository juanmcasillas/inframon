##!/usr/bin/env bash
# -*- coding: utf-8 -*-
# /////////////////////////////////////////////////////////////////////////////
# //
# // icmp.py 
# //
# // implement the ping check
# //
# // 26/02/2025 10:25:54  
# // (c) 2025 Juan M. Casillas <juanm.casillas@gmail.com>
# //
# /////////////////////////////////////////////////////////////////////////////

import socket
import copy
import requests
import time
from datetime import timedelta
import sys

sys.path.append('..')
from inframon.check import CheckBase, CheckStatus
from inframon.literals import *

class Check(CheckBase):
    def __init__(self, config, plugin_config):
        super().__init__("http", config, plugin_config)
            
    # run the test, and get some data.

    def run(self, node, **args):
        
        # try to override check configuration with
        # node local one, if found.
        cfg = copy.copy(self.plugin_config)
        if 'config' in node['checks'][self.name]:
            for k in node['checks'][self.name]['config'].keys():
                cfg[k] = node['checks'][self.name]['config'][k]


        results =  {
            'timeout': 0,
            'avg': 0.0,
            'count': int(cfg["count"]),
            'good': 0,
            'status': NODESTATUS.ALIVE
        }

        for i in range(results["count"]):
            try:
                ts = time.monotonic()
                
                session = requests.Session()
                session.trust_env = False

                response = session.get(cfg['url'], timeout=cfg['timeout'])
                te = time.monotonic()
                td = timedelta(seconds=te-ts).total_seconds()*1000.0
                
                if response.status_code in [ 200, 302 ]:
                    results['avg'] += td
                    results['good'] += 1
                else:
                    pass
            except Exception as e:
                results['timeout'] += 1
            
        results['avg'] = results['avg'] / int(results["count"])

        if results['good'] != results["count"]:
            results['status'] = NODESTATUS.FAIL

        return results
