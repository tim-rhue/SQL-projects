/* sql-KhanAcademy-Data-dig spinoff: Food Delivery */

/*There are quite a few places to eat in Charlotte.  Below is a sample of delivery time + the customer satisfaction.  Complete the numbered objectives to figure out trends between minutes_to_delivery compare to customer_satisfaction.

Instructions: 
1. display the company names and minutes_to_delivery that received a 5 for their customer_satisfaction rating
2. display the company names and minutes_to_delivery that received <= 4 for their customer_satisfaction rating
3. convert the customer_satisfaction numerical rating to a text form using the convention: Great = 5, Good = 4, OK = 3, Needs Improvement = 2, using word_rating. Display the company name, and word_rating using Group By.
*/

CREATE TABLE deliveries (
    id INTEGER PRIMARY KEY AUTOINCREMENT ID,
    company TEXT,
    minutes_to_delivery INTEGER,
    customer_satisfaction_rating INTEGER);
    
INSERT INTO deliveries (company, minutes_to_delivery, customer_satisfaction_rating)
    VALUES ("Jimmy Johns", 16, 5);
INSERT INTO deliveries (company, minutes_to_delivery, customer_satisfaction_rating)
    VALUES ("Viva Chicken", 29, 4);
INSERT INTO deliveries (company, minutes_to_delivery, customer_satisfaction_rating)
    VALUES ("PDQ", 30, 3);    
INSERT INTO deliveries (company, minutes_to_delivery, customer_satisfaction_rating)
    VALUES ("Toyama", 19, 5);
INSERT INTO deliveries (company, minutes_to_delivery, customer_satisfaction_rating)
    VALUES ("Zoe's Kitchen", 35, 3);
INSERT INTO deliveries (company, minutes_to_delivery, customer_satisfaction_rating)
    VALUES ("Pizza Hut", 45, 2);
INSERT INTO deliveries (company, minutes_to_delivery, customer_satisfaction_rating)
    VALUES ("Cook Out", 39, 3);
INSERT INTO deliveries (company, minutes_to_delivery, customer_satisfaction_rating)
    VALUES ("Harris Teeter subs", 40, 2);
INSERT INTO deliveries (company, minutes_to_delivery, customer_satisfaction_rating)
    VALUES ("Chili's", 35, 3);
INSERT INTO deliveries (company, minutes_to_delivery, customer_satisfaction_rating)
    VALUES ("Chick-fila", 18, 5);
INSERT INTO deliveries (company, minutes_to_delivery, customer_satisfaction_rating)
    VALUES ("Chipotle", 24, 4);
INSERT INTO deliveries (company, minutes_to_delivery, customer_satisfaction_rating)
    VALUES ("Subway", 34, 3);
INSERT INTO deliveries (company, minutes_to_delivery, customer_satisfaction_rating)
    VALUES ("Sugar Shack", 22, 4);

/*1*/
Select company, minutes_to_delivery from deliveries where customer_satisfaction_rating = "5";

/*2*/
Select company, minutes_to_delivery from deliveries where customer_satisfaction_rating <= "4";

/*3*/
Select company, 
    Case
        When minutes_to_delivery < 20 Then "Great"
        When minutes_to_delivery >= 20 Then "Good"
        When minutes_to_delivery >= 30 Then "OK"
        Else "Needs Improvement"
    End as word_rating
from deliveries 
Group by company;
