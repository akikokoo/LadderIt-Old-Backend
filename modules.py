from datetime import timedelta

def return_local_time(local_time, current_utc_offset, mission_start_or_deletion_utc):
    if current_utc_offset != mission_start_or_deletion_utc:
        local_time = local_time + timedelta(hours=int(mission_start_or_deletion_utc) - int(current_utc_offset))

    return local_time