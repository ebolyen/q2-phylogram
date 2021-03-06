# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
"""
description:

    Helper script for generating all the files needed to view
    the interactive D3 phylogram (https://github.com/ConstantinoSchillebeeckx/phylogram_d3).

examples:

    make_d3_phylogram.py newick.tre -m otu_mapping.txt
    make_d3_phylogram.py newick.tre -m otu_mapping.txt -o data_dir

"""
import importlib

import qiime
from qiime.plugin import Plugin
from q2_phylogram import __version__
from q2_types import Phylogeny

# IMPORTS
import sys, os, argparse, traceback
import pandas as pd
import Bio.Phylo.Newick
import Bio.Phylo

template = '''
<!doctype html>

<html lang="en">

    <head>

        <!-- CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">
        <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Open+Sans" />
        <link href="https://cdn.rawgit.com/MasterMaps/d3-slider/master/d3.slider.css" rel="stylesheet">
        <link href="https://cdn.rawgit.com/ConstantinoSchillebeeckx/phylogram_d3/master/css/phylogram_d3.css" rel="stylesheet">

        <!-- JS -->
        <script type="text/javascript" src="https://code.jquery.com/jquery-2.2.4.min.js"></script>
        <script type="text/javascript" src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
        <script type="text/javascript" src="https://cdn.rawgit.com/mbostock/5577023/raw/5ee09dca6afdbef864de89d4d6caa3296f926f00/colorbrewer.min.js "></script>
        <script type="text/javascript" src="https://cdn.rawgit.com/jasondavies/newick.js/master/src/newick.js"></script>
        <script src="https://d3js.org/d3.v3.min.js"></script>
        <script src="http://labratrevenge.com/d3-tip/javascripts/d3.tip.v0.6.3.js"></script>
        <script type="text/javascript" src="https://cdn.rawgit.com/MasterMaps/d3-slider/master/d3.slider.js"></script>
        <script type="text/javascript" src="https://cdn.rawgit.com/ConstantinoSchillebeeckx/phylogram_d3/master/js/phylogram_d3.js"></script>
        <script type="text/javascript" src="https://cdn.rawgit.com/ConstantinoSchillebeeckx/phylogram_d3/master/js/utils.js"></script>

        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>

    REPLACE

        <!-- div for tree -->
        <div id='phylogram'></div>

    </body>
</html>
'''



# ------------------------------------------------------------------------------------------------------------#
# ------------------------------------------------- MAIN -----------------------------------------------------#
# ------------------------------------------------------------------------------------------------------------#
def make_d3_phylogram(output_dir: str, tree: Bio.Phylo.Newick.Tree, otu_metadata: qiime.Metadata) -> None:

    mapping_df = otu_metadata.to_dataframe()

    # ERROR CHECK INPUTS
    if isinstance(mapping_df, pd.DataFrame):

        leaves = set([l.name for l in tree.find_clades() if l.name])
        mapping_otus = set(mapping_df.index)

        if leaves > mapping_otus:
            print("Not all leaves were found in the OTU mapping file; as a consequence, these leaves cannot be styled.")


    # CONSTRUCT BODY TAG
    if isinstance(mapping_df, pd.DataFrame):
        body = '<body onload="init(\'dat/tree.tre\', \'#phylogram\', \'dat/mapping.txt\');">' 
    else:
        body = '<body onload="init(\'dat/tree.tre\', \'#phylogram\');">' 

    index = template.replace('REPLACE',body) # html to write to index.html


    # WRITE ALL OUR FILES
    # index.html, tree.tre, mapping.txt (optional)
    dat_dir = os.path.join(output_dir,'dat')
    if not os.path.exists(dat_dir):
        os.makedirs(dat_dir)
    with open(os.path.join(output_dir,'index.html'), 'w') as fout:
        fout.write(index)
    tree_out = os.path.join(dat_dir, 'tree.tre')
    Bio.Phylo.write(tree, tree_out, 'newick')
    if isinstance(mapping_df, pd.DataFrame):
        mapping_out = os.path.join(dat_dir, 'mapping.txt')
        mapping_df.to_csv(mapping_out, sep='\t')


    # FEEDBACK
    print("All your files have been written to the directory", output_dir)
    print("Simply open the file index.html in a browser that has")
    print("an internet connection to view the interactive phylogram.")



plugin = Plugin(
    name='phylogram',
    version=__version__,
    website='https://github.com/ConstantinoSchillebeeckx/q2-phylogram',
    package='q2_phylogram'
)

plugin.visualizers.register_function(
    function=make_d3_phylogram,
    inputs={'tree': Phylogeny},
    parameters={'otu_metadata': qiime.plugin.Metadata},
    name='Visualize phylogram',
    description='Generate interactive visualization of your phylogenetic tree.'
)

def tree_to_biopython_tree(data_dir):
    with open(os.path.join(data_dir, 'tree.nwk'), 'r') as fh:
        return Bio.Phylo.read(fh, 'newick')

plugin.register_data_layout_reader('tree', 1, Bio.Phylo.Newick.Tree, tree_to_biopython_tree)
