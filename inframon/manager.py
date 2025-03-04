##!/usr/bin/env bash
# -*- coding: utf-8 -*-
# /////////////////////////////////////////////////////////////////////////////
# //
# // manager.py
# //
# // Manages the trackvis application (backend and frontend)
# // at high level
# //
# // 26/11/2024 11:38:36
# // (c) 2024 Juan M. Casillas <juanm.casillas@gmail.com>
# //
# /////////////////////////////////////////////////////////////////////////////

import logging
import logging.handlers
import configparser
import sys
import shutil
import json
import math
import os.path
import datetime
import traceback
import importlib
import time
import sqlite3
from pprint import pprint 


from inframon.appenv import *
from inframon.timing import *
from inframon.literals import *
import threading

class Manager:
    LOG_NAME = "InfraMon"

    def __init__(self, config):
        self.config = config
        self.verbose = self.config.verbose
        self.logger = logging.getLogger()
        self.db = None

        self.checks = {}
        self.nodes = {}
        self.refresh = 5000
        self.run_checks = 20000
        self.run_state = False

    def startup(self):
        self.configure_logger()
        self.connect_db()
        self.create_tables()
        self.load_scheduler()
        self.load_checks()
        self.init_nodes()
        

    def shutdown(self):
        """ends the execution, closes the database
        """
        self.db.close()
        raise SystemExit

    # database handlers

    def connect_db(self):
        self.db = sqlite3.connect("file:inframon?mode=memory&cache=shared", check_same_thread=False)
        #self.db = sqlite3.connect("inframon.db", check_same_thread=False)
        self.db.row_factory = sqlite3.Row 

    def create_tables(self):
        sql_prologue = [
            "drop table if exists nodes;",
            "drop table if exists checks;",
            "drop table if exists node_checks;",
        ]
        sql_epilogue = []

        sql_nodes = """
        create table nodes(
            id integer primary key AUTOINCREMENT,
            enabled integer not null default 1,
            name text not null,
            ip text not null default "-.-.-.-",
            mac text default "--:--:--:--:--:--",
            description text not null,
            lastmodified timestamp default CURRENT_TIMESTAMP,
            status integer not null default 0
        );
        """

        sql_checks = """
        create table checks(
            id integer primary key AUTOINCREMENT,
            type text not null,
            config text not null
        );
        """

        sql_node_checks = """
        create table node_checks(
            id integer primary key AUTOINCREMENT,
            node_id integer not null,
            check_id intenger not null,
            result text not null,
            stamp timestamp default CURRENT_TIMESTAMP,
            foreign key(node_id) references nodes(id),
            foreign key(check_id) references checks(id)
        );
        """
                
        cursor = self.db.cursor()

        for sql_sentence in sql_prologue:
            cursor.execute(sql_sentence)
        
        cursor.execute(sql_nodes)
        cursor.execute(sql_checks)
        cursor.execute(sql_node_checks)
        
        for sql_sentence in sql_epilogue:
            cursor.execute(sql_sentence)
        
        cursor.close()

    def insert_check_db(self, check):
        sql = "insert into checks(type, config) values ( ?, ? );"
        cursor = self.db.cursor()
        cursor.execute(sql, (check['type'], str(check['config'])))
        check['id'] = cursor.lastrowid
        self.db.commit()
        cursor.close()
        return check

    def insert_node_db(self, node):
        sql = "insert into nodes(enabled, name, ip, description, status) values ( ?, ?, ?, ?, ? );"
        cursor = self.db.cursor()
        cursor.execute(sql, (node['enabled'],
                             node['name'], 
                             node['ip'], 
                             node['description'],
                             node['status']))
        node['id'] = cursor.lastrowid
        self.db.commit()
        # for each check, get the DB id
        # "dictionary has changed in size"
        for check in node['checks'].keys():
            node['checks'][check]['id'] = self.checks[check]['id']

        cursor.close()
        return node

    def insert_result_db(self, node, check, result):
        sql = "delete from node_checks where node_id = ? and check_id = ?"
        cursor = self.db.cursor()
        cursor.execute(sql, (node['id'], self.checks[check]['id']))
        self.db.commit()

        sql = "insert into node_checks(node_id, check_id, result, stamp) values ( ?, ?, ?, CURRENT_TIMESTAMP );"
        cursor = self.db.cursor()
        cursor.execute(sql, (node['id'],
                             self.checks[check]['id'], 
                             json.dumps(result)))
        sql = "update nodes set lastmodified = CURRENT_TIMESTAMP where id = ?;"
        cursor.execute(sql, (node['id'],))
        self.db.commit()
        cursor.close()
        return node

    def get_node_status_db(self, query="",offset="",limit=0):

        sql = "select * from nodes"
        cursor = self.db.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        ret = []
        for node in rows:
            node = dict(node)
            node['checks'] = {}
            sql = """
                select c.*,nc.result, nc.stamp from checks as c, node_checks as nc where
                    nc.node_id = ? and nc.check_id = c.id
            """
            cursor2 = self.db.cursor()
            cursor2.execute(sql, (node['id'], ))
            rows2 = cursor2.fetchall()

            for results in rows2:
                node['checks'][results['type']] = json.loads(results['result'])
            cursor2.close()

            # add some configuration values not stored on db
            node['urls'] = self.nodes[node['id']]['urls']
            ret.append(node)
        cursor.close()

        return (ret,0,0)

    def update_field_db(self, table, id, attr, value):
        if value == None:
            return False
        
        sql = "update %s set %s = ? where id = ?;" % (table, attr)
        cursor = self.db.cursor()
        cursor.execute(sql, (value, id))
        self.db.commit()
        cursor.close()
        return(True)
    
    def update_node_field_db(self, id, attr, value):
       return self.update_field_db("nodes",id, attr, value)

    ## 
    def configure_logger(self):

        self.logger.setLevel(self.config.logs["level"])
        log_formatter = logging.Formatter(self.config.logs["format"])
        # rootLogger = logging.getLogger()

        if not os.path.exists(self.config.logs["app"]):
            logpath = os.path.dirname(self.config.logs["app"])
            os.makedirs(logpath, exist_ok=True)

        file_handler = logging.FileHandler(self.config.logs["app"])
        file_handler.setFormatter(log_formatter)
        self.logger.addHandler(file_handler)

        #consoleHandler = logging.StreamHandler()
        #consoleHandler.setFormatter(log_formatter)
        #self.logger.addHandler(consoleHandler)

    ## working methods

    def load_scheduler(self):
        self.refresh = float(self.config.scheduler['refresh'])
        self.run_checks = float(self.config.scheduler['run_checks'])

    def load_checks(self):
        for c in self.config.checks:
       
            spec = importlib.util.spec_from_file_location(c['type'], c["module"])
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            c = self.insert_check_db(c)

            self.checks[c['type']] = c
            self.checks[c['type']]['plugin'] = module.Check(self.config, c['config'])

            
            
    def init_nodes(self):
        for n in self.config.nodes:
            n['status'] = NODESTATUS.UNKNOWN
            self.insert_node_db(n)
            self.nodes[n['id']] = n


    def show(self):
        print("Scheduler")
        print(" - refresh (ui): %3.3f ms" % self.refresh)
        print(" - run_checks: %3.3f ms" % self.run_checks)
        print("Checks")
        for c in self.checks.keys():
            print(" - %s Config: %s" % (c,self.checks[c]))

        print("Nodes")
        for nk,n in self.nodes.items():
            print(" - %s %s %s" % (n['ip'], n['name'], n['status']))

    # businness

    def process_results(self, node, check, ret):
        # map attrs
        if "map_attributes" in self.checks[check].keys():
            for attr in self.checks[check]["map_attributes"]:
                from_attr = attr[0]
                to_attr = attr[1]
                self.update_node_field_db(node['id'], to_attr,  ret[from_attr])

    # run checks

    def run_once(self):
        for nodek,node in self.nodes.items():
            enabled = True if 'enabled' in node and node['enabled'] else False
            print("working on node", node['name'], node['id'])
            if not enabled:
                continue

            node_state = NODESTATUS.UNKNOWN
            changed = 0
            
            for check in node['checks'].keys():
                if not check in self.checks:
                    raise ValueError("check '%s' is not implemented" % check)
                
                print(" * working on check", check)
                # run the check
                c = self.checks[check]
                ret = c['plugin'].run(node)
                # store info in db
                self.insert_result_db(node, check, ret)
                self.process_results(node, check, ret)
                #node['checks'][check]['data'] = ret
                if ret['status'] != NODESTATUS.ALIVE:
                    node_state = NODESTATUS.FAIL
                    changed += 1
            # update node state.
            if changed == 0:
                node_state = NODESTATUS.ALIVE
            else:
                pass
            self.update_node_field_db(node['id'], 'status',  node_state)


    def run_once_wrapper(self):
        self.run_once()
        ##self.show_nodes()
        
    def run_forever_wrapper(self):
        while self.run_state:
            try:
                self.run_once_wrapper()
                time.sleep(self.run_checks * (1/1000.0))
            except KeyboardInterrupt:
                return
            except Exception as e:
                print("run_forever_wrapper: %s" % e)
                sys.exit(0)


    def run(self, detached=False, forever=False):
        print("run forever")
        self.threads = []
        self.run_state = True
        if forever:
            thread = threading.Thread(target=self.run_forever_wrapper)
        else:
            thread = threading.Thread(target=self.run_once_wrapper)
        thread.start()
        self.threads.append(thread)
        # wait to end
        if not detached:
            for thread in self.threads:
                thread.join()

    def show_nodes(self):
        # show DB nodes, and results instead configurated ones.
        nodes = self.get_node_status_db()
        pprint(nodes)    

        # for node in self.nodes:
        #     enabled = True if 'enabled' in node and node['enabled'] else False
        #     print("%s %s: %s" % (node['enabled'], node['ip'], node['name']))
        #     for check in node['checks'].keys():
        #         print(" -> %s %s" % (check, node['checks'][check]['status']))
