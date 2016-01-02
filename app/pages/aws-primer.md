title: AWS Primer
timestamp: 2015-06-04 08:49:36
slug: aws-primer
tags: [amazon-web-services, aws, beginning-aws, cloud-computing]
author: Matt Healy

When I first started investigating <a href="http://aws.amazon.com/">Amazon Web Services</a> as an option for hosting our web-based software at work, I was initially overwhelmed with the sheer amount of services available. EC2, ELB, EBS, RDS, S3, so many acronyms! What do they all mean, and how do they correspond to a setup on physical hardware? I would have loved to read a plain English explanation of all these options and how they all piece together, so I'm writing this post so that it can be of use to someone else dipping their toes in the AWS pool.

First off, it's useful to understand *Regions* and *Availability Zones*. AWS currently offers its services in nine regions, spread across the U.S., E.U., Asia Pacific and South America (with a special "Isolated Region" in China and another for U.S. Government services). Within each region there are two or more Availability Zones (AZ). AZ's are designed in such a way as to be geographically isolated from each other, to minimise the chance of downtime in a particular region. You would typically choose to provision your services in a particular region to minimise latency for your customers. Within that region, you can make use of Availability Zones to ensure the greatest uptime possible for your application. This can include strategies such as deploying your entire application across both AZ's, so that if one AZ was to suffer a total outage, your application will stay up.

With that in mind, let's look at a quick rundown of the main services you'd likely use with AWS:

##EC2

Elastic Cloud Compute (EC2) is akin to a "virtual server" that you might use with other hosting providers. You can choose the type of EC2 instance you use, according to the amount of CPU, memory and storage space you need.

Although an EC2 instance is like a virtual server, there is a different mindset when it comes to Amazon (and indeed cloud computing in general). You need to consider an EC2 server as being stateless and temporary - you need to expect the server to suddenly be unavailable and your application needs to have logic to work around this. By not storing any application state on an EC2 instance, you have the freedom to start and stop servers at will, without disrupting your users or losing any data.

##EBS

Elastic Block Storage (EBS) is like a virtual hard drive. You can provision a volume of any size as required, and attach the volume to an EC2 instance. An EBS volume can be attached to only one EC2 instance at a time, but an EC2 instance can have many volumes attached.

##ELB

An Elastic Load Balancer (ELB) allows you to group together multiple EC2 instances and balance traffic to them evenly. This is a fantastic tool to allow your application to scale effectively and be resilient to failures. By spreading the instances behind a load balancer evenly across your Availability Zones, your application becomes protected against a single AZ going down.

##S3

Amazon's Simple Storage Service is an "object" store - quite simply, you can upload objects, usually user-defined resources like images, videos and documents, to a "bucket" and access them via a URL or API call. S3 scales massively, meaning that you can effectively upload as many objects as you want, and only pay for what you use.

##Glacier

Glacier is a similar service to S3, but it is used more for archiving purposes rather than object storage. The service is incredibly cheap, but this comes with a trade-off of slow access speeds. If you need to retrieve an existing archive, it could be anywhere upwards of four hours before you obtain your data.

##RDS

Amazon offers a managed Relational Database Service (RDS), allowing you to host your SQL databases (MySQL, Postgresql, SQL Server) in a managed and controlled environment. This is fantastic for developers who either don't want to or cannot devote the time to being an expert in database administration. RDS manages backups and redundancy for you with the click of a button.

##IAM

Identity Access Management (IAM) is a crucial but often overlooked part of the AWS platform. IAM is where you define who has access to your Amazon resources, what they have access to, and so on. Best practice is to create a login for each user (so they aren't sharing credentials to the "root" or "master" account), and assign them only the minimum permissions they need. For example, you might grant your developers the permissions needed to create new EC2 instances for test purposes, but not to terminate any EC2 instances. Setting up your IAM is super important - there are many horror stories out there where an attacker was able to gain access to the root login of a company's Amazon account and wipe away all data and all backups, effectively destroying the company instantaneously. 

If you or your company is looking for advice on getting started with AWS, or looking to audit their current setup, feel free to get in touch with me.
