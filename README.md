For more details about this project check this:

https://paper.dropbox.com/doc/Fox-Congress-Speeches-Project-Data-processing-steps--ASXG0_RyBSkJ0uzEqU4c8EuOAQ-31iE4L6CD4jkmMFH1myZT

the code to run the script on the cluster: 

bsub -W 900 -R "rusage[mem=20480]" python make_matrices_CNN_transcript_library_based.py

Works to be done (from Elliott): 

1) Match congressmen to districts #2

The ID's (file names) in the segmented speeches data contain the state, the last name, and the starting year for the congressman. This is sufficient to uniquely identify them -- it then needs to be matched with the associated district number.

Note that the districts changed in 2000 and 2010 due to redistricting.

2) Match districts to zip codes #3

The fox news news channel positions and 2005-2008 ratings data are at the zip code level.

Therefore the districts need to be matched to zip codes.

This needs to be updated over time as redistricting (in 2000 and 2010) changes the districts.

3) Aggregate fox news channel positions by district #4

The channel positions are by zip code -- they need to be aggregated to the congressional district level.

That should be done using the population-weighted average by zip code.

This dataset can be used for this purpose:
https://www.dropbox.com/s/fjpi2uwyvu1axlc/zip_code_data.dta?dl=0

4) Compute n-gram frequencies by year for transcripts and speakers #5

We will have a vector of frequencies for each cable station, and each congressional member, for each year.

this can be done 2005-2008 first.

The baseline specification should use tf-idf weights.

5) Compute similarities for each congressman to each news station #6

Compute cosine similarity of each congressman vector to each news station vector.
This can only be done after #5

6) Run first stage regression #7
This requires:

X, endogenous regressor: fox news ratings at congressional district level, from #4
Z, instrument: fox news channel position at congressional district level, from #4

Then regress

X = alpha + gamma * Z

to get first stage estimate gamma

7) Run reduced form regression #8

This requires:

Y, outcome: similarity of congressman speech in district i at time t, to fox news transcript at time t
Z, instrument: fox news channel position at congressional district level, from #4

Then regress

Y = alpha + rho * Z

to get reduced form estimate rho

8) Run 2SLS regression #9
This requires:

Y, outcome: similarity of congressman speech in district i at time t, to fox news transcript at time t, from #6
X, endogenous regressor: fox news ratings at congressional district level, from #4
Z, instrument: fox news channel position at congressional district level, from #4

Then regress (in stata)




















