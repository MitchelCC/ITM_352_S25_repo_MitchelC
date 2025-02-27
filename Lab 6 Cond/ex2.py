def check_list_lenght(lst) :
    length = len(lst)
    if length < 5:
        print(f"The list has {length} elements")
       
    elif 5 <= length <= 10:
        print(f"The list has {length} elements, which is between 5 and 10 inclusive.")
    else:
        print(f"The list has {length} elements, which is greater than 10.")

#Test cases with lists of varying lenghts and different value types 
list1 = [1, 2, 'orange', True] 
list2 = [1, 2, 3, 4, 5]
list3 = ['a','b','c','d','e','f','g']
list4 = list(range(10))
list5 = [1, 'three', 'six', 7, 8,'red','blue', 3.14, True, False, None] 

check_list_lenght(list1)
check_list_lenght(list2)
check_list_lenght(list3)
check_list_lenght(list4)
check_list_lenght(list5)