# simple-monitor

Usage: python monitor.py

monitor.py read every .conf file in the same directory where monitor.py locate.

Each .conf file is a json config about the service you want to monitor. There are sample config files available.

Configuration:

All configuration files are put in checks folder, each file contain json that include information about a service needs to be checked and can be loaded to a dictionary using json library in Python.

This dictionary contains several keys, the value of each key has a default value defined in monitor.py:

* description: Description of the service that needs to be checked.
* url: The URL of this service.
* method: The method with which this tool sending requests.
* timeout: The number of seconds after which sending requests timeout.
* text: The content returned from sending request to this service needs a match with this text.
* body: POST data, if method is POST.
* code: HTTP status code returned should match this code.
* slack_notify: The URL that this tool tries to notify to if any thing wrong about the check, alerting people to focus.

Sample config:

{
  "description": "The Wiredcraft website",
  "url": "http://wiredcraft.com",
  "method": "GET",
  "timeout": 4,
  "text": "wiredcraft",
  "code": 200,
  "slack_notify": "https://wiredcraft.slack.com/services/hooks/slackbot?token=4qNSl8UdnaipTg2f36ZnoEU1&channel=song_for_testing"
}

How to install it:

* Install required packages using command:
pip install -r requirements.txt

* Deploy code to right place.

* Edit crontab, adding a line like crontab file in this repo.
