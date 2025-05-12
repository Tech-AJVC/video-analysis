#!/usr/bin/env python3

import threading
import time
import logging
import datetime
from typing import Optional, Callable

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("background_processing.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("background_scheduler")

# Import the necessary functions
from scheduler import process_new_applications


class BackgroundScheduler:
    """
    Background scheduler that runs in a separate thread alongside the Streamlit app.
    Processes new applications at 2 AM every day.
    """

    def __init__(self, target_hour: int = 2, target_minute: int = 0):
        self.target_hour = target_hour
        self.target_minute = target_minute
        self.thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        self.is_running = False
        self.last_run_date = None

    def _should_run_now(self) -> bool:
        """Check if it's time to run the scheduled job"""
        now = datetime.datetime.now()

        # If we've already run today, don't run again
        if self.last_run_date and self.last_run_date.date() == now.date():
            return False

        # Check if it's time to run (2 AM)
        return now.hour == self.target_hour and now.minute >= self.target_minute

    def _background_job(self):
        """The actual background job that runs in the thread"""
        logger.info("Background scheduler started")

        while not self.stop_event.is_set():
            try:
                # Check if it's time to run
                if self._should_run_now():
                    logger.info(f"Running scheduled job at {datetime.datetime.now()}")

                    # Process new applications
                    try:
                        num_processed = process_new_applications()
                        logger.info(f"Processed {num_processed} applications")
                    except Exception as e:
                        logger.error(f"Error processing applications: {str(e)}")

                    # Update last run date
                    self.last_run_date = datetime.datetime.now()
                    logger.info(f"Job completed. Next run at: {self.target_hour}:00 tomorrow")

                # Sleep for 60 seconds before checking again
                time.sleep(60)

            except Exception as e:
                logger.error(f"Error in background scheduler: {str(e)}")
                # Sleep a bit to avoid busy-waiting in case of persistent errors
                time.sleep(300)

    def start(self):
        """Start the background scheduler thread"""
        if self.is_running:
            logger.warning("Background scheduler is already running")
            return

        logger.info("Starting background scheduler")
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._background_job, daemon=True)
        self.thread.start()
        self.is_running = True
        logger.info(f"Background scheduler started, will run daily at {self.target_hour}:00 AM")

    def stop(self):
        """Stop the background scheduler thread"""
        if not self.is_running:
            return

        logger.info("Stopping background scheduler")
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=5)
        self.is_running = False
        logger.info("Background scheduler stopped")


# Global scheduler instance
scheduler = BackgroundScheduler()


def start_background_processing():
    """Start the background processing - call this from the Streamlit app"""
    scheduler.start()
    return scheduler


def stop_background_processing():
    """Stop the background processing - call this when shutting down"""
    scheduler.stop()