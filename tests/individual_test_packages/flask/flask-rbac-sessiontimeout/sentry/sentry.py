import sentry_sdk
from sentry.pii_phi import PiiRegex
from dotenv import load_dotenv
import os 

load_dotenv()

def before_send(event, hint):
    # Instantiate the PiiRegex object
    pii_checker = PiiRegex()

    # Define a helper function to recursively sanitize data
    def sanitize_data(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    # Check for PII/PHI matches in the string value
                    if pii_checker.any_match(value):
                        data[key] = "[REDACTED]"
                else:
                    # Recurse into nested dictionaries or lists
                    data[key] = sanitize_data(value)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                data[i] = sanitize_data(item)
        return data

    # Apply sanitization to event data that could contain sensitive information
    for section in ['exception', 'logentry', 'message', 'extra']:
        if section in event:
            event[section] = sanitize_data(event[section])

    return event


def init_sentry():
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        before_send=before_send,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

    return sentry_sdk