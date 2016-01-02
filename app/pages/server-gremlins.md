title: Server Gremlins
timestamp: 2015-06-14 12:58:15
slug: server-gremlins
tags: [perl, aws, s3, debugging]
author: Matt Healy

I recently came across an interesting problem with one of the companies I'm involved with. Their main product is an iPad app with a backend server for syncing data back to the cloud. Their production environment resides in the AWS data centre in Sydney, but they have a secondary server in Perth which is still used by some clients on the older version of the app. 

Seemingly without cause, the Perth server started experiencing problems loading image files up to S3. I investigated with the other technicians. We ruled out the obvious first:

1. The code on the server hadn't been touched in over a week, so it couldn't be a code issue
2. The same code was working on the production site in Sydney, indicating that the issue could be to do with the server itself.
3. The same issue occurred when trying to load a file to a different S3 bucket, so the bucket wasn't the problem.

Ok, so all signs point to the server being the problem. But where to start? And how could a problem just materialise out of nowhere, with no changes being made in the last week? I already inspected our code and couldn't find anything, so it was time to look in to the third-party libraries we used. The backend is written in Perl and utilises the <a href="http://search.cpan.org/~tima/Amazon-S3-0.45/lib/Amazon/S3.pm">Amazon::S3</a> module. 

I looked in to the Bucket.pm file and drilled down to basics. The `add_key_filename` method made a call to `add_key`. The `add_key` method contains a comment stating:

> If we're pushing to a bucket that's under DNS flux, we might get a 307

This made me think that the problem might be related to DNS, so I deviated a bit and sanity checked the DNS responses being obtained by the server. I even tried changing the server's resolver just to make sure, but still had no success, so back to checking the Perl modules. 

Looking back in to the `Amazon::S3` module, specifically the `S3.pm` file, I investigated the actual `LWP` object that gets instantiated. Passing the `LWP` object into `Data::Dumper` revealed the cause of our woes:


          'Code' => 'RequestTimeTooSkewed',

          'RequestId' => '183892BBCA7FF3D2',

          'ServerTime' => '2015-06-08T06:25:25Z',

          'Message' => 'The difference between the request time and the current time is too large.',

          'HostId' => 'oOvyHbSk2B7hFlk0UgVREBzq7f5seJhCdbxf8B+cOkrYaZ76qgqt9Z0H+5CU80Xk',

          'MaxAllowedSkewMilliseconds' => '900000',

          'RequestTime' => 'Mon, 08 Jun 2015 06:41:00 GMT'


Unbelievable... after all this investigation, the answer was hiding in plain sight.

The system clock was fast by just over 15 minutes. According to the response, `MaxAllowedSkewMilliseconds` is 900,000 which turns out to be exactly 15 minutes. After syncing the system clock back to the correct time, the issue disappeared.
