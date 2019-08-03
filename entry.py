from numpy import array, append, empty, delete


class Entry:
    def __init__(self, index):
        self.point_idxs = array([index])

    def has(self, point_idx):
        return point_idx in self.point_idxs

    def attach(self, point_idx):
        self.point_idxs = append(self.point_idxs, point_idx)
        return self

    def merge(self, entry):
        self.point_idxs = append(self.point_idxs, entry.point_idxs)
        return self

    @property
    def root_idx(self):
        return self.point_idxs[0]

    @property
    def points(self):
        return self.__points

    @points.setter
    def points(self, points):
        self.__points = points


class Entries:
    def __init__(self):
        self.entries = empty(0, dtype=Entry)

    def find_entry_idx_by_point(self, point_idx):
        for index, entry in enumerate(self.entries):
            if entry.has(point_idx):
                return index

    def create(self, entry):
        self.entries = append(self.entries, entry)

    def attach(self, entry_idx, point_idx):
        self.entries[entry_idx] = self.entries[entry_idx].attach(point_idx)

    def merge(self, from_idx, to_idx):
        from_entry = self.entries[from_idx]
        to_entry = self.entries[to_idx]
        self.entries[to_idx] = to_entry.merge(from_entry)
        self.entries = delete(self.entries, from_idx)
