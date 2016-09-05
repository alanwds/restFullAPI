#!/usr/bin/python2.7

#Import flask module
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

jobs = [
    {
        'id': 1,
        'title': u'Reprocessing data',
        'description': u'job to treprocessing data for a given period', 
	'date-time': u'2016-09-10-00:00:00',
        'status': u'scheduled'
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
	'date-time': u'2016-09-10-00:00:00',
        'status': u'running'
    }
]

#Define an error handler
@app.errorhandler(404)

def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#INDEX (like a help)
@app.route('/')

def index():
	return "Welcome to Job Manager v1.1.\nPlease, check the correct syntax for use this API"

#JOB LIST
@app.route('/jobMan/v1.1/jobs', methods=['GET'])

def get_tasks():
    return jsonify({'jobs': jobs})

#JOB STATUS
@app.route('/jobMan/v1.1/jobs/<int:job_id>/status', methods=['GET'])

#Funcion to filter and show only the specified job id
def get_Job(job_id):

	#Run the array until find job id
	job = [job for job in jobs if job['id'] == job_id]

	#If job id is not found, the error 404 will be returned
	if len(job) == 0:
		abort(404)
	return jsonify({'job': job[0]})

#JOB INSERT
@app.route('/jobMan/v1.1/jobs/schedule', methods=['POST'])

if __name__ == '__main__':
	app.run(debug=True)
