import asyncpg
from config import DATABASE_URL

class Database():
    def __init__(self):
        self.pool = None
    
    async def init_pool(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(DATABASE_URL)
        
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    insta_id TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id SERIAL PRIMARY KEY,
                    account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
                    shortcode TEXT NOT NULL UNIQUE,
                    media_type INTEGER,
                    caption TEXT,
                    hashtags TEXT[],
                    status TEXT DEFAULT 'pending', 
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX IF NOT EXISTS idx_posts_status ON posts(status);
            """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS post_phrase (
                    id SERIAL PRIMARY KEY,
                    text TEXT NOT NULL
                );
            """)

    async def get_phrase(self):
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT text FROM post_phrase LIMIT 1")
            if row:
                return row['text'] 
            
            return None
    
    async def add_refactor_phrase(self, phrase):
        async with self.pool.acquire() as conn:
            await conn.execute("""DELETE FROM post_phrase""")
            await conn.execute("""INSERT INTO post_phrase (text) VALUES ($1)""", phrase)
    
    async def delete_phrase(self):
        async with self.pool.acquire() as conn:
            await conn.execute("""DELETE FROM post_phrase""")

    async def get_accounts(self):
        async with self.pool.acquire() as conn:
            accounts_name = await conn.fetch("""SELECT id, name, insta_id FROM accounts ORDER BY created_at DESC""")

            return [{'id': item['id'], 'name': item['name'], 'insta_id': item['insta_id']} for item in accounts_name]
    
    async def get_shortcodes(self, account_id, max_taken=None):
        async with self.pool.acquire() as conn:
            shortcode = await conn.fetch(
                "SELECT shortcode FROM posts WHERE account_id=$1 ORDER BY id DESC LIMIT $2",
                account_id, 
                max_taken
            )

            return {item['shortcode'] for item in shortcode}

    async def add_insta_id(self, account_id, insta_id):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE accounts 
                SET insta_id = $1 
                WHERE id = $2
                """,
                str(insta_id),  
                account_id
            )

    async def add_post(self, account_id, shortcode, media_type=1, caption="", hashtags=[], status="pending"):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """INSERT INTO posts (account_id, shortcode, media_type, caption, hashtags, status) 
                VALUES ($1, $2, $3, $4, $5, $6)""",
                account_id, shortcode, media_type, caption, hashtags, status
            )
    
    async def get_pending_posts(self, limit=1):
        async with self.pool.acquire() as conn:
            pending_posts = await conn.fetch(
                "SELECT * FROM posts WHERE status = 'pending' ORDER BY id ASC LIMIT $1", 
                limit
            )
            return [dict(pending_post) for pending_post in pending_posts]

    async def update_status_post(self, post_id, status):
        async with self.pool.acquire() as conn:
            await conn.execute(
                    """
                    UPDATE posts
                    SET status = $1 
                    WHERE id = $2
                    """, 
                    status, post_id
                )

    async def get_one_account(self, id):
        async with self.pool.acquire() as conn:
            account = await conn.fetchrow("""SELECT id, name, created_at FROM accounts WHERE id = $1""", id)
            if account:
                return {'id': account['id'], 'name': account['name'], 'created_at': account['created_at']}
            else:
                return None

    async def delete_account(self, id):
        async with self.pool.acquire() as conn:
            await conn.execute("""DELETE FROM accounts WHERE id = $1""", id)

    async def update_account_name(self, id, name):
        async with self.pool.acquire() as conn:
            try:
                status = await conn.execute(
                    """
                    UPDATE accounts 
                    SET name = $1 
                    WHERE id = $2
                    """, 
                    name, id
                )

                if status == "UPDATE 0":
                    return "not_found"
                
                return "success"

            except asyncpg.UniqueViolationError:
                return "already_exists"
            
            except Exception as e:
                return "unknown_error"

    async def add_account(self, account_name):
        async with self.pool.acquire() as conn:
            try:
                result = await conn.fetchval(
                    """
                    INSERT INTO accounts (name) 
                    VALUES ($1) 
                    ON CONFLICT (name) DO NOTHING 
                    RETURNING name
                    """, 
                account_name
                )
            
                return result is not None

            except:
                return None


db = Database()