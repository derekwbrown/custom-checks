
import requests
from datadog_checks.base import AgentCheck, ConfigurationError

AMBIENT_ENDPOINT='https://api.ambientweather.net/v1'
AMBIENT_METRIC_NAMES='weather'

class AmbientCheck(AgentCheck):
    def check(self, instance):
        ## allow URL overload
        url = instance.get('url')
        if not url:
            url = AMBIENT_ENDPOINT

        custom_tags = instance.get('tags', [])
        metric_prefix = instance.get('metric_prefix', AMBIENT_METRIC_NAMES)

        apikey = instance.get('apikey')
        appkey = instance.get('appkey')

        if not apikey or not appkey:
            raise ConfigurationError('Missing app key or api key')

        params = {
           'applicationKey': appkey,
           'apiKey': apikey
        }

        request_url = "{}/devices".format(url)
        res = requests.get(request_url, params)
        out = res.json()
        for device in out:
            addr = device.get("macAddress")
            name = device.get("info").get("name")
            loc = device.get("info").get("location")
            data = device.get("lastData")
            tags = ['name:{}'.format(name), 'location:{}'.format(loc), 'macaddr:{}'.format(addr)]
            tags.extend(custom_tags)
            for key in data:
                ## only submit data that is numerical, i.e. can be converted to floatval
                try:
                    floatval = float(data[key])
                except ValueError as e:
                    continue
                mname = "{}.{}".format(metric_prefix, key)
                self.gauge(mname, floatval, tags)