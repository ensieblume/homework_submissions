-- 1a. You need a list of all the actors who have Display the first and last names of all actors from the table actor. 
USE sakila;

SELECT *
FROM actor
LIMIT 5;

SELECT first_name, last_name
FROM actor
LIMIT 5;

-- 1b. Display the first and last name of each actor in a single column in upper case letters. Name the column Actor Name.  
SELECT CONCAT(first_name, ',', last_name) AS 'Actor Name'
FROM actor
LIMIT 5;

-- 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." 
-- What is one query would you use to obtain this information?
SELECT actor_id, first_name, last_name
FROM actor
WHERE first_name = 'Joe';

-- 2b. Find all actors whose last name contain the letters GEN:
SELECT first_name, last_name
FROM actor
WHERE last_name LIKE '%GEN%';

-- 2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order:
SELECT last_name, first_name
FROM actor
WHERE last_name LIKE '%lI%';


SELECT *
FROM country
LIMIT 5;

-- 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:
SELECT country_id, country
FROM country
WHERE country IN ('Afghanistan', 'Bangladesh', 'China');

-- 3a. Add a middle_name column to the table actor. Position it between first_name and last_name.
-- Hint: you will need to specify the data type.
ALTER TABLE actor
ADD middle_name VARCHAR(255) NULL
AFTER first_name;

SELECT *
FROM actor
LIMIT 5;

-- 3b. You realize that some of these actors have tremendously long last names. Change the data type of the middle_name column to blobs.
ALTER TABLE actor
MODIFY COLUMN middle_name Blob;

SELECT *
FROM actor
LIMIT 5;

-- 3c. Now delete the middle_name column.
ALTER TABLE actor
DROP middle_name;

SELECT *
FROM actor
LIMIT 5;

-- 4a. List the last names of actors, as well as how many actors have that last name.
SELECT last_name,COUNT(*) AS number_of_actors
FROM actor
GROUP BY last_name;

-- 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors
SELECT last_name,COUNT(*)
FROM actor
GROUP BY last_name
HAVING COUNT(*) >= 2;

-- 4c. Oh, no! The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS,
-- the name of Harpo's second cousin's husband's yoga teacher. Write a query to fix the record.

SELECT actor_id, first_name, last_name
FROM actor
WHERE last_name =  "WILLIAMS";


UPDATE actor 
SET first_name = "HARPO"
WHERE first_name = "GROUCHO" AND last_name = "WILLIAMS";

UPDATE actor 
SET first_name = "HARPO"
WHERE first_name = "MUCHO GROUCHO" AND last_name = "WILLIAMS";


-- 4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct name after all!
-- In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO.
-- Otherwise, change the first name to MUCHO GROUCHO, as that is exactly what the actor will be with the grievous error.
-- BE CAREFUL NOT TO CHANGE THE FIRST NAME OF EVERY ACTOR TO MUCHO GROUCHO, HOWEVER! (Hint: update the record using a unique identifier.)

UPDATE actor 
	SET first_name = 
    
		CASE
			WHEN first_name = 'HARPO'
				THEN 'GROUCHO'
			ELSE 'MUCHO GROUCHO'
			
		END
	WHERE last_name = 'WILLIAMS';    
    
-- verify the result
SELECT actor_id, first_name, last_name
FROM actor
WHERE last_name =  "WILLIAMS";


-- 5a. You cannot locate the schema of the address table. Which query would you use to re-create it?
SHOW CREATE TABLE address;

-- 'CREATE TABLE `address` \n  `address_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,\n  `address` varchar(50) NOT NULL,\n 
-- `address2` varchar(50) DEFAULT NULL,\n  `district` varchar(20) NOT NULL,\n  `city_id` smallint(5) unsigned NOT NULL,\n 
-- `postal_code` varchar(10) DEFAULT NULL,\n  `phone` varchar(20) NOT NULL,\n  `location` geometry NOT NULL,\n
--  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n  PRIMARY KEY (`address_id`),\n 
-- KEY `idx_fk_city_id` (`city_id`),\n  SPATIAL KEY `idx_location` (`location`),\n 
-- CONSTRAINT `fk_address_city` FOREIGN KEY (`city_id`) REFERENCES `city` (`city_id`) ON UPDATE CASCADE\n) ENGINE=InnoDB AUTO_INCREMENT=606 DEFAULT CHARSET=utf8'

DESCRIBE address;

-- 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address:
SELECT *
FROM staff
LIMIT 10;

SELECT *
FROM address
LIMIT 10;


SELECT
	staff.first_name,
    staff.last_name,
    address.address
FROM staff JOIN address USING(address_id);

-- 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment. 
SELECT *
FROM staff
LIMIT 10;

SELECT *
FROM payment
LIMIT 10;

-- staff1, $$$,
-- staff2, $$$

SELECT MONTH(payment_date)
FROM payment
LIMIT 10;

SELECT 
	staff.staff_id,
	staff.first_name,
    staff.last_name,
    SUM(payment.amount) as total_amount
FROM staff
JOIN payment on staff.staff_id = payment.staff_id
WHERE MONTH(payment.payment_date) = 8
AND YEAR(payment.payment_date) = 2005
GROUP BY  staff.staff_id, staff.first_name, staff.last_name;  --  alternatively we can use 1,2,3  :-);
    



-- 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join.
SELECT *
FROM film
LIMIT 100;

SELECT *
FROM film_actor
LIMIT 100;

SELECT 
    film_actor.film_id,
    COUNT(film_actor.actor_id) as 'nActors',
    film.title
FROM
    film_actor
		JOIN
    film ON film_actor.film_id = film.film_id  
GROUP BY film_actor.film_id;

-- 6d. How many copies of the film Hunchback Impossible exist in the inventory system?
SELECT *
FROM inventory
LIMIT 10;

SELECT *
FROM film
LIMIT 100;

SELECT 
	film.title,
    inventory.film_id,
    inventory.store_id,
    inventory.inventory_id
FROM film
JOIN inventory on film.film_id = inventory.film_id
WHERE title = 'HUNCHBACK IMPOSSIBLE';


-- 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. List the customers alphabetically by last name:
SELECT *
FROM payment
LIMIT 10;

SELECT *
FROM customer
LIMIT 10;

SELECT  
    customer.customer_id,
    customer.first_name,
    customer.last_name,
    SUM(payment.amount) AS total_paid
FROM payment
JOIN customer on payment.customer_id = customer.customer_id
GROUP BY customer.customer_id, customer.first_name, customer.last_name
ORDER BY customer.last_name, customer.first_name;


