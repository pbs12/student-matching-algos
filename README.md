# CS290 Algorithms Final Project

*This project is a collaboration between Matt Jogodnik, Vikram Ruppa-Kasani,  
Pranav Sharma, and Shubham Joshi and submitted as a final project for CS290  
Algorithms Fall 2020 taught by Dr. Brandon Fain.*

**Research Question: How can match-making algorithm(s) be applied to internship-student  
matching to centralize and declutter the process, as well as improve student outcomes?**

# In this directory:

## Gale-Shapley algorithm
The Gale–Shapley algorithm (also known as the deferred acceptance algorithm) is an algorithm for finding a solution to the stable matching problem, named for David Gale and Lloyd Shapley who had described it as solving both the college admission problem and the stable marriage problem. It takes polynomial time, and the time is linear in the size of the input to the algorithm. It is a truthful mechanism from the point of view of the proposing participants, for whom the solution will always be optimal. Herein, we developed code for the original algorithm, and modified to include *minority reserves* (read: affirmative action) as detailed in Hafalir, I. E., Yenmez, M. B., & Yildirim, M. A. (2013). Effective affirmative action in school choice. Theoretical Economics, 8(2), 325-363.

## Top Trading Cycle
Top trading cycle (TTC) is an algorithm for trading indivisible items without using money. It was also developed by David Gale and published by Herbert Scarf and Lloyd Shapley. It was extended to school matching (see Abdulkadiroğlu, Atila, and Tayfun Sönmez. "School choice: A mechanism design approach." American Economic Review 93, no. 3 (2003): 729-747). We developed a thorough comparison between TTC and Gale-Shapley in this codebase.

## other utilities
- Random data generation scripts for student records and collegiate admission critera for testing with the data
- A small implementation of the Boston Matching algorithm (to serve as a foil to Gale-Shapley)
