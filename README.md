# GARLIC finder

## Dependencies

* Python 3.4+
* 'gene-graph-lib' library

## Usage

This tool uses a graph form of genomes set representation, that is coded in sif format.

To find some subgraph we need to describe it as a string template (see *Language specification* section)
Type in terminal

`python3 find_templates_script.py --graph PATH_to_sif_file --template "TEMPLATE"`

for example

`python3 find_templates_script.py --graph Escherichia_coli.sif --template "'1'>'2'; '2'>'3'; '1'>'3'"`

There are some optimized patterns, which can be computed faster than by universal algorithm
Such template can be chosen by `--type` option.


for example

`python3 find_templates_script.py --graph Escherichia_coli.sif --type spider"`

Available templates:
* spider
* penguin
* garlic





### Language specification
Add edge between 1 and 2: `'1' > '2'` or `'1' {PARAMS} '2'` where:
`'?'` -  name of vertex

**PARAMS**:
* `l(min, max)` - length of path from min to max, default `l(1, 1)`
* `g(name)` - genome name, default `Graph.name_var + graphbuilder.Graph.var_index`
* `w(min, max)` - weight of path from min to max, default `w(1, -1)`
* `u(min, max)` - count of uniq paths from min to max, default `u(0, -1)`
* `n(ids...)` - vertices that must contain the path  `n([])`

Parameters separator `:`
F.e.: `'-1' > '0' {w(0,100):g(X_0)} '1' {u(20, 100):l(0, 100)} '2' {u(20, 100):n(1, 2, 3, 4, 5, 6, 7)}`

`Graph.parse(str)` return all edges in this fromat: `[from, to, genome, weights, lengths, n, uniq]`, split by lenght ( is this edge shows path or simple edge)


**Some format**:

* `'1'>'2'; '2' > '3'` -> `[[["'1'", "'2'", 'X_0', (1, -1), (1, 1), [], (0, -1)], ["'2'", "'3'", 'X_1', (1, -1), (1, 1), [], (0, -1)]], []]`

* `'-1' > '0' {w(0,100):g(X_0)} '1' {u(20, 100):l(0, 100)} '2' {u(20, 100):n(1, 2, 3, 4, 5, 6, 7)}; '1' > '2'` -> `[[["'-1'", "'0'", 'X_1', (1, -1), (1, 1), [], (0, -1)], ["'0'", "'1'", 'X_0', (0, 100), (1, 1), [], (0, -1)], ["'2'", None, 'X_3', (1, -1), (1, 1), (20, 100), [1, 2, 3, 4, 5, 6, 7]], ["'1'", "'2'", 'X_4', (1, -1), (1, 1), [], (0, -1)]], [["'1'", "'2'", 'X_2', (1, -1), (0, 100), (20, 100), (0, -1)]]]`


* `{l(100, 2000)}` -> `[[], [[None, None, 'X_0', (1, -1), (100, 2000), [], (0, -1)]]]]`
