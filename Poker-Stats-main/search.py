def search(list, platform): # search for platform in list
# returns index or -1
    for i in range(len(list)):
        if list[i] == platform:
            return i
    return -1