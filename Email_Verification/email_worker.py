from arq import Worker, create_pool
from arq.connections import RedisSettings
from Email_Verification.email_tasks import send_verification_email
import os

# Retrieve Redis settings from environment variables or use default values
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)

REDIS_SETTINGS = RedisSettings(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD
)

async def startup(ctx):
    print("Worker starting up..")
    ctx['redis'] = await create_pool(REDIS_SETTINGS)
    print("Connected to Redis.")

async def shutdown(ctx):
    print("Worker shutting down..")

class WorkerSettings:
    redis_settings = REDIS_SETTINGS
    functions = [send_verification_email]
    on_startup = startup
    on_shutdown = shutdown



    


