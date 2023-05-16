from qiime2.plugin import Plugin, Int, Metadata, Str
from q2_types.feature_table import FeatureTable, Frequency
from q2_types.feature_data import FeatureData, Differential

from ._methods import absquant

plugin = Plugin(
    name="absquant",
    short_description="Absolute quantification",
    package="absquant",
    version="0.0.1",
    website="github.com/gibsramen/absquant"
)

input_descs = {
    "table": "Feature table",
}
param_descs = {
    "metadata": "Sample metadata",
    "formula": "Design formula",
    "output_dir": "Output directory",
    "njobs": "Number of jobs",
    "tmp_dir": "Temporary directory"
}

plugin.methods.register_function(
    function=absquant,
    inputs={"table": FeatureTable[Frequency]},
    parameters={
        "metadata": Metadata,
        "formula": Str,
        "output_dir": Str,
        "njobs": Int,
        "tmp_dir": Str
    },
    outputs=[
        ("results", FeatureData[Differential])
    ],
    input_descriptions=input_descs,
    parameter_descriptions=param_descs,
    output_descriptions={"results": "Results"},
    name="Absolute quant",
    description="Absolute quant"
)
