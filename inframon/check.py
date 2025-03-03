##!/usr/bin/env bash
# -*- coding: utf-8 -*-
# /////////////////////////////////////////////////////////////////////////////
# //
# // checks.py 
# //
# // 
# //
# // 26/02/2025 10:31:09  
# // (c) 2025 Juan M. Casillas <juanm.casillas@gmail.com>
# //
# /////////////////////////////////////////////////////////////////////////////



class CheckBase:
    def __init__(self, name, config, plugin_config):
        self.name = name
        self.config = config
        self.plugin_config = plugin_config
       

    def run(self, host, **args):
        raise NotImplementedError
    
class CheckStatus:
    def __init__(self, **args):
        for i,j in args.items():
            self.__dict__[i] = j
        
    def ret(self, dict):
        print(args)
        sys.exit(0)
        for i,j in args.items():
            self.__dict__[i] = j        
        return self

    def __str__(self):
        return str(self.__dict__)