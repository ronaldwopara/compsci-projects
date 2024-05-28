# Fibonacci function

#Brute Force Approach
def fib(n):
    # Base Case
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n -2)

# Memoized Approach
def fib_memo(n, memo = {}):
    if n in memo:
        return memo[n]
    if n <= 2:
        return 1
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]




# print(fib_memo(7))


# Grid_Traveller function

# Question:
# Say that you are a traveler on a 2D grid. 
# You begin in the top-left corner and your goal is to travel to the bottom-right corner. You may only move down or right.
# In how many ways can you travel to the goal on a grid with dimensions m * n?

# Brute force Approach
def grid_Traveller(m, n, memo = {}):
    if m == 1 or n == 1:
        return 1
    
    right = grid_Traveller(m, n-1)
    left = grid_Traveller(m-1, n)
    return right + left 

# print(grid_Traveller(16,16))

# Memoized Approach
def grid_traveller(m, n, memo={}):
    if (m, n) in memo:
        return memo[(m, n)]
    if m == 1 or n == 1:
        return 1
    right = grid_traveller(m, n - 1, memo)
    down = grid_traveller(m - 1, n, memo)
    memo[(m, n)] = right + down
    return memo[(m, n)]

# print(grid_traveller(3, 4))

# canSum function

# Question:
# Write a function 'canSum(targetSum, numbers) that takes in a targetSum and an array of numbers as arguments.
# The function should return a boolean 
# indicating whether or not it is possible to generate the targetSum using numbers from the array.
# You may use an element of the array as many times as needed.
# You may assume that all input numbers are nonnegative.

def canSum(targetSum, numbers):
    if targetSum < 0:
        return False
    if targetSum == 0 or 1 in numbers:
        return True
    
    for num in numbers:
        if canSum(targetSum - num, numbers):
            return True

    return False


print(canSum(12, [1]))