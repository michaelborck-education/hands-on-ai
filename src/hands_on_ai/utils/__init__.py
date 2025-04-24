"""
Shared utilities for hands-on-ai modules.
"""

import random
import time


def print_with_delay(messages, delay=0.8):
    """
    Print one of a list of messages with a delay.
    
    Args:
        messages (list): List of messages to choose from
        delay (float): Delay in seconds
    """
    msg = random.choice(messages) if isinstance(messages, list) else messages
    print(msg)
    time.sleep(delay)