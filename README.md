# HKJC-Jockey-Challenge
Estimating odds for HKJC's Jockey Challenge and the Trainer Challenge

In the HKJC's Jockey Challenge, best performing jockeys are assigned points for each 1st, 2nd, or 3rd place finish for each race of the day. The jockey with the most points at the end of the day wins the challenge. The HKJC accepts bets on the outcome in Hong Kong.

Public odds on the HKJC's website are used to estimate the chance of any 3-horse permutation winning each race. Estimates of the expected points jockeys earn and chance of winning the overall jockey challenge are computed using a Monte Carlo simulation. 

The calculation may be peformed before the first race and in between races (just like you can bet during those times as well... if you're in Hong Kong).

Known issues/room for improvement:

• While the program does consider the number of 1st/2nd/3rd places when breaking ties for simulated races, it fails to consider them for previous (actual) races after the first race.

• The program should be using a superfecta (quartet) model instead of a trifecta (tierce) model in order to break ties with the number of 4th place finishes.  But I think these tie breakers are fairly rare (maybe 1% of jockey challenges), so maybe not worth the effort.

• As always, a more accurate trifecta model would result in a more predictive Monte Carlo simulation.  May include an option for reading in an alternative trifecta chance file in the future.

Sample output:

(potential value plays are highlighted in green in the odds table.)

![tnc_points](https://user-images.githubusercontent.com/69921853/195379590-09409d1a-3485-4869-a0de-556f9ea8bd5f.jpg)

![tnc_odds](https://user-images.githubusercontent.com/69921853/195379625-9c23f588-ac5a-4fa6-878d-e56274c06410.jpg)


See order of python files.txt for notes on running the scripts.
