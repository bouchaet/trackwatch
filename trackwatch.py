import sys
import time


def print_marks(min_pace, max_pace, track_length):
    '''Print running marks based on the elapse time'''
    start_time = time.time()
    while True:
        delta = time.time() - start_time

        paces = ""
        for mark in get_boundaries(
                        delta,
                        min_pace,
                        max_pace,
                        track_length):
            pace = get_pretty_pace(delta, mark)
            paces = paces + f' {mark:g}m @ {pace}min/km '
            
        clocktime = get_pretty_time(delta)
        sys.stdout.write(f'\r{clocktime}{paces}')
        sys.stdout.flush()
        time.sleep(0.1)


def get_boundaries(total_time, min_pace, max_pace, length):
    '''Get significant distances'''
    quarter = length / 4
    if total_time < max_pace * (quarter / 1000) * 60:
        return []

    min_dist = total_time / (min_pace * 60) * 1000 
    max_dist = total_time / (max_pace * 60) * 1000

    boundaries = []
    done = False
    mark = min_dist - min_dist % quarter
    while not done:
        mark += quarter
        if mark > min_dist and mark < max_dist and is_std(mark, length):
            boundaries.append(mark)
        elif mark >= max_dist:
            if get_pace(total_time, mark) >= max_pace:
                boundaries.append(mark)
            done = True

    return boundaries


def is_std(distance, track_length):
    return (distance < 2 * track_length \
            or distance % 500 == 0 \
            or distance % track_length == 0)


def get_pretty_pace(total_time, length):
    pace = get_pace(total_time, length)
    seconds = int(((pace % 1) * 60) // 1)
    return f'{int(pace):02}:{seconds:02}'


def get_pace(total_time, length):
    return total_time/(length/1000) / 60


def get_pretty_time(total_seconds):
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    return f'{minutes:02}:{seconds:04.1f}'


if __name__ == "__main__":
    min_pace = 5.0
    max_pace = 2.75
    track_length = 400
    print_marks(min_pace, max_pace, track_length)