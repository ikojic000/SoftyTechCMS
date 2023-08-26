import csv
from io import StringIO

from flaskblog.models import ErrorLog, RequestLog


# Prepare data for logs
def prepare_logs_data(log_model):
    """
    Prepare log data for exporting to JSON or CSV.

    Args:
        log_model (class): The log model (RequestLog or ErrorLog) to retrieve data from.

    Returns:
        list of dict: A list of dictionaries containing log data.
    """
    logs_data = log_model.query.all()
    data = []

    for log in logs_data:
        log_data = {
            "id": log.id,
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "user": log.user.username if log.user else None,
        }

        if isinstance(log, RequestLog):
            log_data.update(
                {
                    "endpoint": log.endpoint,
                    "method": log.methodType,
                }
            )
        elif isinstance(log, ErrorLog):
            log_data.update(
                {
                    "endpoint": log.endpoint,
                    "method": log.methodType,
                    "status_code": log.status_code,
                    "error_message": log.error_message,
                }
            )

        data.append(log_data)

    return data


# Generate CSV from data
def generate_csv(data):
    """
    Generate CSV data from a list of lists.

    Args:
        data (list of list): The data to be converted to CSV format.

    Returns:
        str: The CSV data as a string.
    """
    output = StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerows(data)
    return output.getvalue()
