from collections import Counter
import matplotlib.pyplot as plt

def simpson_diversity_index(species_counts):
    N = sum(species_counts.values())
    D = sum((n/N)**2 for n in species_counts.values())
    return D
# 1970
species_counts1 = {'lamprey': 4781, 'trout': 2874, 'splake': 290, 'salmon': 3400, 'alewife':622}
# 1971
species_counts2 = {'lamprey': 9613, 'trout': 2017, 'splake': 542, 'salmon': 2846, 'alewife': 3126}

sexratio = [13/7,7/3]
# Simpson
D1 = simpson_diversity_index(species_counts1)
D2 = simpson_diversity_index(species_counts2)
print(D1)
print(D2)
