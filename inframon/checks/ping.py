##!/usr/bin/env bash
# -*- coding: utf-8 -*-
# /////////////////////////////////////////////////////////////////////////////
# //
# // ping.py 
# //
# // implement the ping check
# //
# // 26/02/2025 10:25:54  
# // (c) 2025 Juan M. Casillas <juanm.casillas@gmail.com>
# //
# /////////////////////////////////////////////////////////////////////////////

import socket
import copy
import ping3

from scapy.all import getmacbyip
import sys

sys.path.append('..')
from inframon.check import CheckBase, CheckStatus
from inframon.literals import *

class Check(CheckBase):
    def __init__(self, config, plugin_config):
        super().__init__("ping", config, plugin_config)
            
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
            'unknown': 0,
            'ttlexp': 0,
            'avg': 0.0,
            'count': int(cfg["count"]),
            'macaddr': None,
            'good': 0,
            'status': NODESTATUS.NUM[NODESTATUS.ALIVE]
        }

        ip = node['ip']
        try:
            ip_addr = socket.gethostbyname(ip)
        except Exception as e:
            results['status'] = NODESTATUS.NUM[NODESTATUS.UNKNOWN]
            return results

        try:    
            macaddr  = getmacbyip(ip_addr)
        except Exception as e:
            results['status'] = NODESTATUS.NUM[NODESTATUS.UNKNOWN]
            return results

    
        results['macaddr'] = macaddr
        ping3.EXCEPTIONS = True


        for i in range(results["count"]):
            try:
                icmp_data = ping3.ping(ip_addr,
                                timeout=cfg["timeout"], 
                                unit=cfg["units"])
                if icmp_data != None:
                    results['avg'] += icmp_data 
                    results['good'] += 1
            except ping3.errors.Timeout as e:
                results['timeout'] += 1
            except ping3.errors.HostUnknown as e:
                results['ttlexp'] += 1
            except ping3.errors.TimeToLiveExpired as e:
                results['avg'] += 1

        results['avg'] = results['avg'] / int(results["count"])

        if results['good'] != results["count"]:
            results['status'] = NODESTATUS.NUM[NODESTATUS.FAIL]

        # rtt may be 0.0 (ms)
        return results
            

        