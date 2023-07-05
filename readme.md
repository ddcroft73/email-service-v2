### Email Micro Service V2

Its pretty much the same service as before but a bit cleaner. I changed the file structure and this time I opted to use a docker-compose setup instead of a venv and 2 shell files to start it all up. THis way I just list all my services in the YAML file and build\run it and they just spin up like magic. This will be a service that I use on all my web projectst to send emails. It will be used to send plain text as well as HTML Emails. The main purpose will be verify Email emails, reset password emails, and anything pertaining to the apps core function. I'm going to use fastAPI to build the server, and I will also use CElery.

#### Tech Stack:
fastAPI<br>
Celery<br>
Redis<br>
Docke Compose<br>
Celert Flower

SMTP Email functionality built using python email wrapped in a simple class.


#### Purpose:
Send Emails. Thats it. It will have one endpoint. I may need to add another/others when I totally figure out exactly what I am doing.  

#### EndPoint:
/send-email/


#### Request Model:

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
#### Response Model:

```
{
  "result": "string"
}
```
#### Workflow

1. A request is sent to the server along with an dictionary carrying all the nedded info.
2. The server verifies the clients credentials via dependencies; the data within will have been validated before it ever leaves the client as to limit the amount of work this service has to do.
3. The email dictionary is seralized into an object, and passed to the Celery task predefined to handle sending emails.
4. A response is sent back to the client with the task ID confirming that the email is being processed.
5. The email is then dispatched on a FIFO basis.

Celery can be monitired at:[`http://0.0.0.0/5556/`](http://0.0.0.0/5556/). 
This file can be viewd at: [`http://0.0.0.0/8014/`](http://0.0.0.0/8014/). 
Documentation on the API Schema can be found at: [`http://0.0.0.0/8014/Docs/`](http://0.0.0.0/8014/Docs/). 

#### Run Service:
- clone the repo
- cd into da repo
- $ docker-compose up

#### TODO:
- Get the Celery portion, `tasks` finalized:
  It works fine forwhat it is, and what I need. Decide if the class is worth it or just keep the function. 
- For gods sake figure out logger!! Like why the hell does it only ever halfway work!? Maybe it's got something to do with
  how the modules are loading as to why Only info works and not error, vice versa, and why I can't ever get it to consistently write to file!!   
- Build the Info Web Page.
- Make sure the error handling is up to snuff. As is I really only know about `try: except:`. 
- Make the tests hard core. I currently only have one that fires requests at the endpoint.
