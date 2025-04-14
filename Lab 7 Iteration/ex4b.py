def check_fare(fare):
    """
    Checks if a fare is high or low and returns a message.
    :param fare: The fare amount (float or int).
    :return: A string indicating if the fare is high or low.
    """
    if fare > 12:
        return f"This fare is high! (${fare})"
    else:
        return f"This fare is low. (${fare})"
def process_fares(fares):
    """
    Processes a list of fares and prints messages for each fare.
    :param fares: A list of fare amounts (list of floats or ints).
    """
    for fare in fares:
        print(check_fare(fare))

# Test Case 1: Single high fare
assert check_fare(15.00) == "This fare is high! ($15.0)"

# Test Case 2: Single low fare
assert check_fare(10.50) == "This fare is low. ($10.5)"

# Test Case 3: Fare exactly equal to 12 (should be considered low)
assert check_fare(12.00) == "This fare is low. ($12.0)"

# Test Case 4: Negative fare (edge case)
assert check_fare(-5.00) == "This fare is low. ($-5.0)"

# Test Case 5: Zero fare (edge case)
assert check_fare(0.00) == "This fare is low. ($0.0)"

# Test Case 6: Large fare
assert check_fare(100.00) == "This fare is high! ($100.0)"

print("All test cases passed!")