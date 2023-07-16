## Email Micro Service V2

<p>
  This is a straightforward no-frills email service built to facilitate email communication for all of my web applications. Currently, as I am still in the process of building the application(s), this service operates independently. Second iteration.
</p>

<p>
  I developed it to run within a <a href="https://www.docker.com/">Docker</a> container using <a href="https://docs.docker.com/compose/">Docker Compose</a>. In the initial <a href="https://github.com/ddcroft73/email-service">version</a>, the API was built within a virtual environment (venv) and required launching through two shell scripts. The second script was used to launch the <a href="http://www.celeryproject.org/">Celery</a> worker(s). However, I wasn't satisfied with this approach, so I took the initiative to learn how to use Docker Compose, and in the meantime have become a bit facsinated with it.
</p>

<p>
  The service employs Celery to handle email delivery, essentially receiving a request, forwarding it, and awaiting the next request. I have conducted thorough testing, although I am still in the process of mastering proper testing methodologies such as Test-Driven Development (TDD). Currently, my testing involves a script that repeatedly sends requests to the endpoint, including scenarios designed to cause failures. Remarkably, even without Celery, the application handles these situations gracefully. I attribute this success to the robustness of <a href="https://fastapi.tiangolo.com/">FastAPI</a>, and I must acknowledge the brilliance of FastAPI's design, not my own.
</p>

### Tech Stack:
[fastAPI](https://fastapi.tiangolo.com)<br>
[Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)<br>
[Redis](https://redis.io) <br>
[Docker Compose](https://docs.docker.com/compose/) <br>
[Celery Flower](https://flower.readthedocs.io/en/latest/index.html)<br>
Custom Logger
  - Built a logger escpecially designed to work fluently with this application type.
  - Easy to use with self archiving so logs can be kept as reference points for any scenario.
    - INFO
    - ERROR
    - DEBUG
    - WARNING
    
    For me, this is a better logger than Pythons logger. But it's not exactly the same. Built for a specific use case.

SMTP Email functionality built using python email wrapped in a simple class.


### Purpose:
Send Emails. Thats it. It will have one endpoint. I may need to add another/others when I totally figure out exactly what I am doing.  

### EndPoint:
/send-email/


### Request Model:

```
{
  email_to: "string",
  email_from: "string",
  subject: "string",
  message: {
    text: "string",
    html: "string
  }
}
```
### Response Model:

```
{
  "result": "string"
}
```
### Workflow

1. A request is sent to the server along with an dictionary carrying all the nedded info.
2. The server verifies the clients credentials via dependencies; the data within will have been validated before it ever leaves the client as to limit the amount of work this service has to do.
3. The email dictionary is seralized into an object, and passed to the Celery task predefined to handle sending emails.
4. A response is sent back to the client with the task ID confirming that the email is being processed.
5. The email is then dispatched on a FIFO basis.

Celery can be monitired at:[`http://0.0.0.0/5556/`](http://0.0.0.0/5556/). <br>
This file can be viewd at: [`http://0.0.0.0/8014/`](http://0.0.0.0/8014/). <br>
Documentation on the API Schema can be found at: [`http://0.0.0.0/8014/Docs/`](http://0.0.0.0/8014/Docs/). <br>

### Run Service: 

- `$ git clone https://github.com/ddcroft73/email-service-v2.git`
- `$ cd intoDirectoryClonedInto`
- `$ docker-compose up`

### TODO:
- Make the tests more hard core. I currently only have one that fires requests at the endpoint.
- Testing.... and I'm done.
