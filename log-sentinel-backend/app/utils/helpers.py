def parse_log_line(log_line: str) -> dict:
    """
    Parses a single line of log and returns a dictionary with relevant fields.
    Assumes log lines are in a specific format.
    """
    # Example log line format: "timestamp level message"
    parts = log_line.split(' ', 2)
    if len(parts) < 3:
        return {}
    
    return {
        'timestamp': parts[0],
        'level': parts[1],
        'message': parts[2]
    }

def format_log_entry(log_entry: dict) -> str:
    """
    Formats a log entry dictionary into a string for display or storage.
    """
    return f"{log_entry['timestamp']} [{log_entry['level']}] {log_entry['message']}"

def validate_log_entry(log_entry: dict) -> bool:
    """
    Validates the log entry to ensure it contains the required fields.
    """
    required_fields = ['timestamp', 'level', 'message']
    return all(field in log_entry for field in required_fields)