

from datetime import datetime, timezone
import os
import sqlite3
import typing as t
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
import googlemaps


load_dotenv() # MAPS_API_KEY, ORIGINS, DESTINATIONS
gmaps = googlemaps.Client(key=os.environ['MAPS_API_KEY'])


trips_to = gmaps.distance_matrix(
    origins=os.environ['ORIGINS']
    , destinations=os.environ['DESTINATIONS']
    , mode='driving'
    , avoid='tolls'
    , departure_time='now' # datetime.now(timezone.utc) + timedelta(hours=59)
    , traffic_model='best_guess'
)
trips_from = gmaps.distance_matrix(
    origins=os.environ['DESTINATIONS']
    , destinations=os.environ['ORIGINS']
    , mode='driving'
    , avoid='tolls'
    , departure_time='now' # datetime.now(timezone.utc) + timedelta(hours=59)
    , traffic_model='best_guess'
)
ts_utc = datetime.now(timezone.utc)
ts_mt = ts_utc.astimezone(ZoneInfo('America/Denver'))


def format_response(resp: t.Dict) -> t.List[t.Dict[str, str]]:
    """
    Flatten the API response into a list of dicts. Each dict represents
    a single row to be inserted into the database.
    """
    records = []
    for i, origin in enumerate(resp['origin_addresses']):
        for j, dest in enumerate(resp['destination_addresses']):
            print(i, j)
            _this = resp['rows'][i]['elements'][j]
            records.append({
                "ts_utc": str(ts_utc),
                "ts_mt": str(ts_mt),
                "origin": origin,
                "dest": dest,
                "distance_text": _this['distance']['text'],
                "distance_meters": _this['distance']['value'],
                "duration_in_traffic_text": _this['duration_in_traffic']['text'],
                "duration_in_traffic_seconds": _this['duration_in_traffic']['value'],
                "duration_text": _this['duration']['text'],
                "duration_seconds": _this['duration']['value'],
            })
    return records


trips_to_insert = format_response(trips_to)
trips_to_insert.extend(format_response(trips_from))


con = sqlite3.connect("db")
con.row_factory = sqlite3.Row
cur = con.cursor()


cur.execute(
"""
    create table if not exists traffic(
        ts_utc,
        ts_mt,
        origin,
        dest,
        distance_text,
        distance_meters,
        duration_in_traffic_text,
        duration_in_traffic_seconds,
        duration_text,
        duration_seconds
)            
""")
con.commit()

cur.executemany(
"""
    insert into traffic (
        ts_utc,
        ts_mt,
        origin,
        dest,
        distance_text,
        distance_meters,
        duration_in_traffic_text,
        duration_in_traffic_seconds,
        duration_text,
        duration_seconds
    ) VALUES(
        :ts_utc,
        :ts_mt,
        :origin,
        :dest,
        :distance_text,
        :distance_meters,
        :duration_in_traffic_text,
        :duration_in_traffic_seconds,
        :duration_text,
        :duration_seconds
    )
""", trips_to_insert)
con.commit()

