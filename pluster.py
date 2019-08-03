from numpy import argsort
from faiss import IndexFlatL2
from approximate import approximate
from entry import Entry, Entries


def pluster(pc, delta, tau):
    f = approximate(pc, 0.1)

    # sort point_cloud and f by f in ascending order
    sorted_idxs = argsort(f)
    f = f[sorted_idxs]
    pc = pc[sorted_idxs]

    lims, _, I = rips_graph(pc, delta)

    entries = Entries()

    for i in range(len(f)):
        nbr_idxs = I[lims[i]:lims[i+1]]
        upper_star_idxs = nbr_idxs[nbr_idxs < i]
        if upper_star_idxs.size == 0:
            # i is a local maximum
            entries.create(Entry(i))
        else:
            # i is not a local maximum
            entry_idx = entries.find_entry_idx_by_point(upper_star_idxs[0])
            entries.attach(entry_idx, i)
            entries = merge(pc, f, entries, i, upper_star_idxs, tau)

    return entries


def merge(pc, f, entries, i, upper_star_idxs, tau):
    for j in upper_star_idxs:
        main_entry_idx = entries.find_entry_idx_by_point(i)
        entry_idx = entries.find_entry_idx_by_point(j)
        root_idx = entries.entries[entry_idx].root_idx
        if entry_idx != main_entry_idx and f[root_idx] - f[i] < tau:
            entries.merge(entry_idx, main_entry_idx)

    main_entry_idx = entries.find_entry_idx_by_point(i)
    highest_entry_idx = None
    for j in upper_star_idxs:
        entry_idx = entries.find_entry_idx_by_point(j)
        root_idx = entries.entries[entry_idx].root_idx
        if (highest_entry_idx is None) or f[entries.entries[highest_entry_idx].root_idx] < f[root_idx]:
            highest_entry_idx = entry_idx

    if main_entry_idx != highest_entry_idx and f[entries.entries[highest_entry_idx].root_idx] - f[i] < tau:
        entries.merge(main_entry_idx, highest_entry_idx)

    for entry in entries.entries:
        entry.points = pc[entry.point_idxs]

    return entries


def rips_graph(point_cloud, delta):
    point_cloud = point_cloud.astype('float32')
    _, dim = point_cloud.shape
    index = IndexFlatL2(dim)
    index.add(point_cloud)

    return index.range_search(point_cloud, delta)
