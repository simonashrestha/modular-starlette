# from arq import ArqRedis
# from arq.connections import RedisSettings
# import smtplib

# async def send_verification_email(ctx, email:str, verification_link: str):
#     try:
#         with smtplib.SMTP('smtp.example.com', 587) as server:
#             server.starttls()
#             server.login('your-email@example.com', 'your-password')
#             subject = "Verify your email"
#             body = f"Click the link to verify your email: {verification_link}"
#             message = f"Subject: {subject}\n\n{body}"
#             server.sendmail('your-email@example.com', email, message)
#         print(f"Verification email sent to {email}.")
#     except Exception as e:
#         print(f"Error sending email: {e}")