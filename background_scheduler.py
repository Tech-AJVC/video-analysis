#!/usr/bin/env python3

import threading
import time
import logging
import datetime
from typing import Optional, Callable
from apscheduler.schedulers.background import BackgroundScheduler as APScheduler
from apscheduler.triggers.cron import CronTrigger

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
        self.scheduler: Optional[APScheduler] = None
        self.is_running = False
        self.last_run_date = None

    def _should_run_today(self) -> bool:
        """Check if we should run today (haven't run yet today)"""
        now = datetime.datetime.now()
        # If we've already run today, don't run again
        return not (self.last_run_date and self.last_run_date.date() == now.date())

    def _background_job(self):
        """The actual background job that runs daily at 2 AM"""
        # Check if we should run today (prevent duplicate runs)
        if not self._should_run_today():
            logger.info("Job already ran today, skipping")
            return

        logger.info(f"Running scheduled job at {datetime.datetime.now()}")

        try:
            # Process new applications
            num_processed = process_new_applications()
            logger.info(f"Processed {num_processed} applications")
            
            # Update last run date
            self.last_run_date = datetime.datetime.now()
            logger.info(f"Job completed successfully. Next run tomorrow at {self.target_hour}:00 AM")
            
        except Exception as e:
            logger.error(f"Error processing applications: {str(e)}")

    def start(self):
        """Start the background scheduler"""
        if self.is_running:
            logger.warning("Background scheduler is already running")
            return

        logger.info("Starting background scheduler")
        
        # Initialize APScheduler
        self.scheduler = APScheduler()
        
        # Add daily job at 2 AM
        self.scheduler.add_job(
            func=self._background_job,
            trigger=CronTrigger(hour=self.target_hour, minute=self.target_minute),
            id='daily_processing',
            replace_existing=True,
            max_instances=1  # Prevent overlapping runs
        )
        
        # Start the scheduler
        self.scheduler.start()
        self.is_running = True
        logger.info(f"Background scheduler started, will run daily at {self.target_hour}:00 AM")

    def stop(self):
        """Stop the background scheduler"""
        if not self.is_running:
            return

        logger.info("Stopping background scheduler")
        
        if self.scheduler:
            self.scheduler.shutdown(wait=False)
            self.scheduler = None
            
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