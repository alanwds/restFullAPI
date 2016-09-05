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
	'docker-image': u'image x',
	'env-variables': u'ENV Variables',
        'status': u'scheduled'
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
	'date-time': u'2016-09-10-00:00:00',
	'docker-image': u'image Y',
        'env-variables': u'ENV Variables',
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

#Funtion to create a job
def create_job():

	#Parser to avoid uncomplete requests
	if not request.json or not 'title' in request.json:
		abort(400)
	job = {
		'id': jobs[-1]['id'] + 1,
		'title': request.json['title'],
		'date-time': request.json['date-time'],
		'docker-image': request.json['docker-image'],
		'env-variables': request.json['env-variables'],
		'status': u'scheduled'
	}
	
	#Add the job to job arrays
	jobs.append(job)

	#Return the job detail and the code 201 (created)
	return jsonify({'job': job}), 201

#Callback to set a job as finished
@app.route('/jobMan/v1.1/jobs/<int:job_id>/callback', methods=['PUT'])

#Function to update job status
def update_job(job_id):

        job = [job for job in jobs if job['id'] == job_id]
	job[0]['status'] = u'finished'
	return jsonify({'job': job[0]})

		
if __name__ == '__main__':
	app.run(debug=True)
