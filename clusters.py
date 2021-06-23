from circulargrid import CircularGrid
import numpy as np
import pandas as pd


class Clusters(object):
    """ Class that clusters features. Code based on Trackpy library code"""

    @classmethod
    def from_grid(cls, grid, length, min_age):

        clusters = cls(range(length))
        for ring in grid.rings:
            for cell in ring.children:
                if cell.current_age < min_age:
                    continue
                neighbours = grid.get_neighbours(cell)
                for neighbour in neighbours:
                    if neighbour.current_age >= min_age:
                        clusters.add(cell.unique_id, neighbour.unique_id)
                        clusters.count_bonds(cell.unique_id, neighbour.unique_id)

        return clusters

    def __init__(self, indices):
        self.clusters = {i: {i} for i in indices}
        self.bonds = np.zeros(len(indices), dtype=int)
        self.pos_ids = list(indices)

    def __iter__(self):
        return (list(self.clusters[k]) for k in self.clusters)

    def add(self, a, b):
        i1 = self.pos_ids[a]
        i2 = self.pos_ids[b]
        if i1 != i2:  # if a and b are already clustered, do nothing
            self.clusters[i1] = self.clusters[i1].union(self.clusters[i2])
            for f in self.clusters[i2]:
                self.pos_ids[f] = i1
            del self.clusters[i2]

    def count_bonds(self, a, b):
        self.bonds[a] += 1
        self.bonds[b] += 1

    @property
    def cluster_size(self):
        result = [None] * len(self.pos_ids)
        for cluster in self:
            for f in cluster:
                result[f] = len(cluster)
        return result



datafile = 'prob_0.1.csv'
df = pd.read_csv(datafile)
df = df[df.t==0]

max_id = 0
cells_per_ring = len(df[df['parent_ring'] == 0])
num_of_rings = df['parent_ring'].max() + 1
grid = CircularGrid(num_of_rings, cells_per_ring)

for index, row in df.iterrows():
    ring = grid.rings[int(row['parent_ring'])]
    cell = ring.children[int(row['id'])]
    cell.current_age = row['age']
    cell.theta1 = row['theta1']
    cell.theta2 = row['theta2']

    if cell.unique_id > max_id:
        max_id = cell.unique_id

clusters = Clusters.from_grid(grid, max_id + 1, 40)
print(clusters.clusters)
print(clusters.cluster_size)