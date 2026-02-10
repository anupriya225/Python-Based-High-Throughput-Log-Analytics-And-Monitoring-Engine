import re

def parse_log_line(line):
    log_pattern = r'^(?P<timestamp>\S+)\s+(?P<level>\S+)\s+(?P<service>\S+)\s+(?P<message>.*)$'
    
    match = re.match(log_pattern, line)
    if match:
        return match.groupdict()
    else:
        return None