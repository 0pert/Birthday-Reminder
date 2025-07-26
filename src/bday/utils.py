from datetime import datetime

def today():
    now = datetime.now().strftime("%Y-%m-%d")
    date_split = now.split("-")
    now = datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]))
    return now

def time_str_to_obj(str):
    date_split = str.split("-")
    output = datetime(
            int(date_split[0]), int(date_split[1]), int(date_split[2])
        )
    return output
