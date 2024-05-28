# My first attempt at the fibonacci algorithm using iterations and dynamic programming's memoization
def fibonacci_1(n):
    if n <= 1:
        return n
    # All fibonacci sequences start with 0 and 1
    memo1 = {
        0: [0], 1: [1]
    }
    # Creates a dictionary with each key having its two previous values
    for i in range(2, n + 1):
        memo1[i] = [i - 1, i - 2]

    for key, values in memo1.items():
        # Check if key is greater than 1
        if key > 1:
            # Update values if the value is present as a key in the dictionary
            # the entire list comprehension is replacing the original values in memo1[key]
            # with their two previous values by flattening the lists obtained from memo1[val]
            # for each val in the values list.

            memo1[key] = [item for sublist in [memo1[val] for val in values if val in memo1] for item in sublist]
            # [memo1[val] for val in values if val in memo1]
            # Result: [[1, 0], [1, 2]]
            # [item for sublist in [[1, 0], [1, 2]] for item in sublist]
            # Result: [1, 0, 1, 2]

    # the sum of values in tne nth key will be the answer for the nth term in the fibonacci sequence
    return sum(memo1[n])


# My second attempt at the algorithm using iterations and list building
def fibonacci_2(n):
    if n < 0:
        ValueError("Input 0 or greater only!")
    # All fibonacci sequences start with 0 and 1
    fibs = [0, 1]

    # if n is less than 1 or is 0 that means its index will be its value
    if n <= len(fibs) - 1:
        return fibs[n]

    # since it doesn't satisfy the statement on top and its value is greater than 1
    while n > len(fibs) - 1:
        # iteratively adds elements to the list until there n elements in the list
        fibs.append(fibs[-1] + fibs[-2])
    # therefore the last element will be the value we are looking for
    return fibs[-1]


# My third attempt at the algorthm using recursions and dynamic programming's memoization
# Initial memoization dictionary
memo = {}


def fibonacci_3(n):
    # Base case: If n is negative, return 0
    if n < 0:
        return 0

    # Base case: If n is 0 or 1, set memo[num] and return num
    if n == 0 or n == 1:
        memo[n] = n

    # Check if the result for n is already in the memo dictionary
    if n in memo:
        return memo[n]
    else:
        # Recursive calculation for Fibonacci
        answer = fibonacci_3(n - 1) + fibonacci_3(n - 2)

        # Memoize the result for n
        memo[n] = answer

        # Return the calculated Fibonacci value
        return answer


# My fourth attempt on the fibonacci sequence using pure recursions
def fibonacci_4(n):
    # Base case: If n is 0 or 1, return n since all fibonacci sequences start with 0 and 1
    if n == 0 or n == 1:
        return n
    else:
        # Recursive case: Calculate Fibonacci for n by summing the results of two previous Fibonacci numbers
        # Recursive call for the previous two numbers in the sequence
        previous_fib_1 = fibonacci_4(n - 1)
        previous_fib_2 = fibonacci_4(n - 2)

        # Sum the two previous Fibonacci numbers to get the Fibonacci number for n
        current_fib = previous_fib_1 + previous_fib_2

        # Return the calculated Fibonacci number for n
        return current_fib


print(fibonacci_2(5000))


# from analysis:
# 1 and 4 are much slower than 2 and 3
# but although 1 is slow it is still 3x faster than 4
