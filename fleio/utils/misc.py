import time


def wait_for(check_function, max_time=65, check_sleep=1):
    """
    Wait until :param check_function: call return true. At most :param max_time: seconds.
    Check is performed every :param check_sleep: seconds.

    :param check_function: callable that returns True when condition is met
    :param max_time: maximum number of seconds to wait for condition to be True
    :param check_sleep: seconds to sleep between checks
    :return: True if :param check_function: returns true, False is check times out.
    """
    start_time = time.time()
    elapsed_time = 0

    while elapsed_time < max_time:
        if check_function():
            return True
        time.sleep(check_sleep)
        elapsed_time = time.time() - start_time
    return False
