

import sqlite3
import csv

con = sqlite3.connect("db")
con.row_factory = sqlite3.Row
cur = con.cursor()

rows = cur.execute("select * from traffic")
with open('db.csv', 'w') as csvfile:
    traffic_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    traffic_writer.writerow([
        'ts_utc',
        'ts_mt',
        'origin',
        'dest',
        'distance_text',
        'distance_meters',
        'duration_in_traffic_text',
        'duration_in_traffic_seconds',
        'duration_text',
        'duration_seconds'
    ])
    for row in rows:
        traffic_writer.writerow([
            row['ts_utc'],
            row['ts_mt'],
            row['origin'],
            row['dest'],
            row['distance_text'],
            row['distance_meters'],
            row['duration_in_traffic_text'],
            row['duration_in_traffic_seconds'],
            row['duration_text'],
            row['duration_seconds']
    ])

