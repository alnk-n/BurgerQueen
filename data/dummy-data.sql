PRAGMA foreign_keys = ON;

-- usernames, passwords and employee status
INSERT INTO Users (Username, Password, IsEmployee)
VALUES
('Geralt', 'hesterbest', 0),
('Yennefer', 'qwerty', 0),
('Roach', 'pizza', 0),
('Jaskier', 'nyttpassord', 1),
('u', 'user', 0),
('a', 'admin', 1);

-- burger id and names
INSERT INTO Burgers (Name)
VALUES
('Whopper Queen'),
('Triple Cheesy Princess'),
('Kingdom Fries');

-- ingredient id, name and stock
INSERT INTO Ingredients (IngredientName, AmountInStock)
VALUES
('Burgerbrød topp og bunn', 9001),
('Burgerkjøtt', 10),
('Salat', 8008),
('Tomat', 1337),
('Ost', 42),
('Agurk', 666),
('Potet', 420);

-- foreign burger id and ingredient id, and amount of each
INSERT INTO BurgerRecipes (BurgerID, IngredientID, Quantity)
VALUES
(1, 1, 2),
(1, 2, 1),
(1, 3, 1),
(1, 4, 1),
(2, 1, 2),
(2, 2, 3),
(2, 3, 2),
(2, 4, 1),
(2, 5, 1),
(1, 6, 1);

-- foreign user id and burger id, and status
INSERT INTO Orders (OrderID, UserID, BurgerID, IsDone)
VALUES
(1, 1, 1, 1),
(1, 1, 1, 0),
(2, 4, 2, 0),
(3, 3, 1, 0);