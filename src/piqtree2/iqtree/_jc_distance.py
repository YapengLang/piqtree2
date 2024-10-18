from collections.abc import Sequence
from typing import Union

import cogent3
import cogent3.app.typing as c3_types
import numpy as np
from _piqtree2 import iq_jc_distances
from cogent3.evolve.fast_distance import DistanceMatrix

from piqtree2.iqtree._decorator import iqtree_func

iq_jc_distances = iqtree_func(iq_jc_distances, hide_files=True)


def _dists_to_distmatrix(
    distances: np.ndarray,
    names: Sequence[str],
) -> c3_types.PairwiseDistanceType:
    """Convert numpy representation of distance matrix
    into cogent3 pairwise distance matrix.

    Parameters
    ----------
    distances : np.ndarray
        Pairwise distances.
    names : Sequence[str]
        Corresponding sequence names.

    Returns
    -------
    c3_types.PairwiseDistanceType
        Pairwise distance matrix.
    """
    dist_dict = {}
    for i in range(1, len(distances)):
        for j in range(i):
            dist_dict[(names[i], names[j])] = distances[i, j]
    return DistanceMatrix(dist_dict)


def jc_distances(
    aln: Union[cogent3.Alignment, cogent3.ArrayAlignment],
) -> c3_types.PairwiseDistanceType:
    """Compute pairwise JC distances for a given alignemnt.

    Parameters
    ----------
    aln : Union[cogent3.Alignment, cogent3.ArrayAlignment]
        alignment to compute pairwise JC distances for.

    Returns
    -------
    c3_types.PairwiseDistanceType
        Pairwise JC distance matrix.
    """
    names = aln.names
    seqs = [str(seq) for seq in aln.iter_seqs(names)]

    distances = np.array(iq_jc_distances(names, seqs)).reshape((len(names), len(names)))
    return _dists_to_distmatrix(distances, names)