import psycopg2

conn = psycopg2.connect(
    dbname='/DB NAME/', user='/USER/', password='/PASSWORD/', host='localhost', port=5434
)
cur = conn.cursor()

# Can be executed from psql
cur.execute("""
    CREATE EXTENSION IF NOT EXISTS postgis;
    CREATE EXTENSION IF NOT EXISTS postgis_topology;
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS brazil_grid (
        point_id     INTEGER NOT NULL,
        latitude     DOUBLE PRECISION,
        longitude    DOUBLE PRECISION,
        altitude     DOUBLE PRECISION,
        geom         geography(Point, 4326),
        PRIMARY KEY (point_id)
);
""")

with open('path/to/brazil_grid.csv', 'r') as f:
    next(f)  # ignore heade
    cur.copy_expert("COPY brazil_grid(point_id, latitude, longitude, altitude) FROM STDIN WITH CSV", f)

# Executing stuff from psql:
# docker exec -it /CONTAINER NAME/ bash
# psql -U /USER/ -d /DB NAME/

# Can be executed from psql
cur.execute("""
    UPDATE brazil_grid
    SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)::geography;
""")

# Can be executed from psql
cur.execute("""
    ALTER TABLE weather_data
    ADD CONSTRAINT fk_point
    FOREIGN KEY (point_id)
    REFERENCES brazil_grid(point_id);
""")

# Can be executed from psql
cur.execute("""
    CREATE OR REPLACE FUNCTION get_weather_data_nearby(
        lat DOUBLE PRECISION,
        lon DOUBLE PRECISION,
        start_date DATE,
        end_date DATE,
        radius_km DOUBLE PRECISION DEFAULT 20.0
    )
    RETURNS TABLE (
        point_id INTEGER,
        date     DATE,
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
        distance DOUBLE PRECISION
    ) AS $$
    BEGIN
        RETURN QUERY
        WITH target_point AS (
            SELECT ST_MakePoint(lon, lat)::geography AS geom
        ),
        nearby_points AS (
            SELECT gp.point_id, ST_Distance(gp.geom, tp.geom) AS distance
            FROM brazil_grid gp, target_point tp
            WHERE ST_DWithin(gp.geom, tp.geom, radius_km * 1000)
        )
        SELECT 
            c.point_id,
            c.date,
            c.tmin,
            c.tmax,
            c.tavg,
            c.rh_min,
            c.rh_max,
            c.rh_avg,
            c.prcp,
            c.wspd_min,
            c.wspd_max,
            c.wspd_avg,
            np.distance
        FROM weather_data c
        JOIN nearby_points np ON c.point_id = np.point_id
        WHERE c.date BETWEEN start_date AND end_date;
    END;
    $$ LANGUAGE plpgsql;
""")

conn.commit()
cur.close()
conn.close()
