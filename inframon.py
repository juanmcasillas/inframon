##!/usr/bin/env bash
# -*- coding: utf-8 -*-
# /////////////////////////////////////////////////////////////////////////////
# //
# // app.py 
# //
# // manage the command line app (ingest)
# //
# // 26/11/2024 11:40:36  
# // (c) 2024 Juan M. Casillas <juanm.casillas@gmail.com>
# //
# /////////////////////////////////////////////////////////////////////////////

import argparse
import sys

import inframon.timing
from inframon.appenv import *
from inframon.manager import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Show data about file and processing", action="count", default=0)
    parser.add_argument("-c", "--config-file", help="Configuration File", default="conf/inframon.json")
    parser.add_argument("-1", "--once", help="Runs only once. by default, forever", action="store_true", default=False)
    
    args = parser.parse_args()

    AppEnv.config(args.config_file)
    AppEnv.config_set("verbose",args.verbose)

    manager = Manager(AppEnv.config())
    manager.startup()

    
    if AppEnv.config().verbose:
        manager.show()

    # run once
    
    if args.once:
        manager.run_once()
        manager.show_nodes()
    else:
        manager.run_forever()
    manager.shutdown()
