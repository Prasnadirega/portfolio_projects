-- Daily trip counts
SELECT DATE(start_time) AS trip_date, COUNT(*) AS trip_count
FROM citibike_tripdata
GROUP BY trip_date
ORDER BY trip_date;

-- Hourly trip counts
SELECT DATE(start_time) AS trip_date, EXTRACT(HOUR FROM start_time) AS hour, COUNT(*) AS trip_count
FROM citibike_tripdata
GROUP BY trip_date, hour
ORDER BY trip_date, hour;

--Average trip duration per day
SELECT DATE(start_time) AS trip_date, AVG(trip_duration)
FROM citibike_tripdata
GROUP BY trip_date
ORDER BY trip_date;

--Trip counts per user type
SELECT user_type, COUNT(*) AS trip_count
FROM citibike_tripdata
GROUP BY user_type;

--Trips by weather condition
SELECT w.date, 
			 CASE
         WHEN w.rain = 1 THEN 'Rainy'
         WHEN w.snow = 1 THEN 'Snowy'
       END AS weather_condition,
       COUNT(t.start_time) AS trip_count
FROM weather_data w
LEFT JOIN citibike_tripdata
ON DATE(t.start_time) = w.date
GROUP BY w.date, weather_condiion
ORDER BY w.date;