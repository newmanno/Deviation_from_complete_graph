# Deviation_from_complete_graph
 Author: Nolan K Newman <newmanno@oregonstate.edu>
 Date: 7/27/20
 Created with Python v3.5.1
 
 Purpose:
 Calculate how the observed network deviates from an ideal, complete graph that contains all expected correlations.

 Description: This file takes as input a network file (format below) and will calculate all edge:node ratios (AKA "density"), PUC-compliant edges, and how the network deviates from a complete graph (i.e. all nodes connect to all other nodes) with the same number of nodes. **As of right now, the structure of the network file it takes in is specific as it is the output of a previous file in a pipeline**
 
 Dependencies: none (all from base Python)
 
 Example command:
	python dev_from_expected.py --input path/to/network/file --num_groups <number of groups>
	
 Arguments:
	Required: 
		--input  -  network file of correlations between parameters, including directions of correlations, fold changes, and whether the edge is PUC-compliant
		--num_groups  -  number of groups that correlations were originally calculated in. For example, if you calculated correlations in two different groups, WD and ND, then your argument would be "--num_groups 2"
		
	Optional:
		None at this time
		
 Example input network header:
	pair,partner1,partner2,pval_E1,pval_E2,comb_pval,comb_rho,comb_FDR,partner1InFold,partner1_FoldChange,partner2InFold,partner2_FoldChange,corr_direction,partner1_FC_direction,partner2_FC_direction,IfFoldChangeDirectionMatch,PUC
- pair: gene1 <==> gene2
- partner1: gene1
- partner2: gene2
- pval_E1: correlation pvalue in experiment 1
- pval_E2: correlation pvalue in Experiment 2
- comb_pval: Fisher's combined pvalue across both experiments
- comb_rho: combined rho coefficient across both experiments
- comb_FDR: FDR calculated off the combined pvalue
- partner1InFold: gene1
- partner1_FoldChange: Fold change of gene1
- partner2InFold: gene2
- partner2_FoldChange: Fold change of gene2
- corr_direction: correlation direction (either -1 or 1)
- partner1_FC_direction: Fold change direction of gene1 (either -1 or 1)
- partner2_FC_direction: Fold change direction of gene2 (either -1 or 1)    
- IfFoldChangeDirectionMatch: Are the previous 2 values identical (1 if yes, -1 if no)
- PUC: Is the correlation PUC-compliant (are neg-neg or pos-pos correlations +ve and pos-neg correlations -ve?)
			
 Output:
	Outputs a text file with each calculated parameter and its value. Values are rounded to 3 decimal places.
	
 Notes:
	Will not work with a network that contains 0 negative edges, since you must divide the number of positive edges by the number of negative edges. Networks without negative edges are likely erroneous, anyways.






	
