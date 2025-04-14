def check_list_length(lst):
    length = len(lst)
    if length < 5:
        print(f"The list has {length} elements, which is fewer than 5.")
    elif 5 <= length <= 10:
        print(f"The list has {length} elements, which is between 5 and 10 inclusive.")
    else:
        print(f"The list has {length} elements, which is more than 10.")

# List of test cases
test_cases = [
    [],                                      # 0 elements (fewer than 5)
    [1, 2, 3],                              # 3 elements (fewer than 5)
    [1, 2, 3, 4, 5],                        # 5 elements (between 5-10)
    ["a", "b", "c", "d", "e", "f"],         # 6 elements (between 5-10)
    list(range(10)),                         # 10 elements (between 5-10)
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],    # 11 elements (more than 10)
]

# Test all cases
for idx, case in enumerate(test_cases, 1):
    print(f"\nTest Case {idx}: {case}")
    check_list_length(case)  