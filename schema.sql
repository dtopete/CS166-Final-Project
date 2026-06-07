-- Auction app schema for the client application.

DROP TABLE IF EXISTS Bid CASCADE;
DROP TABLE IF EXISTS Shipment CASCADE;
DROP TABLE IF EXISTS Payment CASCADE;
DROP TABLE IF EXISTS Auction CASCADE;
DROP TABLE IF EXISTS Item CASCADE;
DROP TABLE IF EXISTS "User" CASCADE;

CREATE TYPE user_role AS ENUM ('Seller', 'Buyer', 'Admin');
CREATE TYPE item_condition AS ENUM ('available', 'sold', 'removed');
CREATE TYPE a_status AS ENUM ('active', 'closed', 'cancelled');
CREATE TYPE p_status AS ENUM ('pending', 'completed', 'failed');
CREATE TYPE s_status AS ENUM ('pending', 'shipped', 'delivered');

CREATE TABLE "User" (
    login TEXT PRIMARY KEY,
    phoneNum CHAR(20),
    role user_role NOT NULL,
    password TEXT NOT NULL,
    address TEXT,
    favoriteCategory TEXT
);

CREATE TABLE Item (
    itemId CHAR(20) PRIMARY KEY,
    itemName TEXT NOT NULL,
    category TEXT,
    imageURL TEXT,
    condition item_condition NOT NULL,
    startingPrice FLOAT NOT NULL,
    description TEXT,
    sellerLogin TEXT NOT NULL REFERENCES "User"(login)
);

CREATE TABLE Auction (
    auctionId CHAR(30) PRIMARY KEY,
    auctionStatus a_status NOT NULL,
    currentHighestBid FLOAT NOT NULL,
    sellerLogin TEXT NOT NULL REFERENCES "User"(login),
    itemId CHAR(20) NOT NULL REFERENCES Item(itemId),
    buyerLogin TEXT REFERENCES "User"(login)
);

CREATE TABLE Payment (
    paymentId CHAR(30) PRIMARY KEY,
    amount FLOAT NOT NULL,
    paymentStatus p_status NOT NULL,
    buyerLogin TEXT NOT NULL REFERENCES "User"(login),
    auctionId CHAR(30) UNIQUE NOT NULL REFERENCES Auction(auctionId)
);

CREATE TABLE Shipment (
    shipmentId CHAR(30) PRIMARY KEY,
    address TEXT NOT NULL,
    shipmentStatus s_status NOT NULL,
    trackingNumber NUMERIC(10,0),
    auctionId CHAR(30) UNIQUE NOT NULL REFERENCES Auction(auctionId)
);

CREATE TABLE Bid (
    bidId CHAR(30) PRIMARY KEY,
    bidAmount FLOAT NOT NULL,
    bidTimestamp TIMESTAMP NOT NULL,
    buyerLogin TEXT NOT NULL REFERENCES "User"(login),
    auctionId CHAR(30) NOT NULL REFERENCES Auction(auctionId)
);
