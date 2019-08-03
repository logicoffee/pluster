# ModuleNotFoundError: No module named '_swigfaiss'
# というエラーが出たら
# brew install libomp
from faiss import IndexFlatL2
from numpy import array


def approximate(pc, r):
    """
    Point Cloud を生成する確率分布の密度関数を f としたとき,
    f の近似　f' に対して f'(pc) を返す

    Parameters
    ----------
    pc : ndarray of float32
        Point Cloud
    r : float

    Returns
    -------
    approximated_values : ndarray of float32
        Point Cloud の各点における近似関数の値
    """
    pc = pc.astype('float32')
    size = len(pc)
    index = IndexFlatL2(len(pc[0]))
    index.add(pc)
    lim = index.range_search(pc, r)[0]
    return array([lim[i+1] - lim[i] for i in range(size)]) / (size * 2 * r)
