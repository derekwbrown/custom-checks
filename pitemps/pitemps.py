from datadog_checks.base import AgentCheck, ConfigurationError
from datadog_checks.utils.subprocess_output import get_subprocess_output

class PiTempCheck(AgentCheck):
    def check(self, instance):
        tags = instance.get('tags', [])
        tmp_args = ['cat', '/sys/class/thermal/thermal_zone0/temp']
        get_throttled_args = ['sudo', '/usr/bin/vcgencmd', 'get_throttled']
        get_gpu_temp_args = ['sudo', '/usr/bin/vcgencmd', 'measure_temp']

        ## get the cpu temperature
        out, err, retcode = get_subprocess_output(tmp_args, self.log, raise_on_empty_output=True)
        cpu_tmp = float(out) / 1000

        ## get the Gpu temperature
        out, err, retcode = get_subprocess_output(get_gpu_temp_args, self.log, raise_on_empty_output=True)
        ### format of Gpu tmp is "temp=num'C"
        tmpwithC = out.split('=')[1]
        gpu_tmp = float(tmpwithC.split('\'')[0])

        ## get the throttled state
        out, err, retcode = get_subprocess_output(get_throttled_args, self.log, raise_on_empty_output=True)
        is_throttled = int(out.split('=')[1], 0)
        
        self.gauge("system.temp.cpu", cpu_tmp, tags)
        self.gauge("system.temp.gpu", gpu_tmp, tags)
        #self.gauge("system.cpu.is_throttled", is_throttled, tags)

        svccheck = 0 # OK
        if is_throttled:
            svccheck = 1

        self.service_check("system.cpu_is_throttled", svccheck, tags)