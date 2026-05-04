CREATE TABLE item (
    itemID SERIAL PRIMARY KEY,
    itemName CHAR(255) NOT NULL,
    category CHAR(255) NOT NULL,
    startingPrice INTEGER NOT NULL,
    -- Optional below
    imageURL CHAR(255),
    condition CHAR(50),
    itemDescription CHAR(255)

);