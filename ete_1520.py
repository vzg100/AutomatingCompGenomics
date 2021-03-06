import pandas as pd
import numpy as np
from ete3 import Tree, faces, AttrFace, TreeStyle, NodeStyle, NCBITaxa, random_color, TextFace, CircleFace, RectFace
import random

# Read the file and assign it the variable df as a dataframe
df = pd.read_csv("/Users/mark/Downloads/PATRIC_genome-5.csv", dtype={'Genome ID': str})

#Create an object and assign it to the variable 
ncbi = NCBITaxa()


#Dataframes are cool becuase becuase you can take a spreadsheet and slice out a whole column - trust me this is super useful 
ids = set(df["NCBI Taxon ID"]) #use set to remove duplicates

#Strains
patric_id = list(df["Genome ID"])
strain_name = list(df["Genome Name"])
#Extract the tree
tree = ncbi.get_topology(ids, intermediate_nodes=True)
tree.get_ascii(attributes=["sci_name"])


lineages = {}
for i in tree.traverse():
    if len(i.named_lineage) > 5:
        if i.named_lineage[4] in lineages.keys():
            lineages[i.named_lineage[4]].append(i.name)
        else:
            lineages[i.named_lineage[4]] = [i.name]


node_groups = {}
lineage_colors = {"Firmicutes":"Aquamarine", "Bacteroidetes/Chlorobi group":"LightCyan", "delta/epsilon subdivisions":"LightPink", 
"Gammaproteobacteria":"Gold",  "Fusobacteriia":"Violet", "Actinobacteria":"MistyRose", "Betaproteobacteria":"Gainsboro"}

for j in lineages.keys():
    node_groups[j] = tree.get_common_ancestor(lineages[j])
    temp_nest = NodeStyle()
    temp_nest["bgcolor"] = lineage_colors[j]
    node_groups[j].set_style(temp_nest)

for position, i in enumerate(patric_id):
    node = tree.search_nodes(name=i.split(".")[0])[0]
    node.add_child(name=i)
    for j in tree.search_nodes(name=i):
        j.add_features(label="sci_name")
        j.sci_name = strain_name[position]



def layout(node):
    if node.is_leaf():
        N = AttrFace("sci_name", fsize=30)
        faces.add_face_to_node(N, node, 0, position="branch-right")
        circle =  RectFace(100, 100, "black","black")

        #faces.add_face_to_node(circle, position="aligned", column=0, node=node)

        if "coli" in node.sci_name:
                circle = RectFace(100, 100, "red","red")
                faces.add_face_to_node(circle, position="aligned", column=1, node=node)
        if "Salm" in node.sci_name:
            circle =  RectFace(100, 100, "blue","blue")
            faces.add_face_to_node(circle, position="aligned", column=2, node=node)




ts = TreeStyle()
ts.branch_vertical_margin = 10
ts.allow_face_overlap = False
ts.show_scale = False
ts.show_leaf_name = False
ts.layout_fn = layout
ts.mode = "c"
ts.root_opening_factor = .25
ts.optimal_scale_level = "full"
ts.force_topology = True
for i, j in enumerate(lineage_colors.keys()):
    ts.legend.add_face(RectFace(10000, 300, lineage_colors[j], lineage_colors[j]), column=i)
    ts.legend.add_face(TextFace(j, fsize=600), column=i)
tree.show(tree_style=ts)

