For more details about this project check this:

https://paper.dropbox.com/doc/Fox-Congress-Speeches-Project-Data-processing-steps--ASXG0_RyBSkJ0uzEqU4c8EuOAQ-31iE4L6CD4jkmMFH1myZT

the code to run the script on the cluster: 

bsub -W 900 -R "rusage[mem=20480]" python make_matrices_CNN_transcript_library_based.py


