from arq import Worker, create_pool
from arq.connections import RedisSettings
from Email_Verification.email_tasks import send_verification_email

REDIS_SETTINGS = RedisSettings(
    host='localhost',
    port=6379,
    password=None 
)

async def startup(ctx):
    print("Worker starting up..")
    ctx['redis']= await create_pool(RedisSettings())
    print("Connected to Redis.")

async def shutdown(ctx):
    print("Worker shutting down..")

class WorkerSettings:
    redis_settings= RedisSettings()
    functions= [send_verification_email]
    on_startup= startup
    on_shutdown= shutdown

    
