import psycopg2
import os

# connection config
conn = psycopg2.connect(
    host="localhost",
    port=5434,
    dbname="/DB NAME/",
    user="/USER/",        
    password="/PASSWORD/"       
)
cur = conn.cursor()


# create staging table. it has index column, to be forgotten later
cur.execute("""
    CREATE TABLE IF NOT EXISTS staging_table (
        idx INTEGER,              -- This is the unwanted index column from CSV
        point_id INTEGER NOT NULL,
        tmin     DOUBLE PRECISION,
        tmax     DOUBLE PRECISION,
        tavg     DOUBLE PRECISION,
        rh_min   DOUBLE PRECISION,
        rh_max   DOUBLE PRECISION,
        rh_avg   DOUBLE PRECISION,
        prcp     DOUBLE PRECISION,
        wspd_min DOUBLE PRECISION,
        wspd_max DOUBLE PRECISION,
        wspd_avg DOUBLE PRECISION,
        date     DATE NOT NULL
    );
""")

# create final table (without index)
cur.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        point_id INTEGER NOT NULL, -- why not SERIAL?
        date DATE NOT NULL,
        tmin     DOUBLE PRECISION, -- maybe all DOUBLE PRECISION -> REAL? 6 digits of precision
        tmax     DOUBLE PRECISION,
        tavg     DOUBLE PRECISION,
        rh_min   DOUBLE PRECISION,
        rh_max   DOUBLE PRECISION,
        rh_avg   DOUBLE PRECISION,
        prcp     DOUBLE PRECISION,
        wspd_min DOUBLE PRECISION,
        wspd_max DOUBLE PRECISION,
        wspd_avg DOUBLE PRECISION,
        PRIMARY KEY (point_id, date)
    );
""")

# turning table into hypertable
cur.execute("SELECT create_hypertable('weather_data', 'date', if_not_exists => TRUE);")
conn.commit()


# /home/agromai/Development/ds-poseidon/data is mounted as /data on the Docker container:
# /home/agromai/Development/ds-poseidon/data:/data
#                                   fullPath:/alias
csv_paths = [
    "path/to/2019_daily_points.csv",
    "path/to/2020_daily_points.csv",
    "path/to/2021_daily_points.csv",
    "path/to/2022_daily_points.csv",
    "path/to/2023_daily_points.csv",
    "path/to/2024_daily_points.csv",
    "path/to/2025_daily_points.csv"
]

for file_path in csv_paths:
    print(f"Loading: {file_path}")
    with open(file_path, 'r') as f:
        cur.copy_expert("COPY staging_table FROM STDIN WITH CSV HEADER", f)
    conn.commit()
    print(f"Finished: {file_path}")

# feed itmes from intermediate table into the final table, leaving the unwanted columns
# also reorders the final table. .csv is: index  point_id  ..data..  date
#                                final table is: point_id    date  ..data..  

print("organizing from staging table to main table 'weather_data'")

cur.execute("""
    INSERT INTO weather_data (point_id, date, tmin, tmax, tavg, rh_min, rh_max, rh_avg, prcp, wspd_min, wspd_max, wspd_avg)
    SELECT point_id, date, tmin, tmax, tavg, rh_min, rh_max, rh_avg, prcp, wspd_min, wspd_max, wspd_avg
    FROM staging_table;
""")

conn.commit()

# delete intermediate table
print("Drop intermediate table")
cur.execute("DROP TABLE IF EXISTS staging_table;")
conn.commit()

print("end conn and cursor")
# clean up
cur.close()
conn.close()
