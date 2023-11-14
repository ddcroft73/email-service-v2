## Notification Micro Service V2

<p>
  A straightforward no-frills email service built to facilitate email communication for all of my web applications. Currently, as I am still in the process of building the application(s), this service operates independently as the second iteration. I am going to incorporate an sms service into this service as well.
  Instead of Email, it's now Notifications.
</p>

<p>
  I developed it to run within a <a href="https://www.docker.com/">Docker</a> container using <a href="https://docs.docker.com/compose/">Docker Compose</a>. In the initial <a href="https://github.com/ddcroft73/email-service">version</a>, the API was built within a virtual environment (venv) and required launching through two shell scripts. The second script was used to launch the <a href="http://www.celeryproject.org/">Celery</a> worker(s). However, I wasn't satisfied with this approach, so I took the initiative to learn how to use Docker Compose, and in the meantime have become a bit facsinated with it.
</p>

<p>
  The service employs Celery to handle email delivery, essentially receiving a request, forwarding it, and awaiting the next request. I have conducted thorough testing, although I am still in the process of mastering proper testing methodologies such as Test-Driven Development (TDD). Currently, my testing involves a script that repeatedly sends requests to the endpoint, including scenarios designed to cause failures. Remarkably, even without Celery, the application handles these situations gracefully. I attribute this success to the robustness of <a href="https://fastapi.tiangolo.com/">FastAPI</a>, and I must acknowledge the brilliance of FastAPI's design, not my own.
</p>


### Tech Stack:
[FastAPI](https://fastapi.tiangolo.com)<br>
[Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)<br>
[Redis](https://redis.io) <br>
[Docker Compose](https://docs.docker.com/compose/) <br>
[Celery Flower](https://flower.readthedocs.io/en/latest/index.html)<br>


### Purpose:
Send Emails and sendind SMS text messages. I plan to use this with my email gateway to send text messages to users and on the behalf of users. I have decided
to incorporate both to be used with the Life Package SaaS.

### EndPoints:
`/ ` - Root or index. Loads index.html. A React page (I use the CDN files not an actual React App, all components are in index.html) built to emulate this readme file.

`/send-email/ ` - Send emails with Celery

`/send-async/`  - Send emails asynchronusly

`/send-sms/`  - Coming soon...


### Request Model:

```
{
  email_to: "string",
  email_from: "string",
  subject: "string",
  message: "string,
  user_id: "string"
}

```
I am still working on the SMS portion. Not 100 on the Request and response models as of yet.
### Response Model:

```
{
  "result": "string"
}
```

### API DEV Logger:

I built a simple logging class to help me debug and log certain details. Its more simple and not as robust as the Python logger but it is easier to use.
It lets you designate a file to send the log entry to and gives the API am interface so to speak. I use a singelton pattern and where needed import the object
and call the desired method. The output goes to a predefined location. It's great for logging errors and debugging. 

This Logger will remain, but for production I plan to implement a better solution with asynchronous support. I don't want to miss log entries because
requests come in to fast, and without a better logger, it's inevitable.

```
from app.utils.api_logger import logzz
logzz.info("info message here.")
```
### Logger "streams"

INFO<br>
ERROR<br>
DEBUG<br>
WARNING<br>

### Email Support

SMTP Email functionality built using python email wrapped in a simple class. Thats all I needed. It performs well under testing. I can fire 1000 emails at it. many concurrently and it never misses a beat. A lot of this may in part to the way celery deals with the tasks. I have not done much testing on the `send-async` function. I just haven't had time. I included it because, why not? 

### SMS Support

SMS support will be realized through the email gateway. I will setup a dedicated address once I get my domain, and email hostinf setup. The only difference
anyone from the outside will see is the From: section. Instead of a phone number it will simply read `sms@lifepackage.app` or something similar. The Texts
will be free for me and users of the system. In the event that a user employs this method of contact in their package, it will simply one-way. However
if someone is so inclined, they can send an email to the address. It will probably go unanswered.

### Workflow:
1. **Initiation of Request**: A client initiates a service request by transmitting data in JSON format to the email API endpoint.
2. **Request Processing**: Upon receipt, the API validates and forwards the request to a designated Celery task queue for asynchronous processing.
3. **Acknowledgment Response**: Concurrently, the client is issued an immediate acknowledgment response, confirming the initiation of the email sending process.
4. **Task Allocation**: This task enters the Celery queue and awaits allocation to the next available worker node, adhering to a First-In-First-Out (FIFO) scheduling protocol.
5. **Execution and Email Dispatch**: Once allocated, the Celery worker executes the task, culminating in the dispatch of the email as per the queued instruction.

THis system can handle many tasks concurrently and with the use of Celery it fires them like clockwork.
<br><br>

Celery can be monitired at:[`http://0.0.0.0/5556/`](http://0.0.0.0/5556/). <br>
This file can be viewd at: [`http://0.0.0.0/8014/`](http://0.0.0.0/8014/). <br>
Documentation on the API Schema can be found at: [`http://0.0.0.0/8014/Docs/`](http://0.0.0.0/8014/Docs/). <br>

### Run Service: 

- `$ git clone https://github.com/ddcroft73/email-service-v2.git`
- `$ cd intoDirectoryClonedInto`
- `$ docker-compose up`
