import asyncpg

class PostgresChecker:
    def __init__(self, user: str, password: str, database: str, host: str):
        self.user = user
        self.password = password
        self.database = database
        self.host = host

    async def is_healthy(self) -> bool:
        try:
            conn = await asyncpg.connect(
                user=self.user,
                password=self.password,
                database=self.database,
                host=self.host
            )
            await conn.execute("SELECT 1")
            await conn.close()
            return True
        except Exception:
            return False
