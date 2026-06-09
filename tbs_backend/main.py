from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import os
import redis
import json

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        )

redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "redis"),
        port=6379,
        db=0,
        decode_responses=True
        )

@app.get("/games")
def get_games():
    try:
        cached_games = redis_client.get("games_schedule")
        if cached_games:
            return {"status": "success", "source": "redis (cache)", "data": json.loads(cached_games)}

        connection = mysql.connector.connect(
                host=os.getenv("DB_HOST", "db"),
                user="root",
                password=os.getenv("DB_PASSWORD", "rootpassword"),
                database=os.getenv("DB_NAME", "tbsdb")
                )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM games;")
        games = cursor.fetchall()

        for game in games:
            if 'game_date' in game:
                game['game_date'] = str(game['game_date'])

        redis_client.setex("games_schedule", 60, json.dumps(games))

        return {"status": "success", "source": "mysql (db)", "data": games}

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
