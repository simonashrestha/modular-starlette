# from arq import ArqRedis
# from arq.connections import RedisSettings
# from tasks import send_verification_email

# class WorkerSettings:
#     redis_settings= RedisSettings(
#         host= 'localhost',
#         port= 6379,
#     )
#     functions= [send_verification_email]

# async def main():
#     redis= await ArqRedis(WorkerSettings.redis_settings).worker(WorkerSettings)
    