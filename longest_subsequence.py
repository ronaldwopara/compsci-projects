dna_1 = "ACCGTT"
dna_2 = "CCAGCA"


def longest_common_subsequence(string_1, string_2):

    grid = [[0 for col in range(len(string_1) + 1)] for row in range(len(string_2) + 1)]

    for row in range(1, len(string_2) + 1):

        for col in range(1, len(string_1) + 1):

            if string_1[col - 1] == string_2[row - 1]:

                grid[row][col] = grid[row - 1][col - 1] + 1
            else:
                grid[row][col] = max(grid[row - 1][col], grid[row][col - 1])

    return grid


lcs = longest_common_subsequence(dna_1, dna_2)
print(lcs)


def lcs_value(grid, string_1, string_2):
    result = []
    for row in range(len(string_1) + 1, 1):
        for col in range(len(string_1) + 1, 1):
            if string_1[row] == string_2[col]:
                result.append(string_1[row])

    return result[::-1]


print(lcs_value(lcs, dna_1, dna_2))


