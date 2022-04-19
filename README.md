# CA-BNE


This is a piece of software used for measure the performance of different reference point rules.

Before the performance can be measured, the Bayes-Nash Equilibria need to be computed. This can be with the help of the following paper:
**Computing Bayes-Nash Equilibria in Combinatorial Auctions with Continuous Value and Action Spaces**  
Vitor Bosshard, Benedikt Bünz, Benjamin Lubin, and Sven Seuken. In Proceedings of the 26th International Joint Conference on Artificial Intelligence (IJCAI), Melbourne, Australia, August 2017. [[pdf](http://www.ifi.uzh.ch/ce/publications/BNE_Bosshard_et_al_IJCAI_2017-long.pdf)]

The computed BNE strategies need to be added as .txt files to strategyText.
All the settings examined in my Thesis are already present. They can be visualized using the visualizations.py script in folder strategyText.

To measure the performance of the payment rules, the main.py script needs to be run.
It currently measures the performance of the payment rules in standard LLG and standard L3G.
To measure the performance in different settings, the value ranges, the correlation and the path to the BNE strategies need to be adjusted.

To measure the correlation between different performance metric, also main.py script needs to be run.
It currently measures the correlation between LM at truth and all other performance metrics in the same settings as in the Thesis.
To compute the correlation between different performance metrics, either the "metric" variable needs to be adjusted or the "metric1" and "metric2" variables need to be adjusted










