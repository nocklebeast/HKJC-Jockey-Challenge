# HKJC-Jockey-Challenge
Estimating odds for HKJC's Jockey Challenge and the Trainer Challenge

In the HKJC's Jockey Challenge, best performing jockeys are assigned points for each win, place, or show (1st, 2nd, or 3rd place). The jockey with the most points wins the challenge, and the HKJC accepts bets on the outcome in Hong Kong.

Uses a simple model for predicting trifecta winners for each race of the day, based on public odds on HKJC's website. Then estimates the expected points and odds of winning the jockey challenge using a Monte Carlo simulation.

The calculation may be peformed before the first race and in between races (just like you can bet during those times as well... if you're in Hong Kong).  The Trainer Challenge is only played before the first race of the day.

Known issues/room for improvement:

• While the program does consider the number of 1st/2nd/3rd places when breaking ties for simulated races, it fails to consider them for previous (actual) races after the first race.

• The program should be using a superfecta (quartet) model instead of a trifecta (tierce) model in order to break ties with the number of 4th place finishes.  But I think these tie breakers are fairly rare (maybe 1% of jockey challenges), so maybe not worth the effort.

• As always, a more accurate trifecta model would result in a more predictive Monte Carlo simulation.  May include an option for reading in an alternative trifecta chance file in the future.

Sample output:

(potential value plays are highlighted in green in the odds table.)

![tnc_points](https://user-images.githubusercontent.com/69921853/195210291-7a8d91ae-cdb8-46ee-a823-7627f2eb6da5.jpg)

![tnc_odds](https://user-images.githubusercontent.com/69921853/195210306-4b8b3d49-02ed-44e3-8ae7-a8594c6ead1b.jpg)


See order of python files.txt for notes on running the scripts.
