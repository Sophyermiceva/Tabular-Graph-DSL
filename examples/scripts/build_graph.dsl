LOAD users;
LOAD orders;

NODE User KEY id FROM users;

NODE Product KEY product_id FROM orders;

EDGE Bought
    FROM orders
    SOURCE user_id
    TARGET product_id
    WEIGHT amount
    WHERE (amount > 5) AND (amount < 10);
