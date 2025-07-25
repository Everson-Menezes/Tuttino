import aiopg

class PostgresChecker:
    def __init__(self, user: str, password: str, database: str, host: str):
        self.user = user
        self.password = password
        self.database = database
        self.host = host

    async def is_healthy(self) -> bool:
        dsn = f"dbname={self.database} user={self.user} password={self.password} host={self.host}"
        try:
            async with aiopg.connect(dsn) as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT 1")
                    await cur.fetchone()
            return True
        except Exception:
            return False
        