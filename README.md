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

   --> now accuracy is 0.72
         - using logistic regression
         - scaled data so drivetime/rating are within reasonable range
         - store data now