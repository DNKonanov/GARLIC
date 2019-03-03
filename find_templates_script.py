from search.VF2_find_template import find_template
import argparse
from gene_graph_lib.compute_complexity import GenomeGraph
from gene_graph_lib.pattern_searching import count_patten_in_gen_for_each, GarlicPattern, find_spyder, find_transposition
from parser.graphbuilder import Graph


parser = argparse.ArgumentParser()
parser.add_argument('--template', type=str, default=None, help='template (for example "\'1\'>\'2\'>\'3\'"]')
parser.add_argument('--graph', type=str, default=None, help='sif file with graph structure')
parser.add_argument('--type', type=str, default=None, help='optimized pattern name')
parser.add_argument('-o', default='out.txt', type=str, help='output file')
args = parser.parse_args()

g = GenomeGraph()
g.read_graph(args.graph)

template = Graph.parse(args.template)

if args.type == None:
    hits = find_template(template, g)

elif args.type == 'spider':
    hits = find_spyder(template, g)

elif args.type == 'penguin':
    hits = find_transposition(template, g)

elif args.type == 'spider':
    garlic = GarlicPattern()
    hits = count_patten_in_gen_for_each(g.list_graph, garlic)
else:
    print('invalid pattern type')

print()
print('----RESULTS----')
print()

for i in hits:
    print(i)

print('----------')
f = open(args.o, 'w')
for h in hits:
    f.write(str(h))

f.close()
print('Done!')