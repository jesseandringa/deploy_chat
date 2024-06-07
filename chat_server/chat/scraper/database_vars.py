def get_db_vars():
    db_vars = {
        "PGUSER": "postgres",
        "PGPASSWORD": "Winterpark5!",
        "PGHOST": "database-1.cdcuami0ixkj.us-east-2.rds.amazonaws.com",
        "PGPORT": 5432,
        "PGDATABASE": "munidb",
        "DATABASE_URL": "postgresql://postgres:password@postgres:5432/postgres",
    }
    return db_vars
