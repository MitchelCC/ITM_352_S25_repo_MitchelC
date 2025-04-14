import random 
def assign_add_requirements(requirements):
    R1 = random.choice(requirements)
    requirements.remove(R1)

    R2 = random.choice(requirements)
    return R1, R2
add_requirements = ['Req1', 'Req2', 'Req3', 'Req4', 'Req5']
R1, R2 = assign_add_requirements(add_requirements)
print(f"Assigned Requirements: {R1} and {R2}")