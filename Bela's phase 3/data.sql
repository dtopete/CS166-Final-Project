INSERT INTO users (login, password, phone_num, address, role, favorite_category) VALUES
('admin1',  'admin123', '555-000-0001', '1 Admin Blvd, Los Angeles, CA',    'Admin',  NULL),
('seller1', 'pass1234', '555-100-0001', '10 Seller St, San Francisco, CA',  'Seller', NULL),
('seller2', 'pass1234', '555-100-0002', '20 Vendor Ave, San Diego, CA',     'Seller', NULL),
('seller3', 'pass1234', '555-100-0003', '30 Market Rd, Sacramento, CA',     'Seller', NULL),
('seller4', 'pass1234', '555-100-0004', '40 Shop Ln, Oakland, CA',          'Seller', NULL),
('buyer1',  'pass1234', '555-200-0001', '100 Buyer Blvd, Riverside, CA',    'Buyer',  'Cars'),
('buyer2',  'pass1234', '555-200-0002', '200 Bidder St, Fresno, CA',        'Buyer',  'Car Parts'),
('buyer3',  'pass1234', '555-200-0003', '300 Auction Ave, Bakersfield, CA', 'Buyer',  'Collectibles'),
('buyer4',  'pass1234', '555-200-0004', '400 Winning Way, Long Beach, CA',  'Buyer',  'Cars'),
('buyer5',  'pass1234', '555-200-0005', '500 Bid Blvd, Anaheim, CA',        'Buyer',  'Car Parts');
 
INSERT INTO item (item_id, item_name, category, starting_price, image_url, item_condition, description, seller_login, seller_role) VALUES
(1,  '1996 Chevrolet Corvette C4',   'Cars',        8000.00, NULL, 'Used', '1996 Chevy Corvette C4, 5.7L V8, red, 89k miles, runs great.',            'seller1', 'Seller'),
(2,  '1994 Chevrolet Camaro Z28',    'Cars',        6500.00, NULL, 'Used', '1994 Camaro Z28, 5.7L V8, black, T-tops, 102k miles.',                    'seller1', 'Seller'),
(3,  '1993 Ford Mustang GT',         'Cars',        5500.00, NULL, 'Used', '1993 Mustang GT, 5.0L V8, red, 5-speed manual, 95k miles.',               'seller2', 'Seller'),
(4,  '1991 Dodge Viper RT/10',       'Cars',       18000.00, NULL, 'Used', '1991 Dodge Viper RT/10, 8.0L V10, red, collector condition, 45k miles.',  'seller2', 'Seller'),
(5,  '1998 Pontiac Trans Am',        'Cars',        7000.00, NULL, 'Used', '1998 Pontiac Trans Am, 5.7L LS1, white, 78k miles, WS6 package.',         'seller3', 'Seller'),
(6,  '1995 Chevrolet Impala SS',     'Cars',        9000.00, NULL, 'Used', '1995 Chevy Impala SS, 5.7L LT1, black, 67k miles, all original.',         'seller3', 'Seller'),
(7,  'Holley Carb 750 CFM',          'Car Parts',    250.00, NULL, 'Used', 'Holley double-pumper 750 CFM carburetor, fits small block Chevy.',         'seller4', 'Seller'),
(8,  'Flowmaster Exhaust System',    'Car Parts',    180.00, NULL, 'New',  'Flowmaster American Thunder cat-back exhaust, fits 93-97 Camaro/Firebird.','seller4', 'Seller'),
(9,  'Edelbrock Intake Manifold',    'Car Parts',    320.00, NULL, 'Used', 'Edelbrock Performer RPM intake manifold for small block Chevy 350.',       'seller1', 'Seller'),
(10, 'Vintage Corvette Poster Set',  'Collectibles',  45.00, NULL, 'New',  'Set of 6 vintage Corvette racing posters, 18x24 inches each.',             'seller2', 'Seller'),
(11, 'Car Cover for Corvette C4',    'Car Parts',     80.00, NULL, 'New',  'Custom-fit car cover for C4 Corvette, weatherproof, grey.',                'seller3', 'Seller'),
(12, '1:18 Scale 1969 Camaro Model', 'Collectibles',  35.00, NULL, 'New',  'Die-cast 1:18 scale model of 1969 Chevy Camaro SS, orange with stripes.',  'seller4', 'Seller');
 
INSERT INTO auction (auction_id, item_id, seller_login, seller_role, current_highest_bid, auction_status, winner_login, winner_role) VALUES
(1,  1,  'seller1', 'Seller',  8750.00, 'Active', NULL,     NULL),
(2,  2,  'seller1', 'Seller',  7000.00, 'Active', NULL,     NULL),
(3,  3,  'seller2', 'Seller',  6000.00, 'Active', NULL,     NULL),
(4,  4,  'seller2', 'Seller', 19500.00, 'Active', NULL,     NULL),
(5,  5,  'seller3', 'Seller',  7500.00, 'Active', NULL,     NULL),
(6,  6,  'seller3', 'Seller',  9500.00, 'Active', NULL,     NULL),
(7,  7,  'seller4', 'Seller',   275.00, 'Active', NULL,     NULL),
(8,  8,  'seller4', 'Seller',   200.00, 'Active', NULL,     NULL),
(9,  9,  'seller1', 'Seller',   360.00, 'Closed', 'buyer1', 'Buyer'),
(10, 10, 'seller2', 'Seller',    60.00, 'Closed', 'buyer2', 'Buyer'),
(11, 11, 'seller3', 'Seller',    95.00, 'Closed', 'buyer3', 'Buyer'),
(12, 12, 'seller4', 'Seller',    50.00, 'Closed', 'buyer4', 'Buyer');
 
INSERT INTO bid (bid_id, auction_id, buyer_login, buyer_role, bid_amount, bid_timestamp) VALUES
(1,  1, 'buyer1', 'Buyer',  8200.00, '2026-06-01 10:00:00'),
(2,  1, 'buyer2', 'Buyer',  8500.00, '2026-06-02 11:00:00'),
(3,  1, 'buyer3', 'Buyer',  8750.00, '2026-06-03 12:00:00'),
(4,  2, 'buyer4', 'Buyer',  6700.00, '2026-06-01 09:00:00'),
(5,  2, 'buyer5', 'Buyer',  7000.00, '2026-06-02 14:00:00'),
(6,  3, 'buyer1', 'Buyer',  5700.00, '2026-06-03 08:00:00'),
(7,  3, 'buyer2', 'Buyer',  6000.00, '2026-06-04 09:00:00'),
(8,  4, 'buyer3', 'Buyer', 18500.00, '2026-06-04 10:00:00'),
(9,  4, 'buyer5', 'Buyer', 19500.00, '2026-06-05 11:00:00'),
(10, 5, 'buyer4', 'Buyer',  7200.00, '2026-06-02 15:00:00'),
(11, 5, 'buyer5', 'Buyer',  7500.00, '2026-06-03 16:00:00'),
(12, 6, 'buyer1', 'Buyer',  9200.00, '2026-06-05 11:00:00'),
(13, 6, 'buyer2', 'Buyer',  9500.00, '2026-06-05 14:00:00'),
(14, 7, 'buyer3', 'Buyer',   260.00, '2026-06-05 13:00:00'),
(15, 7, 'buyer4', 'Buyer',   275.00, '2026-06-05 15:00:00'),
(16, 8, 'buyer5', 'Buyer',   190.00, '2026-06-04 17:00:00'),
(17, 8, 'buyer1', 'Buyer',   200.00, '2026-06-05 18:00:00'),
(18, 9,  'buyer1', 'Buyer',  360.00, '2026-05-28 10:00:00'),
(19, 10, 'buyer2', 'Buyer',   60.00, '2026-05-29 11:00:00'),
(20, 11, 'buyer3', 'Buyer',   95.00, '2026-05-30 12:00:00'),
(21, 12, 'buyer4', 'Buyer',   50.00, '2026-05-31 13:00:00');
 
INSERT INTO payment (payment_id, auction_id, buyer_login, buyer_role, amount, payment_status) VALUES
(1, 9,  'buyer1', 'Buyer', 360.00, 'Completed'),
(2, 10, 'buyer2', 'Buyer',  60.00, 'Completed'),
(3, 11, 'buyer3', 'Buyer',  95.00, 'Pending'),
(4, 12, 'buyer4', 'Buyer',  50.00, 'Pending');
 
INSERT INTO shipment (shipment_id, auction_id, address, shipment_status, tracking_number) VALUES
(1, 9,  '100 Buyer Blvd, Riverside, CA',   'Delivered', 'TRK-0001-2026'),
(2, 10, '200 Bidder St, Fresno, CA',        'Shipped',   'TRK-0002-2026'),
(3, 11, '300 Auction Ave, Bakersfield, CA', 'Pending',   NULL),
(4, 12, '400 Winning Way, Long Beach, CA',  'Pending',   NULL);
