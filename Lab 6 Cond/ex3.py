def determine_progress1(hits, spins):
    if spins == 0:
        return "Get going!"
    
    hits_spins_ratio = hits / spins

    if hits_spins_ratio > 0:
        progress = "On your way!"
        if hits_spins_ratio >= 0.25:
            progress = "Almost there!"
            if hits_spins_ratio >= 0.5:
                if hits < spins:
                    progress = "You win!"
    else:
        progress = "Get going!"

    return progress
"""""
print(determine_progress1(0,0))
print(determine_progress1(0,5))
print(determine_progress1(1,1))
print(determine_progress1(2,5))
print(determine_progress1(5,10))
"""""
def test_determine_progress(progress_function) :
    #test case 1: spins = 0 return "Get going!"
    assert progress_function(10,0) == "Get going!", "Test Case 1 failed"

test_determine_progress(determine_progress1)
#test case 2: hits = 1, spins = 1 return "Almost there!"
assert determine_progress1(1,1) == "Almost there!", "Test Case 2 failed"

#test case 3: hits = 1, spins = 5 return "On your way!"
assert determine_progress1(1,5) == "On your way!", "Test Case 3 failed"

#test case 4: hits = 5, spins = 10 return "You win!"
assert determine_progress1(5,10) == "You win!", "Test Case 4 success!"

test_determine_progress(determine_progress1)