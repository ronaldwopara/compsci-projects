def dynamic_knapsack(weight_cap, weights, values):
    rows = len(weights) + 1
    cols = weight_cap + 1
    # Set up 2D array
    matrix = [[0] * cols for _ in range(rows)] # We want to create a table of rows that may include the weight's values that fall into the increasing number of weight capacities up to the actual weight capacity

    for index in range(1, rows):
        for weight in range(1, cols):
            if weights[index - 1] <= weight:
                matrix[index][weight] = max(
                    values[index - 1] + matrix[index - 1][weight - weights[index - 1]], matrix[index - 1][weight]) # We want to know whether the current weight that is under the current weight limit still has room for more, and if that combination of items is more profitable than the combination of items without it
            else:
                matrix[index][weight] = matrix[index - 1][weight] # If the current weight we are looking at, doesnt fall within the current weight limit, we save the previously more profitable combination of weights that doesnt include the current weight and is within the current weight limit.

    # Return the value of the bottom right of matrix
    return matrix[-1][-1]


# Test the function
weight_c = 5
weights_ = [3, 2, 1]
values_ = [6, 4, 3]
print(dynamic_knapsack(weight_c, weights_, values_))
