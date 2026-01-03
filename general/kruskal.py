import math
import numpy as np

def run_mc(num_runs, num_places=100):
    sum_p = sum_p2 = 0.
    for _ in range(num_runs):
        steps = np.random.randint(1, 11, num_places)
        for i in range(num_places - 1, -1, -1):
            j = i + steps[i]
            if j < num_places: steps[i] = steps[j]
        init = np.zeros(10, dtype=int)
        for i in range(10): init[steps[i]-1] += 1
        p = init.dot(init)/100
        sum_p += p
        sum_p2 += p*p
    sum_p /= num_runs
    sum_p2 /= num_runs

    return sum_p, math.sqrt((sum_p2 - sum_p * sum_p) / num_runs)

def mc_results(num_runs):
    p, dev = run_mc(num_runs)
    print('probability: {:.5f}'.format(p))
    print('std error  : {:.5f}'.format(dev))

# mc_results(400000)

num_places=100

# 1d probs
probs0 = np.zeros(num_places)
probs1 = np.zeros(num_places)
probs1[:10] = 0.1
probs0[0] = 1.
for i in range(1, num_places):
    probs0[i] += probs0[max(i-10, 0):i].sum() * 0.1
    probs1[i] += probs1[max(i-10, 0):i].sum() * 0.1

probs2 = np.zeros(shape=(num_places, num_places))
probs_couple = np.zeros(num_places)

for i in range(num_places):
    for j in range(num_places):
        p = probs2[max(i-10, 0):i, max(j-10, 0):j].sum() * 0.01  # prob of jumping in both x and y dim
        if j < i:
            p -= probs2[j, max(j-10, 0):j].sum() * probs0[i-j] * 0.1
        if i < j:
            p -= probs2[max(i-10, 0):i, i].sum() * probs0[j-i] * 0.1
        if i < 10:
            p += 0.1 * probs1[j]  # prob of starting in x dim
            if i < j:
                p -= 0.1 * probs1[i] * probs0[j-i]
        if j < 10:
            p += 0.1 * probs1[i]  # prob of starting in y dim
            if j < i:
                p -= 0.1 * probs1[j] * probs0[i - j]
        if i < 10 and j < 10:
            p -= 0.01  # subtract off prob of starting in x and y dim
        if i != j:
            probs2[i, j] = p
        else:
            probs_couple[i] = p

coincidence_prob = 0.
for i in range(-10, 0):
    for j in range(-10, 0):
        coincidence_prob += probs2[i, j] * 0.01 * (11 - max(-i, -j))

print('coupling prob:', sum(probs_couple))
print('coincidence  :', coincidence_prob)
print('total prob   :', sum(probs_couple) + coincidence_prob)

