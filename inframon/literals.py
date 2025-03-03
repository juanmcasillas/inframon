##!/usr/bin/env bash
# -*- coding: utf-8 -*-
# /////////////////////////////////////////////////////////////////////////////
# //
# // literals.py 
# //
# // 
# //
# // 26/02/2025 10:48:20  
# // (c) 2025 Juan M. Casillas <juanm.casillas@gmail.com>
# //
# /////////////////////////////////////////////////////////////////////////////

class ADDR:
    EMPTY_IP = "-.-.-.-"
    EMPTY_MAC = "--:--:--:--:--:--"
    BCAST_MAC = "ff:ff:ff:ff:ff:ff"

    def __init__(self):
        pass

class NODESTATUS:
    UNKNOWN     = "UNKNOWN" 
    ALIVE       = "ALIVE"   
    FAIL        = "FAIL"    

    NUM = {
        UNKNOWN: 0,
        ALIVE:   1,
        FAIL:    2
    }

    def __init__(self):
        pass
