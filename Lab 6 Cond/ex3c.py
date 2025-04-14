def determine_progress3(hits, spins):
    if spins == 0:
        return "Get going!"
    
    hits_spins_ratio = hits / spins

    if hits_spins_ratio >= 0.5 and hits < spins:
        return "You win!"
    elif hits_spins_ratio >= 0.25:
        return "Almost there!"
    elif hits_spins_ratio > 0:
        return "On your way!"
    else:
        return "Get going!"

# Test cases
print(determine_progress3(0, 0))  # Expected: "Get going!"
print(determine_progress3(0, 5))  # Expected: "Get going!"
print(determine_progress3(1, 1))  # Expected: "Almost there!"
print(determine_progress3(2, 5))  # Expected: "On your way!"
print(determine_progress3(5, 10)) # Expected: "You win!"

def test_determine_progress(progress_function):
    # Test case 1: spins = 0 return "Get going!"
    assert progress_function(10, 0) == "Get going!", "Test Case 1 failed"
    
    # Test case 2: hits = 1, spins = 1 return "Almost there!"
    assert progress_function(1, 1) == "Almost there!", "Test Case 2 failed"
    
    # Test case 3: hits = 1, spins = 5 return "On your way!"
    assert progress_function(1, 5) == "On your way!", "Test Case 3 failed"
    
    # Test case 4: hits = 5, spins = 10 return "You win!"
    assert progress_function(5, 10) == "You win!", "Test Case 4 failed"

# Run the test cases
test_determine_progress(determine_progress3)