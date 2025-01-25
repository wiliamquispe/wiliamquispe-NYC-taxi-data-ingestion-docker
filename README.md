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

## Conclusion

