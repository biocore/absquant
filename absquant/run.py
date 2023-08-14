from collections import defaultdict
import pathlib
from importlib_resources import files as resource
import multiprocessing as mp
from subprocess import run
import tempfile

import biom
import pandas as pd

RSCRIPT = resource("absquant") / "absquant.R"


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


def collect(results_dir: str):
    results_dir = pathlib.Path(results_dir)
    coef_files = results_dir.glob("*.tsv")
    estimates = defaultdict(dict)
    pvalues = defaultdict(dict)

    usecols = ["Estimate", "Pr(>|z|)"]
    for f in coef_files:
        this_coef = pd.read_table(f, index_col=0)
        this_coef = this_coef[usecols]
        cov = this_coef.index.tolist()
        for cov, row in this_coef.iterrows():
            estimates[f.stem][f"{cov}_estimate"] = row["Estimate"]
            pvalues[f.stem][f"{cov}_pvalue"] = row["Pr(>|z|)"]

    estimate_df = pd.DataFrame(estimates).T
    pvalue_df = pd.DataFrame(pvalues).T

    results_df = pd.concat([estimate_df, pvalue_df], axis=1)
    return results_df


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
    depths = pd.Series(table.sum("sample").astype(int), index=samp_ids)
    pool = mp.Pool(njobs)

    for fid, counts in zip(
        feat_ids,
        table.iter_data(dense=True, axis="observation")
    ):
        counts = pd.Series(counts.astype(int), index=samp_ids,
                           name="abs_counts")
        data = metadata.copy()
        data["abs_counts"] = counts
        data["depth"] = depths
        data = data.dropna(subset="abs_counts")
        args = (data, formula, fid, output_dir, tmp_dir)
        pool.apply_async(run_absquant, args)

    pool.close()
    pool.join()
