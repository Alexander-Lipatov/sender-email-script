from utils import send_email_with_semaphore, settings


if __name__ == "__main__":
    import asyncio

    recipients = settings.recipients

    async def main():
        tasks = [
            send_email_with_semaphore(
                sender_email=settings.sender_email,
                recipient_email=email,
                subject=settings.subject,
                body=settings.text
            )
            for email in recipients
        ]
        await asyncio.gather(*tasks)



    asyncio.run(main())