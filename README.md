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