from datetime import timedelta, datetime
import pytz
def return_local_time(local_time, current_utc_offset, mission_start_or_deletion_utc):
    if current_utc_offset != mission_start_or_deletion_utc:
        local_time = local_time + timedelta(hours=int(mission_start_or_deletion_utc) - int(current_utc_offset))

    return local_time

def get_time(timezone_str, date):
    timezone = pytz.timezone(timezone_str)
    offset = timezone.utcoffset(datetime.now(timezone).replace(tzinfo=None)).total_seconds() / 3600
    return date + timedelta(hours=offset)