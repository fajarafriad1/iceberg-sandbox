# Iceberg Sandbox (Spark + Iceberg + MinIO + Postgres + Trino)

This project provides a local Lakehouse environment using:

- Apache Spark 3.5
- Apache Iceberg (JDBC Catalog)
- PostgreSQL (Catalog backend)
- MinIO (S3-compatible object storage)
- Trino
- Gravitino

---

# Project Structure

    iceberg-sandbox/
    ├─ dataset/ # Raw dataset (versioned in Git)
    ├─ minio/
    │ └─ data/ # MinIO storage root (ignored by Git)
    ├─ postgres/
    │ ├─ data/ # Postgres data (ignored by Git)
    │ └─ init/ # Optional DB init scripts
    ├─ spark/
    ├─ notebooks/
    ├─ trino/
    ├─ docker-compose.yml
    └─ README.md


---

# First-Time Setup

---
## Initialize MinIO Storage

Create Required Folder:

```bash
mkdir -p minio/data/dataset
mkdir -p minio/data/iceberg/warehouse
```

Copy dataset into MinIO storage:

```bash
cp -r dataset/* minio/data/dataset/
```
---

## Build Containers

```bash
docker compose up -d --build
```
---

## Service Ports

| Service             | Container Port | Host Port | URL / Usage                                    | Description                |
| ------------------- | -------------- | --------- | ---------------------------------------------- | -------------------------- |
| Spark Master UI     | 8080           | 3080      | [http://localhost:3080](http://localhost:3080) | Spark cluster UI           |
| Spark Master (RPC)  | 7077           | 7077      | spark://localhost:7077                         | Spark cluster endpoint     |
| Spark Worker UI     | 8081           | 3081      | [http://localhost:3081](http://localhost:3081) | Spark worker UI            |
| Jupyter Notebook    | 8888           | 3888      | [http://localhost:3888](http://localhost:3888) | Spark notebook environment |
| Spark Driver Port   | 7078           | 7078      | Internal Spark driver communication            | Spark driver               |
| Spark Block Manager | 7079           | 7079      | Internal Spark communication                   | Spark block manager        |
| MinIO API (S3)      | 9000           | 9003      | [http://localhost:9003](http://localhost:9003) | S3-compatible API          |
| MinIO Console       | 9001           | 9004      | [http://localhost:9004](http://localhost:9004) | MinIO web UI               |
| Trino               | 8080           | 8085      | [http://localhost:8085](http://localhost:8085) | SQL query engine           |
| Gravitino API       | 8090           | 8090      | [http://localhost:8090](http://localhost:8090) | Gravitino REST API         |
| Gravitino Console   | 9001           | 9001      | [http://localhost:9001](http://localhost:9001) | Gravitino UI               |
| PostgreSQL          | 5432           | 5437      | localhost:5437                                 | Iceberg JDBC catalog       |

---

## Architecture Overview

| Component | Role                                     |
| --------- | ---------------------------------------- |
| Spark     | Data processing & Iceberg table creation |
| Postgres  | Iceberg JDBC Catalog                     |
| MinIO     | S3-compatible warehouse storage          |
| Trino     | Query engine                             |
| Gravitino | Metadata governance                      |

---

## Quick Access Links

- Spark Master UI → http://localhost:3080
- Spark Worker UI → http://localhost:3081
- Jupyter → http://localhost:3888
- MinIO Console → http://localhost:9004
- Trino → http://localhost:8085
- Gravitino → http://localhost:8090

---

## Iceberg Configuration

Spark Catalog Configuration:

```python
.config("spark.sql.catalog.iceberg_jdbc", "org.apache.iceberg.spark.SparkCatalog")
.config("spark.sql.catalog.iceberg_jdbc.catalog-impl", "org.apache.iceberg.jdbc.JdbcCatalog")
.config("spark.sql.catalog.iceberg_jdbc.uri", "jdbc:postgresql://iceberg-sandbox-postgres:5432/iceberg-jdbc-catalog")
.config("spark.sql.catalog.iceberg_jdbc.warehouse", "s3a://iceberg/warehouse")
```

Dataset Read Path:

```python
.csv("s3a://dataset/ecommerce_order_dataset/train/df_Customers.csv")
```
