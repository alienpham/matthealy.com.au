title: Google Contacts API Error
timestamp: 2015-05-24 13:13:59
slug: google-contacts-api-error
tags: [google, google-contacts, api]
author: Matt Healy

I recently had to upgrade an existing <a href="https://developers.google.com/google-apps/contacts/v3/">Google Contacts</a> integration from version 2 to version 3, as the version 2 API was being discontinued by Google. The differences between the two versions were substantial, as the entire authentication procedure (AuthSub) had to be replaced with the more modern OAuth. Luckily, the actual data format of the contact entries didn't change, and remained as <a href="https://developers.google.com/gdata/docs/2.0/elements?csw=1#gdContactKind">GData Contact kind</a>. 

I made all the required changes, pushed them in to production, and let the users sync away. A few weeks later a user reported that not all of their records were syncing over to Google. I looked in to the problem and found that some of the batches of data synced failed, and had this error message returned:

```Inconsistent repeating query parameter```

Searching for that error string on Google brought me to <a href="https://groups.google.com/forum/#!topic/google-contacts-api/zdfV-AA3TFg"> this old thread</a> from 2011, where the answer was to use the appropriate Content-Type for the HTTP POST request when submitting the batch. I glanced at my code, saw the string `application/atom+xml` and therefore dismissed the thread as not the answer I was looking for.

<img style="float:left; padding-right: 10px" height="200" src="/static/img/blog/obi-wan.jpg" />

I spent the next hour or so trying countless iterations of attempted solutions without any success. After leaving the problem and returning later, I saw the obvious answer: the old thread was right. I needed to use the correct Content-Type. It had turned out that although I was creating a Header resource with the correct Content-Type, I wasn't applying the Header to the actual POST request. I deployed the fix, ran another sync, and of course it worked perfectly.

The lesson I took away from this was to not automatically assume that you are correct all the time, even on the most obvious things that you wouldn't usually think twice about. If you've exhausted all other options, you have to go back to basics and make sure the things you've assumed to be correct actually are.
