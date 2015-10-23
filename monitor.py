import json
import os
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
}


def notify(msg):
    print msg
    # TODO: send message to slack.


def get_config(config_file):
    try:
        config = json.loads(open(config_file).read())
    except (ValueError, TypeError, IOError):
        msg = "config can not be parsed correctly."
        notify(msg)
        return

    return config


def handle_config(config):
    if not config.get("timeout"):
        config['timeout'] = default_config.get("timeout")

    if not config.get("code"):
        config['code'] = default_config.get("code")

    return config


def health_check(config):
    http = urllib3.PoolManager()

    if config['method'] == "GET":
        try:
            result = http.request(
                "GET", config['url'],
                timeout=urllib3.Timeout(total=float(config['timeout'])),
            )
        except urllib3.exceptions.ConnectTimeoutError:
            notify("Service %s timeout" % config['url'])
            return

    elif config['method'] == "POST":
        try:
            result = http.request(
                "POST", config['url'],
                timeout=urllib3.Timeout(total=float(config['timeout'])),
                body=config['body'],
            )
        except urllib3.exceptions.ConnectTimeoutError:
            notify("Service %s timeout" % config['url'])
            return

    elif config['method'] == "PUT":
        try:
            result = http.request(
                "PUT", config['url'],
                timeout=urllib3.Timeout(total=float(config['timeout'])),
                body=config['body'],
            )
        except urllib3.exceptions.ConnectTimeoutError:
            notify("Service %s timeout" % config['url'])
            return

    elif config['method'] == "DEL":
        try:
            result = http.request(
                "DEL", config['url'],
                timeout=urllib3.Timeout(total=float(config['timeout'])),
                body=config['body'],

            )
        except urllib3.exceptions.ConnectTimeoutError:
            notify("Service %s timeout" % config['url'])
            return

    else:
        notify(
            "Service %s method is %s, only POST/GET/DEL/PUT are supported", (
                config['url'],
                config['method']
            )
        )

    if result.status != config['code']:
        msg = "Service %s return code is %s, expect: %s" % (
            config['url'], result.status, config['code']
        )
        notify(msg)

    if result.data != config['text']:
        msg = "Service %s return text is %s, expect: %s" % (
            config['url'], result.data, config['text']
        )
        notify(msg)

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
