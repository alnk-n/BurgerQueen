def updateInventory(con, cursor, order):
    items = order.split(',') if order else []

    for item in items:
        item = item.strip()
        
        cursor.execute("SELECT BurgerID FROM Burgers WHERE Name = ?", (item,))
        burger = cursor.fetchone()
        if not burger:
            print(f'Burger "{item}" not found.')
            continue

        burgerID = burger[0]
        cursor.execute("SELECT IngredientID, Quantity FROM BurgerRecipes WHERE BurgerID = ?", (burgerID,))
        ingredients = cursor.fetchall()

        # subtract ingredients from stock
        for ingredientID, amount in ingredients:
            cursor.execute("UPDATE Ingredients SET AmountInStock = AmountInStock - ? WHERE IngredientID = ?", (amount, ingredientID))

    con.commit()

def viewInventory(con, cursor, username):
    pass