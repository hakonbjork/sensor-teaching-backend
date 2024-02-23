import datetime

# en case kan være at denne blir altfor full, så kanskje limite hvor mye info den kan ha om gangen eller noe
clickstream_data = []

def append_clickstream(clickstream):
    print(clickstream)
    clickstream_data.append(clickstream)

    dt_object = datetime.datetime.fromtimestamp(clickstream['timestamp']/1000)
    readable_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    clickstream_data.append(f"User clicked {clickstream['trigger']} at {readable_time}")

def get_newest_clickstream_setence():
    if clickstream_data:
        return clickstream_data[-1]
    else:
        return ""