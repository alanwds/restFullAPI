# restFullAPI for schedule docker image provising (AWS)
#README

IMPORANT: I'm just started the code. There are a lot of problems and things to do. Please, be careful with that.

[description]
A simple implementation of a restFull API using python for schedule jobs. The initial goal is schedule docker images provising in a AWS EC2 machine.

#API DETAILS

The API have the follow functions:

Schedule: POST - Parameters: imagem docker, date-time to run the job, ENV list.
list: GET - Get all scheduled jobs
status: status - Get job status
callback: PUT  - When job finish, this callback can be used to change job status

URL to access the service: http://[hostname]/jobMan/v1.1/

Resources:

Method	URI					Action
POST	jobMan/v1.1/jobs/schedule		Add a schudule job
GET	jobMan/v1.1/jobs			list all the jobs
GET	jobMan/v1.1/jobs/[job_id]/status	Show the status of specified job id
PUT	jobMan/v1.1/jobs/[job_id]/callback	Update job status when the job ins finished

Each job have the follows fields:

id: unique identifier for job. Numeric type.
title: short job description. String type.
date-time: Date time for job execution. String type.
docker-image: The docker image for the job. String type.
env-variables: Env Variables. String type.
status: status of the job. Text type.
 - scheduled	job scheduled (default)
 - running	job is running
 - finish	job is finished

#FILES

jobMan.py	Service to manager jobs

#DEPLOY
#Install flask
pip install flask
pip install apscheduler=2.1.2

#CURL commands to use API:

#List all jobs:
curl -i -XGET "http://127.0.0.1:5000/jobMan/v1.1/jobs"

#Get specific job status
curl -i -XGET "http://127.0.0.1:5000/jobMan/v1.1/jobs/$JOB_ID/status"

#Insert a job on schedule table (must have json application type on header)
curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Get the new job","date-time":"2016-09-06 17:25:10","docker-image": "image ABC","env-variables":"ENV variables"}' http://127.0.0.1:5000/jobMan/v1.1/jobs/schedule

#Callback to change status when job is finished
curl -i -H "Content-Type: application/json" -X PUT -d '{"status":finished}' http://127.0.0.1:5000/jobMan/v1.1/jobs/2/callback


#TODO
- Auth on API requests
- Call back for on time update job status
- Validation on some methods (for example on update_job)
- Add regex to validade inputs for the jobs
- Store sched.add_date_job for handler it in future
