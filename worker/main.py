import logging
import redis
import sys
import signal

from playwright.sync_api import sync_playwright

from settings import env
from processing import process

import os

running = True


# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def handle_signal(signum, frame):
    global running
    logging.info("Received exit signal (Ctrl + C). Shutting down gracefully.")
    running = False


# Register the custom signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, handle_signal)


def main() -> int:
    global running

    # Initialize Redis connection
    redis_client = redis.Redis(
        host=env.REDIS_HOST,
        port=env.REDIS_PORT,
        decode_responses=True,
    )

    logging.info(f"Redis ping {redis_client.ping()} at port {env.REDIS_PORT} and host {env.REDIS_HOST}")

    # Ensure Redis Stream exists (or create it if not)
    stream_name = env.REDIS_STREAM_NAME

    groups = [group['name'] for group in redis_client.xinfo_groups(stream_name) if group.get('name')]

    group_name = "processing_group"
    if group_name not in groups:
        redis_client.xgroup_create(
            stream_name,
            group_name,
            mkstream=True,
        )

    def process_message(message_id, body: dict):
        """Process a message with Playwright and acknowledge it."""
        job_id = body.get("job_id")
        logging.info(
            "Starting processing job with id %s",
            job_id,
        )

        try:
            with sync_playwright() as playwright:
                with playwright.chromium.launch(headless=False,) as browser:
                    process(
                        body=body,
                        browser=browser,
                        job_id=job_id,
                    )

            logging.info(
                "Finished processing job with id %s",
                job_id,
            )
            # Acknowledge the message after successful processing
            redis_client.xack(
                stream_name,
                group_name,
                message_id,
            )
        except Exception as e:
            logging.error(f"Failed to process job {job_id}: {e}")
            raise Exception(f"Failed to process job {job_id}")
            # In case of failure, do not acknowledge the message so it remains pending

    def retry_pending_messages():
        """Retry processing unacknowledged messages."""
        pending = redis_client.xpending_range(
            stream_name,
            group_name,
            min='-',
            max='+',
            count=10
        )

        for message in pending:
            message_id = message.get("message_id")

            if responses := redis_client.xrange(stream_name, min=message_id, max=message_id):
                for response in responses:
                    if not response:
                        continue

                    body = response[1]

                    logging.info(f"Retrying pending message with id {message_id}")
                    process_message(message_id, body)

    logging.info("Waiting for messages...")

    try:
        while running:
            # Blocking call to get new messages
            messages = redis_client.xreadgroup(
                groupname=group_name,
                consumername="superbet_bot_consumer",
                streams={stream_name: ">"},
                count=1,
                block=1000,
            )

            for stream, msgs in messages:
                for message_id, body in msgs:
                    process_message(message_id, body)

            # Retry pending messages
            retry_pending_messages()

        return 0
    except KeyboardInterrupt:
        logging.info("Received exit signal (Ctrl + C). Shutting down gracefully.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
