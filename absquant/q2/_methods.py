import biom
import pandas as pd

import absquant.run as aq


def absquant(
    table: biom.Table,
    metadata: pd.DataFrame,
    formula: str,
    output_dir: str,
    njobs: int = None,
    tmp_dir: str = None
) -> pd.DataFrame:
    aq.absquant(
        table,
        metadata.to_dataframe(),
        formula,
        output_dir,
        njobs,
        tmp_dir
    )
    results = aq.collect(output_dir)
    results.index.name = "featureid"
    return results
