def clean_logs(log_list: list, keep_last: int = 100):
    return log_list[-keep_last:]