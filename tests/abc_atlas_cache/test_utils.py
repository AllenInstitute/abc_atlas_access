import hashlib
import numpy as np
from abc_atlas_access.abc_atlas_cache import utils


def test_file_hash_from_path(tmpdir):

    rng = np.random.default_rng(seed=881)
    alphabet = list('abcdefghijklmnopqrstuvwxyz')
    fname = tmpdir / 'hash_dummy.txt'
    with open(fname, 'w') as out_file:
        for ii in range(10):
            out_file.write(''.join(rng.choice(alphabet, size=10)))
            out_file.write('\n')

    hasher = hashlib.md5()
    with open(fname, 'rb') as in_file:
        chunk = in_file.read(7)
        while len(chunk) > 0:
            hasher.update(chunk)
            chunk = in_file.read(7)

    ans = utils.file_hash_from_path(fname)
    assert ans == hasher.hexdigest()
