import pandas as pd
import numpy as np
from ete3 import Tree, faces, AttrFace, TreeStyle, NodeStyle, NCBITaxa, random_color, TextFace, CircleFace, RectFace


# Read the file and assign it the variable df as a dataframe
df = pd.read_csv("/Users/mark/Downloads/PATRIC_genome.csv")

#Create an object and assign it to the variable 
ncbi = NCBITaxa()


#Dataframes are cool becuase becuase you can take a spreadsheet and slice out a whole column - trust me this is super useful 
ids = set(df["NCBI Taxon ID"]) #use set to remove duplicates

#Extract the tree
tree = ncbi.get_topology(ids, intermediate_nodes=True)
tree.get_ascii(attributes=["sci_name"])

lineages = {}
for i in tree.traverse():
    print(i)
    if len(i.named_lineage) > 5:
        if i.named_lineage[4] in lineages.keys():
            lineages[i.named_lineage[4]].append(i.name)
        else:
            lineages[i.named_lineage[4]] = [i.name]

node_groups = {}
import random
color_list = ["SkyBlue", "HotPink", "PeachPuff", "Gold", "DarkViolet", "Thistle", "Teal", "MediumAquamarine", "DeepskyBlue", 
"Brown", "Khaki", "Chocolate", "SaddleBrown", "DarkGrey", "Olive", "Violet"]
for i, j in enumerate(lineages.keys()):
    node_groups[j] = tree.get_common_ancestor(lineages[j])
    temp_nest = NodeStyle()


    temp_nest["bgcolor"] = color_list[i]
    node_groups[j].set_style(temp_nest)

def layout(node):
    if node.is_leaf():
        N = AttrFace("sci_name", fsize=30)
        faces.add_face_to_node(N, node, 0, position="branch-right")
        circle =  RectFace(100, 100, "black","black")

        faces.add_face_to_node(circle, position="aligned", column=0, node=node)
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
ts.root_opening_factor = 1


tree.show(tree_style=ts)

