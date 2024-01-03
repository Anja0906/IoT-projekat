import datetime
import time

from dateutil import parser

from server.server import get_server_values

influxdb_client, org = get_server_values()


def handle_flux_query(influxdb_client, query, org):
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
    query = f"""from(bucket: "example_db")
        |> range(start: -5s)
        |> filter(fn: (r) => r.name == "{name}")"""
    query_data = handle_flux_query(influxdb_client, query, org)
    return check_values_true_last_seconds(query_data, 5)


def query_dus_sensor(i_client, organization, name):
    query = f"""from(bucket: "example_db")
        |> range(start: -10m)
        |> filter(fn: (r) => r.name == "{name}")
        |> tail(n: 10)"""
    query_data = handle_flux_query(i_client, query, organization)
    return check_dus_for_entering_or_leaving(query_data)


def check_dus_for_entering_or_leaving(query_data):
    values = []
    for d in query_data:
        values.append(d["_value"])
    if analyze_movement(values):
        return True
    else:
        return False


def analyze_movement(measurements):
    entering = 0
    leaving = 0

    for i in range(len(measurements) - 1):
        if measurements[i + 1] < measurements[i]:
            entering += 1
        elif measurements[i + 1] > measurements[i]:
            leaving += 1

    return entering > leaving


def query_gyro_sensor():
    query = f"""from(bucket: "example_db")
            |> range(start: -10m)
            |> filter(fn: (r) => r.name == "GSG")
            |> tail(n: 6)"""
    query_data = handle_flux_query(influxdb_client, query, org)
    if significant_movement(query_data):
        print("Značajan pokret detektovan")
    else:
        print("Nema značajnog pokreta")


def extract_values(value_str):
    clean_str = value_str.replace('a/g:', '').replace('g', '').replace('d/s', '')
    parts = clean_str.split('\t')
    a_values = [float(parts[i]) for i in range(3)]
    g_values = [float(parts[i]) for i in range(3, 6)]
    return a_values, g_values


def significant_movement(data, accel_threshold=3.0, gyro_threshold=400.0):
    prev_accel, prev_gyro = extract_values(data[0]["_value"])

    for entry in data[1:]:
        current_accel, current_gyro = extract_values(entry["_value"])
        accel_diff = [abs(current - prev) for current, prev in zip(current_accel, prev_accel)]
        gyro_diff = [abs(current - prev) for current, prev in zip(current_gyro, prev_gyro)]
        if any(diff > accel_threshold for diff in accel_diff) or any(diff > gyro_threshold for diff in gyro_diff):
            return True
        prev_accel, prev_gyro = current_accel, current_gyro
    return False


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
        query_dus_sensor("DUS1")
        query_gyro_sensor()
        # if result1:
        #     print(f"Alarm at {datetime.datetime.now()} for DS1: {result1}")
        # if result2:
        #     print(f"Alarm at {datetime.datetime.now()} for DS2: {result2}")
        time.sleep(5)  # Wait for 5 seconds before the next query


if __name__ == '__main__':
    continuously_query_sensor()
