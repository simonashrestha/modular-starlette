from arq import create_pool
from arq.connections import RedisSettings
import smtplib
from email.mime.text import MIMEText

async def send_verification_email(ctx, email: str, username: str):
    # verification_link = f" https://good-externally-bat.ngrok-free.app/verify-email/{username}"
    ngrok_url = "https://good-externally-bat.ngrok-free.app"
    verification_link = f"{ngrok_url}/verify-email/{username}"
    msg = MIMEText(f"Please verify your email by clicking this link: {verification_link}")
    msg['Subject'] = 'Email Verification'
    msg['From'] = 'simonaashrestha@gmail.com' 
    msg['To'] = email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('simonaashrestha@gmail.com', 'kbygwsoiphtkqnle')
            server.send_message(msg)
        print(f"Verification email sent to {email}")

    except Exception as e:
        print(f"Failed to send email: {e}")

async def enqueue_verification_email(email: str, username: str):
    redis = await create_pool(RedisSettings())
    job = await redis.enqueue_job("send_verification_email", email, username)
    print(f"Job enqueued with ID: {job}")
        

