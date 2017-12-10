# berlin_startup_jobs_analysis
Steps :
1. Data collection: 
    1.1 Stackoverflow parser
    1.2 Berlin Startup Jobs parser
    
2. Parse BSJ skills:

    a. Collect skills manually for every job position, organize data into json file and write individual skill parser;
    b. Group/Cluster skills :
    
    - Version 1: Group skills manually, write nltk modelling script to add skill-type/cluster/family as separate column;
    - Version 2: Cluster skills using Machine Learning K-means Clustering algorithm
    
3. Data vizualization using Tableau to answer questions about data
4. Website and story-writing 
