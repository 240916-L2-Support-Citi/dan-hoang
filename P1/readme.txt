log_monitor_skip.txt records the line number that was last read from the log
file.

alert_system_last_time.txt records the number of nonfatal errors encountered
to date (modulo nonfatal error tolerance) on the first line, the number of fa-
tal errors encountered to date (modulo fatal error tolerance) on the second
line, and the timestamp of the last log entry processed.

The initial state of these files should be 0 for log_monitor_skip.txt and 0, 0,
and a blank line for alert_system_last_time.txt.
