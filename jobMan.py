#!/usr/bin/python2.7

#Import flask modules
from flask import Flask, jsonify, abort, make_response, request

#Import Scheduler modules
from apscheduler.scheduler import Scheduler

#Import date time module
import datetime

#Enable a fake debug module (just for watch script execution)
debug = 0

#Function to fake debug
def log(logEntry):
	if (debug == 0):
		print logEntry
	else:
		print 'Debug mode disable'


app = Flask(__name__)

log('Starting jobManager')


log('Starting scheduler')
#Inicia o scheduler
sched = Scheduler()
sched.start()


#Job examples
jobs = [
    {
        'id': 1,
        'title': u'Reprocessing data',
        'description': u'job to treprocessing data for a given period', 
	'date-time': u'2016-09-10 00:00:00',
	'docker-image': u'image x',
	'env-variables': u'ENV Variables',
        'status': u'scheduled'
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
	'date-time': u'2016-09-10 00:00:00',
	'docker-image': u'image Y',
        'env-variables': u'ENV Variables',
        'status': u'running'
    }
]

#Define an error handler
@app.errorhandler(404)

def not_found(error):
    log('Page note found error')
    return make_response(jsonify({'error': 'Not found'}), 404)


#####################API FUNCTIONS##########################

#INDEX (like a help)
@app.route('/')

def index():
	log('Requisition at root path')
	return "Welcome to Job Manager v1.1.\nPlease, check the correct syntax for use this API"

#JOB LIST
@app.route('/jobMan/v1.1/jobs', methods=['GET'])

def get_jobs():
    log('Listing all jobs')
    return jsonify({'jobs': jobs})

#JOB STATUS
@app.route('/jobMan/v1.1/jobs/<int:job_id>/status', methods=['GET'])

#Funcion to filter and show only the specified job id
def get_Job(job_id):

	log('Returning info about an especific job')
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

	log('Inserting a new job')
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
	
	#schedule job
	log('Scheduling job')
	sched.add_date_job(createEC2, request.json['date-time'],request.json['docker-image'])

	#Add the job to job arrays
	jobs.append(job)

	#Return the job detail and the code 201 (created)
	return jsonify({'job': job}), 201

#Callback to set a job as finished
@app.route('/jobMan/v1.1/jobs/<int:job_id>/callback', methods=['PUT'])

#Function to update job status
def update_job(job_id):

	log('Setting status finished for job_id')
        job = [job for job in jobs if job['id'] == job_id]
	job[0]['status'] = u'finished'
	return jsonify({'job': job[0]})

#####################/API FUNCTIONS##########################

#####################AWS FUNCTIONS##########################

def createEC2(dockerImage):
	date = datetime.datetime.now().time()
	print('Creating EC2 function started ati', date)
	print('Creating EC2 with',dockerImage)
		
if __name__ == '__main__':
	app.run(debug=True)
