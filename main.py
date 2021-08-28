import logging
import time
import datetime

from activity import ActivityEntry
from utils import DBConnection
from ctypes import windll, create_unicode_buffer

# Configure the logger that will be the output of this script
logging.basicConfig(filename='TimeTracker.log', filemode='w', level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


def get_foreground_window_title():
    """
    get the application name given hwnd.
    Foreground window is the window that is currently getting input
    """
    hwnd = windll.user32.GetForegroundWindow()
    if hwnd:
        length = windll.user32.GetWindowTextLengthW(hwnd)
        buf = create_unicode_buffer(length + 1)
        windll.user32.GetWindowTextW(hwnd, buf, length + 1)

        return buf.value if buf.value else None
    return None


if __name__ == '__main__':
    # use database sqlite3 to store historical data
    db_connection = DBConnection()
    db_connection.connect()
    db_connection.create_table('activities', ActivityEntry.get_keys())

    # Keep the program running and registering new activities
    # as we change from one activity to another
    start_time = None
    prev_active_window = ""
    prev_app = ""
    try:
        while True:
            new_activity_window = get_foreground_window_title()
            if new_activity_window is not None and prev_active_window != new_activity_window:
                # if it is a new window (activity)
                end_time = datetime.datetime.now()

                if start_time is not None:
                    # if it is not the first cycle... insert new activity
                    print(new_activity_window, start_time)
                    time_entry = ActivityEntry(str(prev_active_window), start_time, end_time)
                    time_entry_dict = time_entry.get_time_dict()
                    entry_keys = ', '.join([':{}'.format(k) for k in time_entry_dict.keys()])
                    db_connection.insert_entry_to_table('activities', time_entry_dict, entry_keys)

                # set when this activity started
                start_time = datetime.datetime.now()
                prev_active_window = new_activity_window
            time.sleep(0.5)     # we don't need to check for new activities that often
    except KeyboardInterrupt:
        print('bye')    # user ended the task pressing Ctrl + c
