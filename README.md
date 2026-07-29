# Retail ETL Pipeline

A portfolio project demonstrating a **Python-based ETL pipeline** for updating a retail company's database. The application is fully **Dockerized** and processes fictional retail data from JSON files through extraction, transformation, and loading (ETL), simulating a real-world retail data workflow.

> **Note**
> All data used in this project is fictional and intended for demonstration purposes only.

## ✨ Features

* Extracts retail data from JSON files.
* Transforms and validates the input data.
* Loads processed data into a relational database.
* Dockerized development environment for reproducibility.
* Modular Python codebase designed for maintainability and scalability.

## 🛠️ Tech Stack

* Python
* Docker & Docker Compose
* MySQL
* SQLAlchemy
* Pandas

## 📁 Project Structure

```text
.
├── data_raw/              # Raw input data (ignored by Git)
├── tests/                 # Sample output tables (future unit and integration tests)
├── utils/                 # Helper modules and utility functions
├── main.py                # Application entry point
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker image definition
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── TODO.md                # Planned features and 
```

## 🚀 Getting Started

### 1. Build and start the containers

```bash
docker-compose up --build -d
```

### 2. Open a shell inside the application container

```bash
docker exec -it RetailETL bash
```

### 3. Install dependencies (if needed)

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Update the requirements file

If new Python packages are installed:

```bash
pip freeze > requirements.txt
```

## 📝 Notes

* The `data_raw/` directory is intentionally excluded from version control.
* Test data directories are tracked without their contents.

## 🔮 Future Improvements

* More Bussiness processes tables.
* Unit and integration tests.

## 🎓 Portfolio

This project is intended for educational and portfolio purposes.
