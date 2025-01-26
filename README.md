# Ingestion and Analysis of NYC Taxi Data
## Project Overview
This project demonstrates the ingestion and analysis of NYC Taxi data using a variety of technologies. Additionally, it includes a Terraform demo showcasing the main features of the technology, independent of the data analysis workflow.

### Key Components
1. **Data Ingestion**
   - NYC Taxi data is ingested into a PostgreSQL database hosted in a Docker container.
   - The ingestion process is handled by a Python script running in a separate Docker container.

2. **Data Analysis**
   - The data is analyzed using SQL queries through **PGAdmin**, a graphical interface for managing and querying PostgreSQL databases.

3. **Terraform Demo**
   - A small infrastructure is deployed on **Google Cloud Platform (GCP)** using **Terraform**.
   - This section of the project is a standalone demo, showcasing Terraform's key features and is **not directly related to the NYC Taxi data workflow**.

> **Note:** The environment and tools used to test and develop this project are as follows: Windows 11, Git Bash terminal, Visual Studio Code, and Anaconda.

## Docker
### Run Docker Containers Individually
Network for communication between containers
```bash
docker network create pg-network
```

PostgreSQL container
```bash
winpty docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v //g/DE/ZoomCamp/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name pg-database \
    postgres:13
```
PGAdmin container

```bash
winpty docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4
```
### Use Docker Compose
Docker Compose simplifies the management of multiple containers by providing a tool to define and run multi-container Docker applications. In this project, it streamlines the setup and execution of the entire stack, ensuring a more structured and efficient workflow.
```bash
#Starts all the containers defined in the `docker-compose.yaml` file.
docker-compose up

#Stop containers
docker-compose down

#In detached mode
docker-compose up -d
```

## Data Pipeline Ingestion
### Building Docker Image
From the terminal running above the directory "ingestion_container", run
```bash
docker build -t taxi_ingest:v001 .
```
### Running Ingestion Container
```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

winpty docker run -it \
    --network=pg-network \
    taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --database=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```

## Terraform
Terraform is an open-source tool for managing infrastructure as code. It uses declarative configuration files to provision and manage resources across various platforms like GCP, Azure, and AWS.
### Setup
Download Terraform client and put it into PATH folder → “C:\Windows\System32”
### Apply Infrastructure to GCP
Install GCP SDK for Windows (CLI de gcloud). In GCP create a key for authentication and save the JSON key file.
> **Note:** To run the "gcloud" command from the Git Bash terminal, it is important to activate the Anaconda environment beforehand.
```bash
# Authenticate
export GOOGLE_APPLICATION_CREDENTIALS="YOURPATH/keys.json"
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS

# Above "terraform" directory
# Initialize terraform
terraform init

# Planned changes or architecture
terraform plan

# Apply or deploy the architecture
terraform apply

# Destroy the changes
terraform destroy
```
The variables file in the "terraform" directory helps improve the clarity and ease of understanding and running the Terraform main file.
## Analysis of Data
>**Note:** The datasets used in the analysis process were [green_tripdata](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz) and [zones](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
)
### Question 3
During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, respectively, happened:
- Up to 1 mile
- In between 1 (exclusive) and 3 miles (inclusive),
- In between 3 (exclusive) and 7 miles (inclusive),
- In between 7 (exclusive) and 10 miles (inclusive),
- Over 10 miles
```sql
SELECT
	SUM(CASE WHEN trip_distance <= 1.0 THEN 1 ELSE 0 END) AS custom_1,
	SUM(CASE WHEN trip_distance > 1.0 AND trip_distance <= 3.0 THEN 1 ELSE 0 END) AS custom_2,
	SUM(CASE WHEN trip_distance > 3.0 AND trip_distance <= 7.0 THEN 1 ELSE 0 END) AS custom_3,
	SUM(CASE WHEN trip_distance > 7.0 AND trip_distance <= 10.0 THEN 1 ELSE 0 END) AS custom_4,
	SUM(CASE WHEN trip_distance > 10 THEN 1 ELSE 0 END) AS custom_5
FROM
	green_taxi_data
WHERE
	DATE(lpep_dropoff_datetime) >= '2019-10-01' AND DATE(lpep_dropoff_datetime) < '2019-11-01';
```
Results: 104802, 198924, 109603, 27678, 35189
### Question 4
Which was the pick up day with the longest trip distance? Use the pick up time for your calculations
```sql
SELECT
	DATE(lpep_pickup_datetime),
	trip_distance
FROM
	green_taxi_data
ORDER BY
	trip_distance DESC
LIMIT 1
```
Result: 2019-10-31
### Question 5
Which were the top pickup locations with over 13,000 in total_amount (across all trips) for 2019-10-18?
```sql
SELECT
	z."Zone",
	SUM(t.total_amount) AS total_amount_sum
FROM
	green_taxi_data t
JOIN 
	zones AS z ON t."PULocationID" = z."LocationID"
WHERE
	DATE(t.lpep_pickup_datetime) = '2019-10-18'
GROUP BY
	z."Zone"
HAVING
    SUM(t.total_amount) > 13000
ORDER BY
	SUM(t.total_amount) DESC
```
Results
| Zone   | total_amount_sum      |
|-------------|---------------|
| East Harlem North | 18686.67999999975   |
| East Harlem South | 16797.25999999982   |
| Morningside Heights | 13029.789999999899   |

### Question 6
For the passengers picked up in October 2019 in the zone named "East Harlem North" which was the drop off zone that had the largest tip?
```sql
SELECT
	zd."Zone" AS drop_off_zone,
	t.tip_amount
FROM
	green_taxi_data t
JOIN 
	zones AS zd ON t."DOLocationID" = zd."LocationID"
JOIN
	zones AS zp ON t."PULocationID" = zp."LocationID"
WHERE
	DATE(t.lpep_pickup_datetime) >= '2019-10-01' AND DATE(t.lpep_pickup_datetime) < '2019-11-01' AND zp."Zone" = 'East Harlem North'
ORDER BY
	t.tip_amount DESC
LIMIT 1
```
Result
| Drop Off Zone | Tip Amount |
|---------------|------------|
| JFK Airport   | 87.3       |

## Conclusion
This project successfully ingests and analyzes NYC Taxi data using Docker, PostgreSQL, and Terraform. It identifies key travel trends, revenue hotspots, and tipping patterns, demonstrating the effective use of modern tools for scalable data workflows.