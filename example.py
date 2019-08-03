from numpy import random, empty, append
from matplotlib.pyplot import scatter, show
from pluster import pluster


def cluster():
    if random.rand() > 1/3:
        return 0
    return 1


def mixed_2_normal(n):
    samples = empty((0, 2), dtype='float32')
    for _ in range(n):
        if cluster() == 0:
            sample = random.multivariate_normal(
                [0, 0],
                [[2, 0], [0, 2]]
            )
        else:
            sample = random.multivariate_normal(
                [4, 4],
                [[1, 0], [0, 1]]
            )
        samples = append(samples, [sample], axis=0)
    return samples


samples = mixed_2_normal(100)
entries = pluster(samples, 1, 1)

for entry in entries.entries:
    x = entry.points[:, 0]
    y = entry.points[:, 1]
    scatter(x, y)

show()
