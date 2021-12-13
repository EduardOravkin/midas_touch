# Possible ideas to explore in MoneyBall

1. City is a categorical variable with a lot of caregories. Could instead "state" or area (according to some definition of area, e.g. west coast / east coast) help with performance?

2. Instead of One-Hot-Encoding investors create a variable "has_brand_name_investor" (get finite list of brand_name investors for this)

3. Instead of one-hot-encoding categories, create a variable called "is_tech?"

# Possible ideas to explore in Midas

Will work only if it is possible to get all (or nearly all) of the investments that each VC fund makes.

1. PageRank (the way google indexes search results https://en.wikipedia.org/wiki/PageRank) on VC funds. Important: "The underlying assumption is that better VC funds are likely to have more co-investments with other VC funds."

2. The score of a VC fund will be defined by the following pseudocode:

if vc_fund is in brand_name_vc_funds:
    score[vc_fund] = 1
else:
    scores[vc_fund] = average_score_of_coinvestments[vc_fund]
    scores[vc_fund] = (sum of scores[co_investement] for each co_investment of the vc_fund)/n_co_investment[vc_fund]

would compute the latter by an iterative algorithm. Would it converge? (all 1s is definitely a solution)

# Qs / summaries

Moneyball summary:

Successful companies: size of list sheet is 624, academic sheet is 505, work sheet is 573, Investor Sheet it 523. Intersection has 441 companies.

Unsuccessful companies: size of list sheet is 1637, academic sheet is 855, work sheet is 1354, Investor Sheet it 974. 

The number of features will be 8-12 (more likely 8). The succesful / unsuccessful sheets have the same features


Midas summary / qs:

1. Only around 7K of data even though in description it says 57K
2. Is there a finite-list of what are called brand investors?
3. Given a co-investor (e.g IDG Capital), do you have the number of their startups that none of the brand investors from the finite list (assuming answer to q.2 is yes), invested in their startup.

If the answer to 3. is yes, then 

Simple Model 1: I would model the relationship graph just by Strenth_i/(Total number of startups of co-investor). Modify this by influence of time somehow. 

Better Model 2: Time-series prediction problem. Example: Use prediction of Simple Model 1 until year 2020 as a prior for Better Model 2, and then predict the posterior of Better Model 2 by updating the prior based on an increase in the performance of the co-investor in the past year (e.g. number of unicorns produced or some type of financial data)

Discuss this with Yigit. If good then do Midas, if no good then do Moneyball.

note:Academic paper seems to be a bit ambitious (A good paper can take 1000 hours to write (mine took more)).
