# CONCEPTUAL

# [5, 6, 2, 3, 1, 4]
# we randomly select "3" and swap with the last element
# [5, 6, 2, 4, 1, 3]

# We'll use () to mark our "lesser than" pointer
# We'll use {} to mark our progress through the list

# [{(5)}, 6, 2, 4, 1, 3]
# {5} is not less than 3, so the "lesser than" pointer doesn't move

# [(5), {6}, 2, 4, 1, 3]
# {6} is not less than 3, so the "lesser than" pointer doesn't move

# [(5), 6, {2}, 4, 1, 3]
# {2} is less than 3, so we SWAP the values...
# [(2), 6, {5}, 4, 1, 3]
# Then we increment the "lesser than" pointer
# [2, (6), {5}, 4, 1, 3]

# [2, (6), 5, {4}, 1, 3]
# {4} is not less than 3, so the "lesser than" pointer doesn't move

# [2, (6), 5, 4, {1}, 3]
# {1} is less than 3, so we SWAP the values...
# [2, (1), 5, 4, {6}, 3]
# Then we increment the "lesser than" pointer
# [2, 1, (5), 4, {6}, 3]

# We've reached the end of the non-pivot values
# [2, 1, (5), 4, 6, {3}]
# Swap the "lesser than" pointer with the pivot...
# [2, 1, (3), 4, 6, {5}]


from random import randrange, shuffle


def quicksort(lst, start, end):
    # this portion of list has been sorted
    if start >= end:
        return
    print("Running quicksort on {0}".format(lst[start: end + 1]))
    # select random element to be pivot
    pivot_idx = randrange(start, end + 1)
    pivot_element = lst[pivot_idx]
    print("Selected pivot {0}".format(pivot_element))
    # swap random element with last element in sub-lists
    print(
        "Swapping the pivot element: {0} with the element at the end of the list: {1}".format(pivot_element, lst[end]))
    lst[end], lst[pivot_idx] = lst[pivot_idx], lst[end]
    print(lst)

    # tracks all elements which should be to left (lesser than) pivot
    less_than_pointer = start

    for i in range(start, end):
        # we found an element out of place
        if lst[i] < pivot_element:
            # swap element to the right-most portion of lesser elements
            print("Swapping {0} with {1} since it's less than the pivot".format(lst[i], lst[less_than_pointer]))
            lst[i], lst[less_than_pointer] = lst[less_than_pointer], lst[i]
            print(lst)
            # tally that we have one more lesser element
            less_than_pointer += 1
    # move pivot element to the right-most portion of lesser elements
    lst[end], lst[less_than_pointer] = lst[less_than_pointer], lst[end]
    print("""
    Swapping the pivot with the current lesser than since at this point,
    the list has been partitioned and everything with a lesser index than 
    less_than_pointer has a value lower than pivot_element
    """)
    print("{0} successfully partitioned".format(lst[start: end + 1]))
    # recursively sort left and right sub-lists
    quicksort(lst, start, less_than_pointer - 1)
    quicksort(lst, less_than_pointer + 1, end)


my_list = [5, 3, 1, 7, 4, 6, 2, 8]
shuffle(my_list)
print("PRE SORT: ", my_list)
quicksort(my_list, 0, len(my_list) - 1)
print("POST SORT: ", my_list)
