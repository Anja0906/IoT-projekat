import datetime
import time

from dateutil import parser

from server import bucket, org, influxdb_client


def handle_flux_query(influxdb_client, query, org, bucket):
    try:
        query_api = influxdb_client.query_api()
        tables = query_api.query(query, org=org)

        container = []
        for table in tables:
            for record in table.records:
                container.append(record.values)

        return container
    except Exception as e:
        return []


def query_ds_sensor(name):
    query = f"""from(bucket: "{bucket}")
        |> range(start: -5s)
        |> filter(fn: (r) => r.name == "{name}")"""
    query_data = handle_flux_query(influxdb_client, query, org, bucket)
    return check_values_true_last_seconds(query_data, 5)


def check_values_true_last_seconds(data, seconds):
    if not data:
        return False
    last_data_point = data[-1]
    last_timestamp = last_data_point['_time']
    if isinstance(last_timestamp, str):
        last_timestamp = parser.parse(last_timestamp)

    threshold_timestamp = last_timestamp - datetime.timedelta(seconds=seconds)

    return all(
        (parser.parse(item['_time']) if isinstance(item['_time'], str) else item['_time']) >= threshold_timestamp and
        item['_value']
        for item in data if '_time' in item and '_value' in item
    )
def continuously_query_sensor():
    while True:
        result1 = query_ds_sensor("DS1")
        result2 = query_ds_sensor("DS2")
        if result1:
            print(f"Alarm at {datetime.datetime.now()} for DS1: {result1}")
        if result2:
            print(f"Alarm at {datetime.datetime.now()} for DS2: {result2}")
        time.sleep(5)  # Wait for 5 seconds before the next query

if __name__ == '__main__':
    continuously_query_sensor()