import pathlib
from pkg_resources import resource_filename
import multiprocessing as mp
from subprocess import run
import tempfile

import biom
import pandas as pd

RSCRIPT = resource_filename("absquant", "absquant.R")

def run_absquant(
    data: pd.DataFrame,
    formula: str,
    feat_name: str,
    output_dir: pathlib.Path,
    tmp_dir: pathlib.Path = None
):
    with tempfile.NamedTemporaryFile(dir=tmp_dir) as f:
        data.to_csv(f.name, sep="\t", index=True)
        args = ["Rscript", RSCRIPT, f.name, formula, output_dir, feat_name]
        run(args)


def absquant(
    table: biom.Table,
    metadata: pd.DataFrame,
    formula: str,
    output_dir: str,
    njobs: int = None,
    tmp_dir: str = None
):
    output_dir = pathlib.Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=False)

    samp_ids = table.ids("sample")
    feat_ids = table.ids("observation")
    pool = mp.Pool(njobs)

    for fid, counts in zip(
        feat_ids,
        table.iter_data(dense=True, axis="observation")
        ):
        counts = pd.Series(counts.astype(int), index=samp_ids,
                           name="abs_counts")
        data = metadata.copy()
        data["abs_counts"] = counts
        data = data.dropna(subset="abs_counts")
        args = (data, formula, fid, output_dir, tmp_dir)
        pool.apply_async(run_absquant, args)

    pool.close()
    pool.join()
