
 
-- index auction_status. Buyers and the app constantly filter auctions by status. With this index, PostgreSQL jumps directly to the relevant rows.
CREATE INDEX idx_auction_status ON auction(auction_status);
 
-- index bid_auction_id
-- Every time we look up bids for an auction, we query by auction_id. Since auction_id is a foreign key, indexing it speeds up joins significantly.
CREATE INDEX idx_bid_auction_id ON bid(auction_id);
 
-- index item_category. Without this index, browsing by category scans the entire item table.
-- This index makes category filtering fast even with thousands of items.
CREATE INDEX idx_item_category ON item(category);
 
-- index bid_buyer_login Buyers frequently check their own bid history. Querying bids by buyer_login without an index scans all bids in the table.
CREATE INDEX idx_bid_buyer_login ON bid(buyer_login);
 
-- index payment_auction_id. After an auction closes, the system looks up payment status by auction_id.
-- Indexing this foreign key speeds up payment lookups and joins with auction.
CREATE INDEX idx_payment_auction_id ON payment(auction_id);
 
-- index shipment_auction_id. shipment is always looked up by auction_id after closing.
-- This index speeds up shipment tracking queries for both buyers and sellers.
CREATE INDEX idx_shipment_auction_id ON shipment(auction_id);
 
-- index auction_seller_login. Sellers frequently view all their own auctions.
CREATE INDEX idx_auction_seller_login ON auction(seller_login);
 
-- index bid_timestamp. Useful for sorting bids chronologically to find the most recent/highest bid.
CREATE INDEX idx_bid_timestamp ON bid(bid_timestamp);
 