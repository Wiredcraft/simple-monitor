import json
import os
import requests
import urllib3
from os import listdir


default_config = {
    "description": "Description",
    "url": "",
    "method": "POST",
    "body": "",  # exists only if method is POST
    "timeout": 5,
    "code": 200,
    "text": "",
    "slack_notify": "https://wiredcraft.slack.com/services/hooks/slackbot?token=4qNSl8UdnaipTg2f36ZnoEU1&channel=song_for_testing",
}


def notify(msg, url):
    print msg
    result = requests.post(url, data=msg.encode("utf-8"))
    if result.status_code != 200:
        print "Notification fail!"


def get_config(config_file):
    try:
        config = json.loads(open(config_file).read())
    except (ValueError, TypeError, IOError):
        print "config can not be parsed correctly."
        return

    return config


def handle_config(config):
    if not config.get("timeout"):
        config['timeout'] = default_config.get("timeout")

    if not config.get("code"):
        config['code'] = default_config.get("code")

    if not config.get("slack_notify"):
        config['slack_notify'] = default_config.get("slack_notify")

    return config


def health_check(config):

    try:
        if config['method'] == "GET":
            result = requests.get(
                config['url'],
                timeout=float(config['timeout']),
            )
        elif config['method'] == "POST":
            result = requests.post(
                config['url'],
                timeout=float(config['timeout']),
            )
        elif config['method'] == "PUT":
            result = requests.put(
                config['url'],
                timeout=float(config['timeout']),
            )
        elif config['method'] == "DEL":
            result = requests.delete(
                config['url'],
                timeout=float(config['timeout']),
            )
        else:
            notify(
                "Service %s method is %s, only POST/GET/DEL/PUT are supported", (
                    config['url'],
                    config['method']
                ),
                config['slack_notify']
            )
            return
    except requests.exceptions.Timeout:
        notify(u"Service %s timeout" % config['url'], config['slack_notify'])
        return
    except requests.exceptions.ConnectionError:
        notify(u"Service %s can not be connected" % config['url'], config['slack_notify'])
        return

    if result.status_code != config['code'] or result.text != config['text']:
        msg = u"Service %s return code is %s, expect: %s,\n" \
        u"return text is %s, expect: %s" % (
            config['url'], result.status_code, config['code'],
            result.text, config['text']
        )
        notify(msg, config['slack_notify'])
    return


def main():
    for filename in listdir('.'):
        _, file_extension = os.path.splitext(filename)
        if file_extension == '.conf':
            read_config = get_config(filename)
            if not read_config:
                raise IOError
            config = handle_config(read_config)
            health_check(config)


if __name__ == '__main__':
    main()
