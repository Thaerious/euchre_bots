from collections import deque

def flatten(nested_list):
    """
    Flattens a list of lists into a single list.

    Args:
        nested_list (list of lists): The nested list to flatten.

    Returns:
        list: A single flat list containing all elements.
    """
    queue = list(nested_list)
    flat = []

    while queue:
        item = queue.pop()
        if isinstance(item, list):
            queue.extend(reversed(item))
        else:
            flat.append(item)

    return flat