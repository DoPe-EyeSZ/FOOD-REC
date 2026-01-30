delete this later:
challenges:
1. figuring out how to use google places api
2. dk how to feature encode (cuisine type)
   - idk how to assign numeric value to chinese food and differentiate that w french food
   - idk what to do if api doesnt provide sufficient data to assign cuisine to a resturant
4. lack of data causing ambiguity (restaurants dont have specific cuisine data so it becomes unkonwn which cuisine something is)
5. accuracy was -1.43
   - i used a linear regression when logistic regression was best
   - data was inconsisent (didnt have a way to store data)

   --> now accuracy is 0.7166666666666667
         - using logistic regression
         - scaled data so drivetime/rating are within reasonable range
         - store data now

current issues (1/23/26)
* abiguity to data
   - some restaurants dont have cuisine labels so they are classified as "restaurants"
   - chinese restaurts can be seen more so can lead to smaller acceptance ratio than french restaurnt that is seen less often    (chiense 50/55 vs. french 2/2    french>chinese)

   SOLUTION: use AI api to auto classify (if finaically feasible)

* lack of feature data
   - users tend to pick restaurnts based off pictures --> hard encode pictures
   - only collected 300 data points, the more the better
   - lowk rushed the decision making process (had to iterate 300 restaurnts so prolly a little tired)

* using logistsc regression
   - fits use case, but maybe better model like random forrest????
      - random forrest good for complex relationships with features (rating, rating count, drive time)



update (1/23/26)
- random forrest has better accuracy of 0.7666666666666667


update (1/26/26)
- accuracy is now 0.79 after adding 200 more data sets
- gonna use cross validation to test model accuracy so i dont gotta split data manually
- cross validation results: [0.76 0.8  0.76 0.79 0.84]
   - model is accurate and consistent for the most part across 5 different test sets


update (1/27/26)
- reverted back to logistic regression bc model did 20% better in training vs testing (overfitting)
- accuracy is not 76 percent after reverting back to logistic
- performed feature importance (everything accurate except drive time but i didnt look at drive time)
   - importance will correct itself

- real world simulation proves to be tough
- most of function saves data to sql db
   - but simulation doesn not require that so i had to comment out a lot of stuff
- data collection phase was tailored for training so i had to provide my response
   - had to create function that collects feature data without response bc i cannot use join function

- had to refactor api function
   - api data extraction function was made specifically for testing initially so it prompts user for their input
   - was not beneficial for real world simulation since i did not need to provide input, but just make prediction with
   raw data
   - removed all input and database collect to the collect data file so data collection makes sense
   - now api function data extract function only returns filtered data

- established real world simulation
   - was 75 percent accurate so fit the model's score

- sort the prediction probablity from highest to lowest
- select top 5 + random 5 for exploration purposes


update (1/28/26)
- began implementing into flask
- creating pipeline function
- save model and scalar to to ML folder through pickle
   - idrk how to use pickle

update (1/29/26)
- more implementation to flask
- adding reponse handling
- error arised from passing dictionary to url which caused crashing
- established basic data transfer across routes

update (1/30/26)
- simplify training file
   - added training function



skills:
- cross validation to test model accuracy
- data scaling to allow feature data to be within a reasonable range
- encoded feature data
- stored data into a sqlite db for testing
- trained/test model on 500 data sets



v2 ideas:
- show image of restaurant
- show description of restaurant
- show predicted probability