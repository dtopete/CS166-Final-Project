-- Auction app schema with role-based business constraints.

-- Drop old objects when re-running this script.
DROP TABLE IF EXISTS Bid CASCADE;
DROP TABLE IF EXISTS Auction CASCADE;
DROP TABLE IF EXISTS Shipment CASCADE;
DROP TABLE IF EXISTS Item CASCADE;
DROP TABLE IF EXISTS Payment CASCADE;
DROP TABLE IF EXISTS "User" CASCADE;

CREATE TABLE "User" (
    userLogin SERIAL PRIMARY KEY,
    phoneNum BIGINT NOT NULL,
    userPassword VARCHAR(255) NOT NULL,
    userRole VARCHAR(20) NOT NULL,
    userAddress VARCHAR(255) NOT NULL,
    favoriteCategory VARCHAR(255),
    
    CONSTRAINT user_role_check CHECK (userRole IN ('Buyer', 'Seller', 'Admin')),

    CONSTRAINT user_login_role_uq UNIQUE (userLogin, userRole)
);

CREATE TABLE Payment (
    paymentID SERIAL PRIMARY KEY,
    amount INTEGER NOT NULL,
    paymentStatus VARCHAR(255) NOT NULL,
    payerUserLogin INTEGER NOT NULL,
    payerRole VARCHAR(20) DEFAULT 'Buyer' CHECK (payerRole = 'Buyer'),

    CONSTRAINT payment_user_fk
        FOREIGN KEY (payerUserLogin, payerRole) REFERENCES "User"(userLogin, userRole)
);

CREATE TABLE Item (
    itemID SERIAL PRIMARY KEY,
    itemName VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    startingPrice INTEGER NOT NULL,
    imageURL VARCHAR(255),
    condition VARCHAR(50),
    itemDescription VARCHAR(255),

    managerUserLogin INTEGER NOT NULL,
    managerRole VARCHAR(20) DEFAULT 'Seller' CHECK (managerRole = 'Seller'),

    CONSTRAINT item_manager_fk
        FOREIGN KEY (managerUserLogin, managerRole) REFERENCES "User"(userLogin, userRole)
);

CREATE TABLE Shipment (
    shipmentID SERIAL PRIMARY KEY,
    shipmentAddress VARCHAR(255) NOT NULL,
    shipmentStatus VARCHAR(255) NOT NULL,
    trackingNumber VARCHAR(100)
);

CREATE TABLE Auction (
    auctionID SERIAL PRIMARY KEY,
    auctionStatus VARCHAR(255) NOT NULL,
    currentHighestBid INTEGER NOT NULL,
    shipmentID INTEGER,
    itemID INTEGER NOT NULL,
    paymentID INTEGER,
    winningUserLogin INTEGER,

    creatorUserLogin INTEGER NOT NULL,
    CONSTRAINT auction_shipment_fk
        FOREIGN KEY (shipmentID) REFERENCES Shipment(shipmentID),
    CONSTRAINT auction_item_fk
        FOREIGN KEY (itemID) REFERENCES Item(itemID),
    CONSTRAINT auction_payment_fk 
        FOREIGN KEY (paymentID) REFERENCES Payment(paymentID),
    CONSTRAINT auction_winner_fk
        FOREIGN KEY (winningUserLogin) REFERENCES "User"(userLogin)
    -- Creator must be a seller
    CONSTRAINT auction_creator_fk
        FOREIGN KEY (creatorUserLogin, creatorRole) REFERENCES "User"(userLogin, userRole)
);

CREATE TABLE Bid (
    bidID SERIAL PRIMARY KEY,
    bidAmount INTEGER NOT NULL,
    bidTimestamp TIMESTAMP NOT NULL,
    auctionID INTEGER NOT NULL,

    userLogin INTEGER NOT NULL,
    userRole VARCHAR(20) DEFAULT 'Buyer' CHECK (userRole = 'Buyer'),

    CONSTRAINT bid_auction_fk
        FOREIGN KEY (auctionID) REFERENCES Auction(auctionID),
    -- Bidder must be a buyer
    CONSTRAINT bid_user_fk
        FOREIGN KEY (userLogin, userRole) REFERENCES "User"(userLogin, userRole)
);