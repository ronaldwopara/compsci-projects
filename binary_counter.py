LED_1 = 12
LED_2 = 13
LED_3 = 11
LED_4 = 6


def get_binary_representation(number):
    binary_string = bin(number)[2:]  # [2:] to remove the '0b' prefix
    binary_digits = list(map(int, binary_string))
    return binary_digits

# Example usage:
input_number = 11
binary_representation = get_binary_representation(input_number)
print(binary_representation)

