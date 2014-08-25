from flask import render_template, jsonify, request
from agency import agency
import MySQLdb as mdb
import numpy as np
from saving import load_sparse_csr, unpickle
import redis
from json import loads, dumps
from secret import pw

db = mdb.connect("localhost", "iva", pw, db="Ravelry", charset='utf8')
q = redis.Redis(unix_socket_path='/var/run/redis/redis.sock')
username_list = set(unpickle('username_list'))

@agency.route('/')
@agency.route('/index')
def index():
	return render_template("index.html")
        
@agency.route("/projects")
def projects_json():
	user = request.args.get('username')
	if user in username_list:
		craft = request.args.get('craft')
		category = request.args.get('category')
		q.rpush("tasks", dumps([user, craft, category]))
		recs = loads(q.blpop("results")[1].decode('utf-8'))
		with db:
			cur = db.cursor()
			# FIX IT: The order of recommendations is not preserved:
			cur.execute("SELECT pattern_name, pattern_id, pattern_photo FROM Photos WHERE pattern_id IN (%s,%s,%s,%s,%s);", tuple(recs))
			base_url = 'http://www.ravelry.com/patterns/library/'
			projects = []
			for name in cur:
				projects.append(dict(name="<a href={0}{1}>{2}</a>".format(base_url, name[1], name[0].encode('utf-8')), pic="<img src={0}>".format(name[2])))
			return jsonify(projects=projects)
	else:
		error = []
		error.append({'pic' : 'Invalid Username', 'name': ''})
		return jsonify(projects=error)
 
@agency.route("/jquery")
def index_jquery():
    return render_template('index.html')


