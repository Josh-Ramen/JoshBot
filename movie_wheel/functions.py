def movie_queue_to_str(queue: list):
    if (len(queue) == 0):
        return "Nothing yet."
    elif (len(queue) == 1):
        return "*{}*".format(str(queue[0]))
    else:
        return "*{}* and *{}*".format(str(queue[0]), str(queue[1]))