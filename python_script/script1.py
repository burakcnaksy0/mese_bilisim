import random

num_chicken = 25000  # number of chickens
days = 30  # number of days

monthly_sum_weights = []  # monthly weight list
total_chickens = 0

for i in range(days):
    daily_chicken = random.randint(1, 25000)  # daily number of chickens       # 200 , 300 , 400 .....
    daily_sum_weights = []  # daily weight list
    for j in range(daily_chicken):
        weight = random.uniform(1.5, 5.5)
        daily_sum_weights.append(weight)
    daily_total_weight = sum(daily_sum_weights)
    print(f"{i + 1}. day: {daily_chicken} chickens, total weight: {daily_total_weight:}")
    monthly_sum_weights.extend(daily_sum_weights)  # combining lists
    total_chickens += daily_chicken

print(f"Total number of chickens: {total_chickens}")
print(f"Sum weight of total chickens: {sum(monthly_sum_weights):}")
print(f"Average weight of total chickens: {(sum(monthly_sum_weights) / total_chickens):}")
