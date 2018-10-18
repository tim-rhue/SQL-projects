/* Use ALTER to add a 'price' column to the table. Then select all the columns in each row to see what your table looks like now. */

CREATE TABLE clothes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    design TEXT);
    
INSERT INTO clothes (type, design)
    VALUES ("dress", "pink polka dots");
INSERT INTO clothes (type, design)
    VALUES ("pants", "rainbow tie-dye");
INSERT INTO clothes (type, design)
    VALUES ("blazer", "black sequin");

Alter Table clothes ADD Price Integer; 

Select * from clothes;

/* Now assign each item a price, using UPDATE - item 1 should be 10 dollars, item 2 should be 20 dollars, item 3 should be 30 dollars. When you're done, do another SELECT of all the rows to check that it worked as expected. */

Update clothes Set Price = 10 where id = 1;
Update clothes Set Price = 20 where id = 2;
Update clothes Set Price = 30 where id = 3;

Select * from clothes; 

/* Now insert a new item into the table that has all three attributes filled in, including 'price'. Do one final SELECT of all the rows to check it worked. */

Insert INTO clothes (type, design, price)
    VALUES ("hat","top hat",15);

Select * from clothes; 