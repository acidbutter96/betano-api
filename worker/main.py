import logging
import redis
from playwright.sync_api import sync_playwright

from config import settings
from processing import process

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def main() -> int:
    # Initialize Redis connection
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True,
    )

    # Ensure Redis Stream exists (or create it if not)
    stream_name = settings.REDIS_STREAM_NAME
    redis_client.xgroup_create(
        stream_name,
        "processing_group",
        mkstream=True,
        ignore_exists=True,
    )

    def process_message(message_id, body):
        """Process a message with Playwright and acknowledge it."""
        job_id = body.get("job_id")
        logging.info("Starting processing job with id %s", job_id)

        with sync_playwright() as playwright:
            with playwright.chromium.launch(headless=True) as browser:
                process(body, browser=browser, job_id=job_id)

        logging.info("Finished processing job with id %s", job_id)
        # Acknowledge the message after successful processing
        redis_client.xack(stream_name, "processing_group", message_id)

    logging.info("Waiting for messages...")

    while True:
        # Blocking call to get new messages
        messages = redis_client.xreadgroup(
            groupname="processing_group",
            consumername="superbet_bot_consumer",
            streams={stream_name: ">"},
            count=1,
            block=0,  # Block indefinitely
        )

        for stream, msgs in messages:
            for message_id, body in msgs:
                process_message(message_id, body)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
