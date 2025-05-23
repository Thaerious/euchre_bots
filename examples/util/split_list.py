def split_list(my_list, count):
    """
    Splits a list into 'count' approximately equal parts.

    Args:
        my_list (list): The list to split.
        count (int): The number of chunks to divide the list into.

    Returns:
        list of lists: A list containing 'count' sublists.
    """    
    length = len(my_list)
    chunk_size = length // count
    remainder_size = length % count

    chunks = []
    start = 0
    for i in range(count):
        end = start + chunk_size
        if i < remainder_size: end += 1

        chunk = my_list[start:end]
        chunks.append(chunk)
        start = end
    
    return chunks