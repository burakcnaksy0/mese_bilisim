import random

days = 30  # number of days
monthlySumWeight = []  # monthly weight list
total_chicken = 0  # total number of chicken
for i in range(days):  # 1 , 2 , 3 , 4 , 5 .... 29 , 30
    dailyChicken = random.randint(1, 25000)  # 200 , 300 , 400  ..
    dailySumWeight = []
    for j in range(dailyChicken):
        weight = random.uniform(1.5, 5.5)
        dailySumWeight.append(weight)  # repair!!!!!!
    dailyTotalWeight = sum(dailySumWeight)
    print(i + 1, " . day total chicken : ", dailyChicken, "  and   total weights : ", dailyTotalWeight)
    monthlySumWeight.extend(dailySumWeight)  # The extends command combines lists.
    total_chicken += dailyChicken

print("  ")
print("total number of chickens : {} ".format(total_chicken))
print("sum weight of total chickens : {} ".format(sum(monthlySumWeight)))
print("average weight of total chickens : {} ".format(sum(monthlySumWeight) / total_chicken))
