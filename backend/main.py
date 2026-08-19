from fastapi import FastAPI
from backend.database import get_connection

app = FastAPI(
    title="Supply Prescript API",
    version="1.0.0",
)
@app.get("/")
def root():
    return {
        "message": "Supply Prescript API is running"
    }
@app.get("/health")
def health():
    return {
        "status": "ok",
        "database": "MySQL",
    }
@app.get("/health/database")
def database_health():
    try:
        connection = get_connection()

        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE()")
        database_name = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return {
            "status": "ok",
            "database": database_name,
        }

    except Exception as e:
        return {
            "status": "error",
            "database": "MySQL",
            "error": str(e),
        }