# Citi Bike & Weather Data Project

## Data Used
- **Citi Bike trip data** from Jersey City (2016)
- **Weather data** from Newark Airport (2016)

---

## Cleaning the Data
- Some bike data was missing or had unknown user info — kept as "unknown" for analysis.
- Found that 99% of user_type that were missing birth_year was Customer, whilst 
  1.5% were subscribers
- Found a few very long trip durations — kept but marked them.
- Removed useless or hard to connect columns in the weather data.
- Added simple rain/snow flags to the weather data.

---

## Loading into Database
- Loaded both datasets into **PostgreSQL** using Python (SQLAlchemy).
- Kept structure simple with just two tables: `citibike_tripdata` and `weather_data`.

---

## SQL Views Created
Made views to help with analysis:

- `daily_trip_counts`: trips per day  
- `hourly_trip_counts`: trips per hour  
- `avg_trip_duration_daily`: average trip length each day  
- `trip_counts_by_user_type`: how many trips by each user type  
- `avg_age_by_month`: rider age trends over months  
- `trips_weather_condition`: trips on clear, rainy, or snowy days  

These help spot patterns in ridership and how weather affects it.
