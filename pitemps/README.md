# pitemps.py

Periodically queries the OS on a Raspberry Pi for the CPU and GPU temperatures.
Uses `/sys/class/thermal/thermal_zone0/temp` for the CPU temperature, and 
shells to `/usr/bin/vcgencmd` for the GPU temperature, and the boolean indicating
if the CPU is throttled for temperature reasons.

If the CPU is throttled, sets the `system.cpu_is_throttled` service check.


## notes
Need to add dd-agent to /etc/sudoers.  Sample /etc/sudoers.d/91-dd-agent-vcgencmd
dd-agent ALL=NOPASSWD: /usr/bin/vcgencmd