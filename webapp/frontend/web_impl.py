# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

from flask import Blueprint, render_template, \
                  flash, redirect, url_for, current_app, request, Response, \
                  after_this_request, send_file, jsonify, \
                  send_from_directory



#from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from markupsafe import escape

import flask
import traceback
import logging
import os
import sys
import time
import json
import html
from webapp.caching import cache
from inframon.helpers import remove_accents

web_impl = Blueprint('web_impl', __name__)

#remove after touch the JS files (in static path)
#@web_impl.route('/static/<path>')
#@cache.cached(timeout=60*60*24)  # Cache for 24 hours
def static_files(path):
    return send_from_directory('static', path)

# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.

@web_impl.route('/')
def index():
    return redirect(url_for('web_impl.monitor'))

@web_impl.route('/error', methods=['GET', 'POST'])
def error():
    msg = request.args.get("msg","Unknown error")
    return render_template('error.html',msg=msg)

# page handlers


@web_impl.route('/dashboard.html', methods=['GET'])
def tracks_dashboard():

    return render_template('dashboard.html')





@web_impl.route('/nodes/query', methods=['GET','POST'])
def nodes_query():
    
    # process both entries (get and post)
    query = request.args.get("query",None)
    offset = int(request.args.get("offset",0))
    limit = int(request.args.get("size",0))

    if 'query' in request.form.keys():
        query = request.form['query']

    if 'offset' in request.form.keys():
        offset = request.form['offset']
        offset = int(offset)
    
    if 'limit' in request.form.keys():
        limit = request.form['limit']
        limit = int(limit)

    input_query = ""
    if query is None or query == "":
        query = current_app.manager.config.queries['default']
        offset = 0
        limit = 0
    else:
        query = html.unescape(query)
        query = remove_accents(query)
        input_query = query
                
    #current_app.logger.info("Parsed query: <%s> (limit: %d, offset: %d)" % (query,limit,offset))
    
    try:
        nodes, pagination, data_len = current_app.manager.get_node_status_db(query=query, offset=offset, limit=limit)
    except Exception as e:
        return jsonify(error = True,
                        text = 'bad query: %s' % e,
                        code = 2,
                        nodes = [])

    return jsonify(error = False,
                   text = 'success',
                   code = 0,
                   pagination = pagination,
                   total_size = data_len,
                   nodes = nodes,
                   query = input_query)










@web_impl.route('/monitor.html', methods=['GET'])
def monitor():

    query = request.args.get("query",None)
    if query is None:
        query = ""
    else:
        query = html.unescape(query)

    offset = request.args.get("offset",0)
    limit = request.args.get("limit",0)
 
    nodes, offset, limit = current_app.manager.get_node_status_db(query=query, offset=offset, limit=limit)
    return render_template('monitor.html',
                           nodes=nodes, query=query, offset=offset, limit=limit,
                           scheduler=current_app.manager.config.scheduler)




# json handlers
