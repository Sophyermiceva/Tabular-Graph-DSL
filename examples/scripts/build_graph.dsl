# Example DSL script: build a user-product purchase graph.
#
# Data files expected in ../data/

LOAD users;
LOAD orders;

NODE User KEY id FROM users;

NODE Product KEY product_id FROM orders;

EDGE Bought
    FROM orders
    SOURCE user_id
    TARGET product_id
    WEIGHT amount;
