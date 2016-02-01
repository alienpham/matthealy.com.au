title: S3 Sync - Danger!
timestamp: 2016-01-31 18:51:09
slug: s3-sync-danger
tags: [amazon-web-services, aws, s3, backup]
author: Matt Healy

I recently had to revisit the backup strategy for a web design business run by a friend of mine. The business only ran a single server, containing a MySQL database and Apache web server, serving about ten Wordpress websites for clients. We previously had a very simple backup script which ran every night. The script would create a tar archive of the entire htdocs area, and a MySQLdump of the database, and FTP it all across to an FTP account on a different server. This approach has a couple of drawbacks:

1. *It's insecure.* The data is sent across the Internet via an insecure protocol, FTP. This could have been remedied by using a secure file transfer protocol such as SFTP.

2. *It's inefficient.* Every night, we're sending an entire snapshot to the backup server. Obviously, there's a whole lot of data on the server that never changes, so there is really no need to back it up every night. To make things worse, the backup process takes longer and longer each night, as the amount of data on the server increases over time. We're needlessly wasting precious bandwidth with this solution. The ideal solution involves doing a full backup as a baseline, then only sending the changes across in each subsequent backup.

Eventually the FTP account was no longer available, so I started looking in to a better solution. I'd done a lot of work recently with <a href="https://aws.amazon.com/">Amazon Web Services</a>, so I decided to investigate that as a backup solution. Amazon's <a href="https://aws.amazon.com/s3/">S3 offering</a> allows infinitely scalable, cheap object storage in the cloud. I went ahead and created a bucket which would store the backup files.

The <a href="https://aws.amazon.com/cli/">official AWS Command Line Interface (CLI)</a> provides an easy way to perform operations on S3 (along with most of the the other AWS services). In fact, they have a command which can sync a local folder with an S3 bucket, sending only the modified files with each sync. Armed with this new tool, I wrote a basic Perl script which would call the following system command:

    system("/usr/bin/aws s3 sync --delete /var/www/html/ s3://maad-backup/html");

I set the script to run automatically at 10pm each night, and went to bed happy with the knowledge that I'd set up a simple backup solution which would cost mere cents per month.

When I awoke the next morning, I checked my emails and saw that I had a Billing Alarm email from Amazon - my monthly spend had already gone past the alarm threshold I had set! What had gone wrong? Had my account been compromised somehow? I had a sick feeling just thinking about what the current monthly spend would be by now. If indeed I had been compromised, the intruders would have spun up as many powerful EC2 machines as they could, most likely to mine for Bitcoin.

After logging on to my AWS account, I could breathe a sigh of relief - I hadn't been compromised, only stupid. My monthly spend was at about $50, up from my usual of $25-$30. Drilling in to the AWS Bill, I could see that my S3 costs for the month were *well* above my normal spend. The bill was reporting that I had made several million PUT operations to S3 - that is, I had loaded millions of files. Surely this couldn't be right... There would definitely be a lot of files on the web server, but nowhere in the order of millions.

Clicking around the S3 console I could immediately see the problem. One of the subfolders that I had synced to S3 contained a symbolic link - to itself.

    [matthewh@folio mydir]$ pwd
    /home/matthewh/mydir

    [matthewh@folio mydir]$ ln -s ./ mydir

    [matthewh@folio mydir]$ ll
    total 0
    lrwxrwxrwx 1 matthewh matthewh 2 Feb  1 12:43 mydir -> ./
    [matthewh@folio mydir]$ cd mydir/
    [matthewh@folio mydir]$ cd mydir/
    [matthewh@folio mydir]$ cd mydir/
    [matthewh@folio mydir]$ cd mydir/
    [matthewh@folio mydir]$ pwd
    /home/matthewh/mydir/mydir/mydir/mydir/mydir

Turns out that by default, the `aws sync` command will follow these symbolic links and create separate, distinct objects in the S3 bucket, even when the link points to its own directory. My script had been running for hours, creating infinite levels of directories containing themselves.

<img style="float:right; padding-left: 10px" height="300" src="/static/img/blog/turtles.jpg" />

I checked the process list and confirmed that the script was no longer running, so I assume I must have hit some sort of memory limit on the server, or perhaps a hard limit on directory depth on S3.

After consulting the <a href="http://docs.aws.amazon.com/cli/latest/reference/s3/sync.html">documentation</a> (this would have been the ideal first step!) I realised the mistake - I had to include a parameter `--no-follow-symlinks`.

    system("/usr/bin/aws s3 sync --no-follow-symlinks --delete /var/www/html/ s3://maad-backup/html");

Running the script again fixed up the existing mess (by virtue of the `--delete` parameter) and gave me the desired result - a simple, secure backup of the web server.

This could have been a lot worse - if I didn't have a billing alarm set up, and if the script had not killed itself - I could have run up a very massive AWS bill because of this mistake.
