# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 11:47:38 2020

@author: Nolan K Newman <newmanno@oregonstate.edu>
"""

# import the io and networkx module
import argparse
import csv
from collections import Counter
from math import factorial

# Create a dictionary function to easily add keys and values to dictionary
class dictionary(dict):
    def __init__(self):
        self = dict()
        
    # Add key/value pair
    def add(self, key, value):
        self[key] = value

corr_dict = dictionary()
fc = {}

parser = argparse.ArgumentParser(description='Example: python dev_from_expected --input <network file> --num_groups <number of groups> \n\n See README.md for more info\n\n')
parser.add_argument("--input", help = 'Network file (see README.md for example)')
parser.add_argument("--num_groups", help = 'Number of groups correlations were initially performed in')

args = parser.parse_args()

if (args.input != '') and (args.num_groups != ''):
    net_file = args.input
    net_file_trimmed = net_file[:-4] # trim the ".csv" or ".txt" from the input file string   
    groups = int(args.num_groups)
else:
    raise Exception("Error: please provide both a network file and the number of groups correlations were performed in. See --help for more information.")

# Counters for puc calculation
puc_compliant = 0
puc_noncompliant = 0

# import specified file into python
with open(net_file) as csvfile:
    file = csv.reader(csvfile, delimiter = ',')
    for row in file:

        # Check if there are any NAs in the correlation column and if not then add the edge to the dictionary
        # The keys are nodes that make up the edge and values are a list of parameters (pval, comb pval, rho, etc.)        
        if row[12] != 'NA':
            nodes = row[1:3]
            list_to_tuple = tuple(nodes)
            corr_dict.add(list_to_tuple,row[3:len(row)])
        
            fc_node1_column = 11 + groups
            fc_node2_column = 12 + groups
            
            # Find FC direction of each node
            fc[row[1]] = row[fc_node1_column].strip()
            fc[row[2]] = row[fc_node2_column].strip()
            
            # Is each edge PUC-compliant?
            puc_col = 14 + groups
        
            if row[puc_col].strip() == str(1):
                puc_compliant += 1
            elif row[puc_col].strip() == str(-1):
                puc_noncompliant += 1
                     
        else:
            print("An NA was found for a correlation. Continuing anyways but omitting this correlation.")

    csvfile.close()  
 
# This removes the header of the data frame essentially
del corr_dict['partner1', 'partner2']         
del fc['partner2']
del fc['partner1']

# Get a dictionary of all correlation directions and count all positive and negative edges in observed network
pos_corr = 0 # counter for the number of positive edges
neg_corr = 0 # counter for the number of positive edges
rho_column = 7 + groups
for key,value in corr_dict.items():
    try:    
        if str(value[rho_column].strip()) == '1':
            pos_corr += 1
        elif str(value[rho_column].strip()) == '-1':
            neg_corr += 1
    except:
        print("ERROR: an incorrect value was supplied for correlation directions. Aborting.")         
     
nedges = pos_corr + neg_corr        
        
print("\nThere are " + str(pos_corr) + " positive edges and " + str(neg_corr) + " negative edges for a total of " + str(nedges) + " edges.\n")

# Count the number of positive and negative nodes    
nodedir = Counter(fc.values())
pos_nodes = nodedir['1']
neg_nodes = nodedir['-1']  

total_nodes = int(pos_nodes) + int(neg_nodes)
print("\nThere are " + str(pos_nodes) + " positive nodes and " + str(neg_nodes) + " negative nodes for a total of " + str(total_nodes) + " nodes.\n")

obs_edge_node_ratio = nedges / total_nodes

obs_posneg_node_ratio = int(pos_nodes) / int(neg_nodes)
obs_negpos_node_ratio = int(neg_nodes) / int(pos_nodes)

# Find the ratio of positive:negative edges (and vice versa) in the observed graph
if int(neg_corr) != 0:
    obs_posneg_ratio = int(pos_corr)/int(neg_corr)
else:
    obs_posneg_ratio = 1.0
    
if int(pos_corr) != 0:
    obs_negpos_ratio = int(neg_corr)/int(pos_corr)
else:
    obs_negpos_ratio = 1.0

# Find the number of edges in a full graph      
expec_pos = int(factorial(pos_nodes)/(2 * factorial(pos_nodes - 2)) + factorial(neg_nodes)/(2 * factorial(neg_nodes - 2)))           
expec_neg = pos_nodes * neg_nodes
expec_total = expec_pos + expec_neg          
expec_edge_node_ratio = expec_total / total_nodes

# Find the ratio of positive:negative edges (and vice versa) in a full graph
ideal_ratio_posneg = expec_pos/expec_neg
ideal_ratio_negpos = expec_neg/expec_pos
           
#Calculate the non-normalized deviation from the expected (full) graph
dev_posneg = obs_posneg_ratio/ideal_ratio_posneg
dev_negpos = obs_negpos_ratio/ideal_ratio_negpos
                      
#Calculate the normalized deviation from the expected (full) graph
dev_norm_posneg = (obs_posneg_ratio - ideal_ratio_posneg) / ideal_ratio_posneg
dev_norm_negpos = (obs_negpos_ratio - ideal_ratio_negpos) / ideal_ratio_negpos

# calculate the normalized deviation of the edge:node (density) from the full graph
dens_dev = (abs(obs_edge_node_ratio - expec_edge_node_ratio)) / expec_edge_node_ratio

# Calculate PUC (the proportion of edges that do not follow the expected direction)
puc = puc_noncompliant / nedges

with open("deviation_output.txt", "w") as file:
    file.write("Number of total nodes: " + str(total_nodes) + "\n")    
    file.write("Number of positive nodes: " + str(pos_nodes) + "\n")
    file.write("Number of negative nodes: " + str(neg_nodes) + "\n")
    file.write("Positive:negative node ratio: %.3f"  % obs_posneg_node_ratio + "\n")   
    file.write("Negative:positive node ratio: %.3f"  % obs_negpos_node_ratio + "\n") 
    file.write("Number of PUC-compliant edges: " + str(puc_compliant) + "\n")     
    file.write("Number of PUC-noncompliant edges: " + str(puc_noncompliant) + "\n")     
    file.write("PUC: " + str(puc) + "\n\n")     
  
    file.write("### OBSERVED values ###\n") 
    file.write("Observed number of total edges: " + str(nedges) + "\n")        
    file.write("Observed number of positive edges: " + str(pos_corr) + "\n")  
    file.write("Observed number of negative edges: " + str(neg_corr) + "\n")
    file.write("Observed density (edge:node ratio): " + str(obs_edge_node_ratio) + "\n")     
    file.write("Observed positive:negative edge ratio: %.3f" % obs_posneg_ratio + "\n")   
    file.write("Observed negative:positive edge ratio: %.3f" % obs_negpos_ratio + "\n\n")
    
    file.write("### EXPECTED values ###\n")   
    file.write("Full graph number of total edges: " + str(expec_total) + "\n")   
    file.write("Full graph number of positive edges: " + str(expec_pos) + "\n")
    file.write("Full graph number of negative edges: " + str(expec_neg) + "\n")   
    file.write("Full graph density (edge:node ratio): " + str(expec_edge_node_ratio) + "\n")       
    file.write("Full graph positive:negative edge ratio: %.3f" % ideal_ratio_posneg + "\n")
    file.write("Full graph negative:positive edge ratio: %.3f" % ideal_ratio_negpos + "\n\n")   
    
    file.write("### Departures from full graph ###\n")       
    file.write('Non-normalized positive:negative deviation from full graph ratio (observed ratio / full graph ratio): %.2f' % dev_posneg + "\n")
    file.write('Non-normalized negative:positive deviation from full graph ratio (observed ratio / full graph ratio): %.2f' % dev_negpos + "\n")
    file.write('Normalized positive:negative deviation from full graph ((observed ratio - full graph ratio) / full graph ratio): %.2f' % dev_norm_posneg + "\n")      
    file.write('Normalized negative:positive deviation from full graph ((observed ratio - full graph ratio) / full graph ratio): %.2f' % dev_norm_negpos + "\n")          
    file.write('Normalized density (edge:node ratio) deviation from full graph ((observed ratio - full graph ratio) / full graph ratio): %.5f' % dens_dev + "\n")            
            
            
