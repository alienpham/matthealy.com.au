title: Using Supervisor with Flask and Gunicorn
timestamp: 2015-09-28 03:51:09
slug: using-supervisor-with-flask-and-gunicorn
tags: [flask, amazon-web-services, aws, ec2, deployment, devops, python, supervisor, gunicorn]
author: Matt Healy

In my <a href="/blog/post/deploying-flask-to-amazon-web-services-ec2/">last blog post</a> we looked at how to deploy our Flask application using Gunicorn on Amazon's EC2 service. That blog post was more focused on getting a very simple test case up and running, but one thing we didn't cover in detail was how best to manage our Gunicorn process.

If you recall from the previous post, we set up our server with Nginx acting as the web server listening for traffic on port 80, which forwarded requests to our Flask application server (Gunicorn) running on port 8000. This works well, except for the fact that we aren't really looking after our Gunicorn process. A Gunicorn process can die because of a coding error, or perhaps some other external factor. We also want our Gunicorn process to start again in the event of a reboot. 

To kick things off, let's install supervisord:

    [ec2-user@ip-172-31-6-157 ~]$ sudo pip install supervisor --pre

We need to set the configuration for supervisor. First, run the following command:

    [ec2-user@ip-172-31-6-157 ~]$ echo_supervisord_conf

This should print out a sample configuration file to your terminal. Let's use this as the basis for our configuration.

    [ec2-user@ip-172-31-6-157 ~]$ sudo bash -c '/usr/local/bin/echo_supervisord_conf > /etc/supervisord.conf'
    [ec2-user@ip-172-31-6-157 ~]$ sudo vi /etc/supervisord.conf

At the very bottom of the script, add the following block and adjust to suit your application.

    [program:myapp]
    command = /home/apps/.virtualenvs/myapp/bin/python /home/apps/.virtualenvs/myapp/bin/gunicorn app:app -b localhost:8000
    directory = /home/apps/myapp
    user = apps
    autostart=true                ; start at supervisord start (default: true)
    autorestart=true                ; whether/when to restart (default: unexpected)

Save the file, and now let's start supervisor. We want supervisor to start automatically at boot time, so we will need an init script for this. Supervisor doesn't usually come packaged with an init script, but you can download one from <a href="https://gist.githubusercontent.com/MattHealy/a3772c19b6641eb3157d/raw/06932656e8a173e91e978468a10d837a69a1ecfa/supervisord">this link</a>.

    [ec2-user@ip-172-31-6-157 ~]$ cd /etc/init.d
    [ec2-user@ip-172-31-6-157 init.d]$ sudo bash -c 'wget https://gist.githubusercontent.com/MattHealy/a3772c19b6641eb3157d/raw/06932656e8a173e91e978468a10d837a69a1ecfa/supervisord'
    [ec2-user@ip-172-31-6-157 init.d]$ sudo chmod +x supervisord
    [ec2-user@ip-172-31-6-157 init.d]$ sudo chkconfig --add supervisord
    [ec2-user@ip-172-31-6-157 init.d]$ sudo /etc/init.d/supervisord start

The above commands ensure that every time the machine is restarted, supervisor will start automatically, and in turn will start our Gunicorn process for serving our Flask app.
