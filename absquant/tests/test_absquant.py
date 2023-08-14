from importlib_resources import files as resource
from tempfile import TemporaryDirectory
import pathlib

import biom
import pandas as pd
import pytest

from absquant.run import absquant

DATA_PATH = resource("absquant") / "tests/data"
MD_PATH = DATA_PATH / "rnai_sample_metadata_clean.txt"
TBL_PATH = DATA_PATH / "table.small.biom"


def test_full():
    tbl = biom.load_table(TBL_PATH)
    metadata = pd.read_table(MD_PATH, sep="\t")

    with TemporaryDirectory() as tmpdir:
        outdir = f"{tmpdir}/test"
        absquant(
            tbl,
            metadata,
            "host_subject_id",
            outdir
        )
        import os
        print(os.listdir(outdir))
    assert 0
