from collections import Counter, defaultdict
import re


# Dummy log details
RAW_LOGS = [
    "2024-06-01 08:01:12,045 INFO     auth: User admin logged in successfully",
    "2024-06-01 08:01:45,112 INFO     database: Connection pool initialized with 10 connections",
    "2024-06-01 08:02:03,201 WARNING  auth: Failed login attempt for user guest",
    "2024-06-01 08:02:18,334 ERROR    database: Connection timeout after 30 seconds",
    "2024-06-01 08:02:19,401 ERROR    database: Connection timeout after 30 seconds",
    "2024-06-01 08:02:55,510 INFO     api: GET /api/products returned 200 OK",
    "2024-06-01 08:03:10,612 INFO     api: GET /api/users returned 200 OK",
    "2024-06-01 08:03:33,701 WARNING  cache: Cache miss for key user_session_4821",
    "2024-06-01 08:03:44,812 ERROR    api: POST /api/orders failed with 500 Internal Server Error",
    "2024-06-01 08:04:01,905 CRITICAL database: Max connection limit reached, refusing new connections",
    "2024-06-01 08:04:15,023 ERROR    database: Connection timeout after 30 seconds",
    "2024-06-01 08:04:29,134 WARNING  auth: Session token expired for user id 2291",
    "2024-06-01 08:04:50,245 INFO     scheduler: Background job cleanup_temp_files started",
    "2024-06-01 08:05:02,356 ERROR    scheduler: Job send_email_digest failed with SMTP timeout",
    "2024-06-01 08:05:18,467 INFO     api: GET /api/reports returned 200 OK",
    "2024-06-01 08:05:31,578 ERROR    auth: Account locked after 5 failed login attempts",
    "2024-06-01 08:05:47,689 WARNING  database: Query execution time exceeded 2 seconds",
    "2024-06-01 08:06:03,790 INFO     cache: Cache warmed up with 1500 entries",
    "2024-06-01 08:06:19,901 ERROR    api: POST /api/orders failed with 500 Internal Server Error",
    "2024-06-01 08:06:35,012 CRITICAL auth: Multiple CRITICAL security violations detected from IP 192.168.1.55",
    "2024-06-01 08:06:51,123 INFO     api: DELETE /api/sessions returned 204 No Content",
    "2024-06-01 08:07:07,234 WARNING  scheduler: Job daily_report is running 15 minutes behind schedule",
    "2024-06-01 08:07:23,345 ERROR    database: Deadlock detected between transactions T1 and T2",
    "2024-06-01 08:07:39,456 INFO     auth: Password changed for user id 1042",
    "2024-06-01 08:07:55,567 ERROR    cache: Redis connection refused on port 6379",
    "2024-06-01 08:08:11,678 INFO     api: GET /api/dashboard returned 200 OK",
    "2024-06-01 08:08:27,789 WARNING  auth: Failed login attempt for user guest",
    "2024-06-01 08:08:43,890 ERROR    scheduler: Job send_email_digest failed with SMTP timeout",
    "2024-06-01 08:09:00,001 CRITICAL database: Disk usage at 98 percent, writes may fail soon",
    "2024-06-01 08:09:16,112 INFO     database: Automatic vacuum completed on table orders",
    "2024-06-01 08:09:32,223 ERROR    api: GET /api/analytics timed out after 60 seconds",
    "2024-06-01 08:09:48,334 WARNING  cache: Cache eviction rate above threshold at 82 percent",
    "2024-06-01 08:10:04,445 INFO     scheduler: Background job sync_inventory completed in 4.2 seconds",
    "2024-06-01 08:10:20,556 ERROR    database: Connection timeout after 30 seconds",
    "2024-06-01 08:10:36,667 INFO     auth: New user registered with id 5503",
    "2024-06-01 08:10:52,778 CRITICAL api: API rate limiter triggered, dropping requests from IP 10.0.0.88",
    "2024-06-01 08:11:08,889 WARNING  database: Replication lag is 45 seconds behind primary",
    "2024-06-01 08:11:24,990 ERROR    auth: JWT signature verification failed for token",
    "2024-06-01 08:11:41,101 INFO     cache: Cache hit ratio is 94 percent over last 5 minutes",
    "2024-06-01 08:11:57,212 ERROR    api: POST /api/payments rejected by gateway with code 402",
]


LOG_PATTERN = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+)"
    r"\s+(?P<level>\w+)"
    r"\s+(?P<module>\w+):"
    r"\s+(?P<message>.+)"
)

def parse_log_line(line):
    """
    Parse one raw log string into a dict with four fields.
    Returns None if the line does not match the expected format.
    """

    # Remove any leading or trailing whitespace from the line
    cleaned_line = line.strip()

    # Try to match the cleaned line against the regex pattern
    match = LOG_PATTERN.match(cleaned_line)

    # If no match was found, the line is malformed, so we skip it
    if match is None:
        return None

    # Pull each named group out of the match and store it in a plain dict
    timestamp = match.group("timestamp")
    level     = match.group("level")
    module    = match.group("module")
    message   = match.group("message")

    log_entry = {
        "timestamp": timestamp,
        "level":     level,
        "module":    module,
        "message":   message,
    }

    return log_entry


def parse_all_logs(raw_lines):
    """
    Go through every raw log string and parse it.
    Returns a list of dicts. Lines that fail to parse are skipped.
    """

    parsed_entries = []

    for line in raw_lines:

        # Parse this single line into a dict
        entry = parse_log_line(line)

        # Only add to our list if parsing was successful
        if entry is not None:
            parsed_entries.append(entry)

    return parsed_entries

def count_log_levels(parsed_logs):
    """
    Count how many entries exist for each log level (INFO, WARNING, ERROR, CRITICAL).
    Returns a Counter like: Counter({'INFO': 14, 'ERROR': 14, ...})
    """

    # Start with an empty Counter
    level_counter = Counter()

    # Walk through every parsed entry and tally its level
    for entry in parsed_logs:
        level = entry.get("level")
        level_counter[level] = level_counter[level] + 1

    return level_counter


def count_active_modules(parsed_logs):
    """
    Count how many log lines each module produced.
    The module with the highest count is the busiest one.
    """

    module_counter = Counter()

    for entry in parsed_logs:
        module = entry.get("module")
        module_counter[module] = module_counter[module] + 1

    return module_counter


def count_error_messages(parsed_logs, top_n=5):
    """
    Collect every message from ERROR and CRITICAL entries, count duplicates,
    and return the top_n most common ones as a list of (message, count) pairs.
    """

    # First collect only the messages from error-level entries
    error_messages = []

    for entry in parsed_logs:
        level = entry.get("level")

        # We only care about serious issues, not INFO or WARNING
        if level == "ERROR" or level == "CRITICAL":
            message = entry.get("message")
            error_messages.append(message)

    # Counter will tally duplicate messages automatically
    message_counter = Counter(error_messages)

    # most_common(n) returns a sorted list of (item, count) tuples
    top_messages = message_counter.most_common(top_n)

    return top_messages



def group_errors_by_module(parsed_logs):
    """
    Build a dict where each key is a module name and each value is
    the list of error messages that module produced.
    """

    # defaultdict(list) means errors_by_module[any_new_key] starts as []
    errors_by_module = defaultdict(list)

    for entry in parsed_logs:
        level = entry.get("level")

        # Only group the serious log levels
        if level == "ERROR" or level == "CRITICAL":
            module  = entry.get("module", "unknown")
            message = entry.get("message")

            # Append directly, no need to check if the key exists
            errors_by_module[module].append(message)

    return errors_by_module


def generate_summary(parsed_logs):
    """
    Combine all analysis results into one summary dict with four fields:
      total_entries  - how many log lines were parsed
      error_rate     - percentage of lines that were ERROR or CRITICAL
      top_errors     - the three most repeated error messages
      busiest_module - the module that produced the most log lines
    """

    total_entries = len(parsed_logs)

    # Guard: if there are no entries, return safe default values
    if total_entries == 0:
        empty_summary = {
            "total_entries":  0,
            "error_rate":     "0.00%",
            "top_errors":     [],
            "busiest_module": None,
        }
        return empty_summary

    # Count levels and modules using our functions from Step 2
    level_counts  = count_log_levels(parsed_logs)
    module_counts = count_active_modules(parsed_logs)

    # Get the three most repeated error messages
    top_3_errors = count_error_messages(parsed_logs, top_n=3)

    # Calculate how many entries were errors or critical
    error_count    = level_counts.get("ERROR", 0)
    critical_count = level_counts.get("CRITICAL", 0)
    total_bad      = error_count + critical_count

    # Express that as a percentage of all entries, rounded to 2 decimal places
    error_rate_number = round((total_bad / total_entries) * 100, 2)
    error_rate_string = str(error_rate_number) + "%"

    # most_common(1) returns a list with one tuple: [(module_name, count)]
    # We grab index [0][0] to get just the module name string
    top_module_list  = module_counts.most_common(1)
    top_module_tuple = top_module_list[0]
    busiest_module   = top_module_tuple[0]

    # Build the list of just the message strings, dropping the counts
    top_error_messages = []
    for message, count in top_3_errors:
        top_error_messages.append(message)

    summary = {
        "total_entries":  total_entries,
        "error_rate":     error_rate_string,
        "top_errors":     top_error_messages,
        "busiest_module": busiest_module,
    }

    return summary


def print_separator(title=""):
    """Print a full-width separator line, with an optional title above it."""
    divider = "=" * 60
    if title:
        print(divider)
        print("  " + title)
        print(divider)
    else:
        print(divider)


def print_counter_results(counter, label, top_n=5):
    """
    Display the top N items from a Counter with a simple bar chart made of hashes.
    Each hash symbol represents one occurrence.
    """

    print()
    print("  " + label)
    print()

    top_items = counter.most_common(top_n)

    for item, count in top_items:
        # Build a visual bar: one hash per occurrence
        bar = "#" * count

        # Print item name left-aligned, count right-aligned, then the bar
        print("    {:<35} {:>3}   {}".format(item, count, bar))


def print_errors_by_module(errors_by_module):
    """
    For each module, print how many errors it had and list each unique error message.
    Duplicate messages within a module are printed only once.
    """

    print()

    # sorted() makes the output alphabetical and easier to scan
    for module, messages in sorted(errors_by_module.items()):

        error_count = len(messages)
        print("  Module: {}  ({} error entries)".format(module, error_count))

        # Use a set to track which messages we have already printed
        already_printed = set()

        for message in messages:
            if message not in already_printed:
                print("      -", message)
                already_printed.add(message)

        print()


def print_summary(summary):
    """Display each field of the summary dict on its own clearly labelled line."""

    print()
    print("  Total entries  :", summary.get("total_entries"))
    print("  Error rate     :", summary.get("error_rate"))
    print("  Busiest module :", summary.get("busiest_module"))
    print()
    print("  Top repeated errors:")

    top_errors = summary.get("top_errors", [])

    for index, message in enumerate(top_errors):
        # enumerate starts at 0 by default, so we add 1 for a natural count
        number = index + 1
        print("    {}. {}".format(number, message))



if __name__ == "__main__":

    parsed_logs = parse_all_logs(RAW_LOGS)

    print_separator("PARSED LOG ENTRIES  (first 5 shown)")

    first_five = parsed_logs[:5]

    for entry in first_five:
        timestamp = entry.get("timestamp")
        level     = entry.get("level")
        module    = entry.get("module")
        message   = entry.get("message")

        print("  {}   [{:<8}]   {}   {}".format(timestamp, level, module, message))

    remaining_count = len(parsed_logs) - 5
    print()
    print("  ... and {} more entries".format(remaining_count))

    print_separator("LOG LEVEL DISTRIBUTION  (Counter)")
    level_counts = count_log_levels(parsed_logs)
    print_counter_results(level_counts, "How many entries per level", top_n=10)

    print_separator(" MOST ACTIVE MODULES  (Counter)")
    module_counts = count_active_modules(parsed_logs)
    print_counter_results(module_counts, "Total log lines per module", top_n=10)

    print_separator(" MOST REPEATED ERROR MESSAGES  (Counter)")
    top_errors = count_error_messages(parsed_logs, top_n=5)

    # Build a Counter from the results so we can reuse print_counter_results
    error_counter = Counter()
    for message, count in top_errors:
        error_counter[message] = count

    print_counter_results(error_counter, "Repeated error and critical messages", top_n=5)


    print_separator("ERRORS GROUPED BY MODULE  (defaultdict)")
    errors_by_module = group_errors_by_module(parsed_logs)
    print_errors_by_module(errors_by_module)

    print_separator("FINAL SUMMARY DICT")
    summary = generate_summary(parsed_logs)
    print_summary(summary)
    print_separator()