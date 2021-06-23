def search(list, platform): # search for platform in list
# returns index or -1
    for (i, item) in enumerate(list):
        if item == platform:
            return i
    return -1