# CP-Calendar

It's just a simple script to add all contest from site to your `Google Calendar` and make two reminder for them one before the contest one day, and another before half an hour, the event on `Google Calendar` have the registration link of the contest.

## Requirements

```bash
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

```bash
    pip install DateTime
```

```bash
    pip install python-dotenv
```

## Choose sites you want to get they contests

from `.env` file you can write True of False on the right of each site

## Replace `credentials.json` with your `credentials` information

See first `11` minutes in this [video](https://www.youtube.com/watch?v=eRHvfNKcwMQ&t=1629s&ab_channel=Cndro) to know how to get your credentials information

The site in the video: [Cloud Google](https://console.cloud.google.com/)
