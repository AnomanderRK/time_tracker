class ActivityEntry:
    def __init__(self, name, start_time, end_time):
        """
        object for new activities. e.g. using office, using chrome, etc
        Parameters
        ----------
        name:
            name of the activity
        start_time:
            start time. When the activity started yyyy-mm-dd-hh-mm-ss
        end_time
            When the activity started yyyy-mm-dd-hh-mm-ss
        """
        self.activity_name = name
        self.start_time = start_time
        self.end_time = end_time
        self.time_difference = None
        self.days = None
        self.hours = None
        self.minutes = None
        self.seconds = None
        self._get_specific_times()

    @staticmethod
    def get_keys():
        """Get a string with all the needed keys returned by the get_time_dict and the expected types for db"""
        return "activity text, start_time text, end_time text, days int, hours int, minutes int, seconds int"

    def _get_specific_times(self):
        """calculates all the time related variables based on start, end times"""
        self.time_difference = self.end_time - self.start_time
        self.days = self.time_difference.days
        self.seconds = self.time_difference.seconds
        self.hours = self.days * 24 + self.seconds // 3600
        self.minutes = (self.seconds % 3600) // 60
        self.seconds = self.seconds % 60

    def get_time_dict(self):
        """get time entry dict"""
        return {
            "activity" : self.activity_name,
            "start_time": self.start_time.strftime("%Y-m-%d %H:%M:%S"),
            "end_time": self.end_time.strftime("%Y-m-%d %H:%M:%S"),
            "days": self.days,
            "hours": self.hours,
            "minutes": self.minutes,
            "seconds": self.seconds,
        }
