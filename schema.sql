-- Note for the following
-- if the name is different, it may interfere with PSQL syntax
-- Requires Foreign Keys added and Relationships

-- Entities
CREATE TABLE Item (
    itemID SERIAL PRIMARY KEY,
    itemName CHAR(255) NOT NULL,
    category CHAR(255) NOT NULL,
    startingPrice INTEGER NOT NULL,
    imageURL CHAR(255),
    condition CHAR(50),
    itemDescription CHAR(255),
    -- Relationships below --
    -- Item is listed in Auction
    FOREIGN KEY (auctionID) REFERENCES Auction(auctionID)
    -- User Manages Item, constraint role = Seller
);

CREATE TABLE Shipment (
    ShipmentID SERIAL PRIMARY KEY,
    shipmentAddress CHAR(255) NOT NULL, 
    shipmentStatus CHAR(255) NOT NULL,
    trackingNumber INTEGER,
    -- Relationships below --
    -- Shipment is for Auction
    FOREIGN KEY (auctionID) REFERENCES Auction(auctionID)
);

CREATE TABLE Payment(
    paymentID SERIAL PRIMARY KEY,
    amount INTEGER NOT NULL,
    paymentStatus CHAR(255) NOT NULL
);

CREATE TABLE User (
    userLogin SERIAL PRIMARY KEY,
    phoneNum INTEGER NOT NULL,
    userPassword CHAR(255) NOT NULL,
    userRole CHAR(255) NOT NULL,
    userAddress CHAR(255) NOT NULL,
    favoriteCategory CHAR(255),

    -- Relationships below --
    -- User Manages Item, TODO: constraint role = Seller
    FOREIGN KEY (managedItemID) REFERENCES Item(itemID),
    -- User makes Payment
    FOREIGN KEY (paymentID) REFERENCES Payment(paymentID),
    -- User Wins Auction
    FOREIGN KEY (winningAuctionID) REFERENCES Auction(auctionID),
    -- User Create Auction
    FOREIGN KEY (createdAuctionID) REFERENCES Auction(auctionID),
    -- User places Bids
    FOREIGN KEY (bidID) REFERENCES Bid(bidID)
);

CREATE TABLE Bid (
    bidID SERIAL PRIMARY KEY,
    bidAmount INTEGER NOT NULL,
    bidTimestamp TIMESTAMP NOT NULL,
    -- Relationships below --
    -- Auction receives Bids
    FOREIGN KEY (auctionID) REFERENCES Auction(auctionID),
    -- User places Bid
    FOREIGN KEY (userLogin) REFERENCES User(userLogin)
);

CREATE TABLE Auction(
    auctionID SERIAL PRIMARY KEY,
    auctionStatus CHAR(255) NOT NULL,
    currentHighestBid INTEGER NOT NULL,

    -- Relationships below --
    -- Auction has shipment
    FOREIGN KEY (shipmentID) REFERENCES Shipment(ShipmentID),
    -- Item listed in Auction
    FOREIGN KEY (itemID) REFERENCES Item(itemID),
    -- Auction has payment
    FOREIGN KEY (paymentID) REFERENCES Payment(paymentID),
    -- User Wins Auction
    FOREIGN KEY (winningUserLogin) REFERENCES User(userLogin),
    -- User Creates Auction
    FOREIGN KEY (creatorUserLogin) REFERENCES User(userLogin),
    -- Auction receives Bids
    FOREIGN KEY (auctionID) REFERENCES Bid(auctionID)
);