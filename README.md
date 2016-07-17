# q2-phylogram

QIIME2 plugin for generating interactive [D3.js based phylograms](https://github.com/ConstantinoSchillebeeckx/phylogram_d3)

![Render](https://rawgit.com/ConstantinoSchillebeeckx/phylogram_d3/master/tree_rect.png "Rectangular tree type")
![Render](https://rawgit.com/ConstantinoSchillebeeckx/phylogram_d3/master/tree_radial.png "Radial tree type")

## Installing

Assuming [QIIME2 has been installed](https://github.com/qiime2/qiime2/wiki/Installing-and-using-QIIME-2), simply do the following:

```pip install https://github.com/ConstantinoSchillebeeckx/q2-phylogram/archive/master.zip```

## Usage

Convert input Newick tree to QIIME2 artifact:

```qiime tools import --type Phylogeny --input-path example/tree.tre --output-path tree.qza```

Generate visualization:

```qiime phylogram make_d3_phylogram --tree tree.qza --otu-metadata-file example/mapping.txt --visualization viz.qzv```
