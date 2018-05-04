import IBM
import numpy as np

### Recreating HW2 problem 2 ###
# This uses the same vital rates and initial age structure as HW2 problem 2

# birth rates
m = np.array([0, 0.42, 3.5, 4.3, 4.8])
# survival rates
p = np.array([0.76, 0.84, 0.92, 0.95, 0.96])
# age classes:
# 0-6 years; 0 individuals
# 7-14 years; 100
# 15-27 years; 200
# 28-52 years; 400
# 53-74 years; 500
classes = np.array([6, 14, 27, 52, 74])

turtletown1 = IBM.create_pop(n=100, age_range=[7, 14], m_sigma=0, p_sigma=0)
turtletown1 = np.append(turtletown1, IBM.create_pop(n=200, age_range=[15, 27], m_sigma=0, p_sigma=0))
turtletown1 = np.append(turtletown1, IBM.create_pop(n=400, age_range=[28, 52], m_sigma=0, p_sigma=0))
turtletown1 = np.append(turtletown1, IBM.create_pop(n=500, age_range=[53, 74], m_sigma=0, p_sigma=0))

test1 = [IBM.simulate_pop(turtletown1, 30, m=m, p=p, age_classes=classes, r_sigma=0, m_sigma=0, p_sigma=0) for _ in range(5)]
print(test1)

### Adding environmental stochastiscity
test2 = [IBM.simulate_pop(turtletown1, 30, m=m, p=p, age_classes=classes, r_sigma=0.15, m_sigma=0, p_sigma=0) for _ in range(5)]

### Adding variation among individuals
turtletown2 = IBM.create_pop(n=100, age_range=[7, 14], m_sigma=0.15, p_sigma=0.15)
turtletown2 = np.append(turtletown2, IBM.create_pop(n=200, age_range=[15, 27], m_sigma=0.15, p_sigma=0.15))
turtletown2 = np.append(turtletown2, IBM.create_pop(n=400, age_range=[28, 52], m_sigma=0.15, p_sigma=0.15))
turtletown2 = np.append(turtletown2, IBM.create_pop(n=500, age_range=[53, 74], m_sigma=0.15, p_sigma=0.15))

test3 = [IBM.simulate_pop(turtletown2, 30, m=m, p=p, age_classes=classes, r_sigma=0, m_sigma=0.15, p_sigma=0.15) for _ in range(5)]

### Both environmental stochasticity and variation among individuals

test4 = [IBM.simulate_pop(turtletown2, 30, m=m, p=p, age_classes=classes, r_sigma=0.15, m_sigma=0.15, p_sigma=0.15) for _ in range(5)]

print("Population growth with no stochasticity")
print(test1[1])
print("Population growth with environmental stochasticity")
print(test2[1])
print("Population growth with individual variation")
print(test3[1])
print("Both sources of variation")
print(test4[1])

np.savetxt("/Users/scottericr/Downloads/test1.csv", np.transpose(test1), delimiter=",")
np.savetxt("/Users/scottericr/Downloads/test2.csv", np.transpose(test2), delimiter=",")
np.savetxt("/Users/scottericr/Downloads/test3.csv", np.transpose(test3), delimiter=",")
np.savetxt("/Users/scottericr/Downloads/test4.csv", np.transpose(test4), delimiter=",")