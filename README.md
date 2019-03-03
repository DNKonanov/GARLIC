# GARLIC finder

## Dependencies

* Python 3.4+
* 'gene-graph-lib' library

## Usage

This tool uses a graph form of genomes set representation, that is coded in sif format
To find some subgraph we need to describe it as a string template type in terminal

`python3 find_template_script.py --graph PATH_to_sif_file --template "TEMPLATE"`

for example

`python3 find_template_script.py --graph Escherichia_coli.sif --template "'1'>'2'; '2'>'3'; '1'>'3'"`

There are some optimized patterns, which can be computed faster than by universal algorithm
Such template can be chosen by `--type` option.


for example

`python3 find_template_script.py --graph Escherichia_coli.sif --type spider"`

Available templates:
* spider
* penguin
* garlic





### Language sprepecification
Добавть ребро между 1 и 2: ___'1' > '2'___ или ___'1' {PARAMS} '2'___
где:
___\'?\'___ имя переменной
**PARAMS**:
___l(min, max)___ - длина пути от min до max, по умолчанию ___l(1, 1)___
___g(name)___ - имя генома, по умолчанию ___graphbuilder.Graph.name_var + graphbuilder.Graph.var_index___
___w(min, max)___ - вес пути от min до max, по умолчанию ___w(1, -1)___
___u(min, max)___ - уникальные ребра в пути пути от min до max, по умолчанию ___u(0, -1)___
___n(ids...)___ - включаемые в путь ребра, по умолчанию ___n([])___

Параметры разделяются чимволом '___:___'
Например: ___'-1' > '0' {w(0,100):g(X_0)} '1' {u(20, 100):l(0, 100)} '2' {u(20, 100):n(1, 2, 3, 4, 5, 6, 7)}___

После вызова ___Graph.parse(str)___ получим на выходе список, в котром каждое ребро представляется как: ___[from, to, genome, weights, lengths, n, uniq]___

Во входных данных отдельные пути разделяются ___';'___

***Примеры***:
___'1'>'2'; '2' > '3';___ -> ___[[["'1'", "'2'", 'X_0', (1, -1), (1, 1), [], (0, -1)], ["'2'", "'3'", 'X_1', (1, -1), (1, 1), [], (0, -1)]], []]___
___
___'-1' > '0' {w(0,100):g(X_0)} '1' {u(20, 100):l(0, 100)} '2' {u(20, 100):n(1, 2, 3, 4, 5, 6, 7)}; '1' > '2'___ -> ___[[["'-1'", "'0'", 'X_1', (1, -1), (1, 1), [], (0, -1)], ["'0'", "'1'", 'X_0', (0, 100), (1, 1), [], (0, -1)], ["'2'", None, 'X_3', (1, -1), (1, 1), (20, 100), [1, 2, 3, 4, 5, 6, 7]], ["'1'", "'2'", 'X_4', (1, -1), (1, 1), [], (0, -1)]], [["'1'", "'2'", 'X_2', (1, -1), (0, 100), (20, 100), (0, -1)]]]___

___
___{l(100, 2000)}___ -> ___[[], [[None, None, 'X_0', (1, -1), (100, 2000), [], (0, -1)]]]___ 
