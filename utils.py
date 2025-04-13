import asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from aiosmtplib import SMTP
from config import settings


async def send_email_async(
    sender_email: str,
    receiver_email: str,
    subject: str,
    body: str,
    smtp_server: str,
    smtp_port: int,
    login: str,
    password: str
):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    signature = settings.signature

    msg.attach(MIMEText(body + signature, 'html'))

    smtp = SMTP(hostname=smtp_server, port=smtp_port, start_tls=True)
    await smtp.connect()
    await smtp.login(login, password)
    await smtp.send_message(msg)
    await smtp.quit()


async def send_email_with_semaphore(
        sender_email: str,
        recipient_email: str,
        subject: str,
        body: str,
):
    async with asyncio.Semaphore(10):
        await send_email_async(
            sender_email,
            recipient_email,
            subject,
            body,
            settings.smtp_server,
            settings.smtp_port,
            settings.login,
            settings.password
        )
