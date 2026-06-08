import datetime
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy.exc import OperationalError

try:
    from backend.models import db, User, Item, Auction, Payment, Shipment, Bid
except ImportError:
    from models import db, User, Item, Auction, Payment, Shipment, Bid


def create_app():
    app = Flask(__name__)
    database_url = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app)

    def error(message, status=400):
        return jsonify({'error': message}), status

    def seed_initial_data():
        users = [
            {'login': 'admin1',  'phoneNum': '555-000-0001', 'role': 'Admin',  'password': 'admin123', 'address': '1 Admin Blvd, Los Angeles, CA',    'favoriteCategory': None},
            {'login': 'seller1', 'phoneNum': '555-100-0001', 'role': 'Seller', 'password': 'pass1234', 'address': '10 Seller St, San Francisco, CA',  'favoriteCategory': None},
            {'login': 'seller2', 'phoneNum': '555-100-0002', 'role': 'Seller', 'password': 'pass1234', 'address': '20 Vendor Ave, San Diego, CA',     'favoriteCategory': None},
            {'login': 'seller3', 'phoneNum': '555-100-0003', 'role': 'Seller', 'password': 'pass1234', 'address': '30 Market Rd, Sacramento, CA',     'favoriteCategory': None},
            {'login': 'seller4', 'phoneNum': '555-100-0004', 'role': 'Seller', 'password': 'pass1234', 'address': '40 Shop Ln, Oakland, CA',          'favoriteCategory': None},
            {'login': 'buyer1',  'phoneNum': '555-200-0001', 'role': 'Buyer',  'password': 'pass1234', 'address': '100 Buyer Blvd, Riverside, CA',    'favoriteCategory': 'Cars'},
            {'login': 'buyer2',  'phoneNum': '555-200-0002', 'role': 'Buyer',  'password': 'pass1234', 'address': '200 Bidder St, Fresno, CA',        'favoriteCategory': 'Car Parts'},
            {'login': 'buyer3',  'phoneNum': '555-200-0003', 'role': 'Buyer',  'password': 'pass1234', 'address': '300 Auction Ave, Bakersfield, CA', 'favoriteCategory': 'Collectibles'},
            {'login': 'buyer4',  'phoneNum': '555-200-0004', 'role': 'Buyer',  'password': 'pass1234', 'address': '400 Winning Way, Long Beach, CA',  'favoriteCategory': 'Cars'},
            {'login': 'buyer5',  'phoneNum': '555-200-0005', 'role': 'Buyer',  'password': 'pass1234', 'address': '500 Bid Blvd, Anaheim, CA',        'favoriteCategory': 'Car Parts'}
        ]

        items = [
            {'itemId': '1',  'itemName': '1996 Chevrolet Corvette C4',   'category': 'Cars',        'startingPrice': 8000.00,  'imageURL': None, 'condition': 'Used', 'description': '1996 Chevy Corvette C4, 5.7L V8, red, 89k miles, runs great.',            'sellerLogin': 'seller1'},
            {'itemId': '2',  'itemName': '1994 Chevrolet Camaro Z28',    'category': 'Cars',        'startingPrice': 6500.00,  'imageURL': None, 'condition': 'Used', 'description': '1994 Camaro Z28, 5.7L V8, black, T-tops, 102k miles.',                    'sellerLogin': 'seller1'},
            {'itemId': '3',  'itemName': '1993 Ford Mustang GT',         'category': 'Cars',        'startingPrice': 5500.00,  'imageURL': None, 'condition': 'Used', 'description': '1993 Mustang GT, 5.0L V8, red, 5-speed manual, 95k miles.',               'sellerLogin': 'seller2'},
            {'itemId': '4',  'itemName': '1991 Dodge Viper RT/10',       'category': 'Cars',        'startingPrice': 18000.00, 'imageURL': None, 'condition': 'Used', 'description': '1991 Dodge Viper RT/10, 8.0L V10, red, collector condition, 45k miles.',  'sellerLogin': 'seller2'},
            {'itemId': '5',  'itemName': '1998 Pontiac Trans Am',        'category': 'Cars',        'startingPrice': 7000.00,  'imageURL': None, 'condition': 'Used', 'description': '1998 Pontiac Trans Am, 5.7L LS1, white, 78k miles, WS6 package.',         'sellerLogin': 'seller3'},
            {'itemId': '6',  'itemName': '1995 Chevrolet Impala SS',     'category': 'Cars',        'startingPrice': 9000.00,  'imageURL': None, 'condition': 'Used', 'description': '1995 Chevy Impala SS, 5.7L LT1, black, 67k miles, all original.',         'sellerLogin': 'seller3'},
            {'itemId': '7',  'itemName': 'Holley Carb 750 CFM',          'category': 'Car Parts',   'startingPrice': 250.00,   'imageURL': None, 'condition': 'Used', 'description': 'Holley double-pumper 750 CFM carburetor, fits small block Chevy.',         'sellerLogin': 'seller4'},
            {'itemId': '8',  'itemName': 'Flowmaster Exhaust System',    'category': 'Car Parts',   'startingPrice': 180.00,   'imageURL': None, 'condition': 'New',  'description': 'Flowmaster American Thunder cat-back exhaust, fits 93-97 Camaro/Firebird.', 'sellerLogin': 'seller4'},
            {'itemId': '9',  'itemName': 'Edelbrock Intake Manifold',    'category': 'Car Parts',   'startingPrice': 320.00,   'imageURL': None, 'condition': 'Used', 'description': 'Edelbrock Performer RPM intake manifold for small block Chevy 350.',       'sellerLogin': 'seller1'},
            {'itemId': '10', 'itemName': 'Vintage Corvette Poster Set',  'category': 'Collectibles', 'startingPrice': 45.00,    'imageURL': None, 'condition': 'New',  'description': 'Set of 6 vintage Corvette racing posters, 18x24 inches each.',             'sellerLogin': 'seller2'},
            {'itemId': '11', 'itemName': 'Car Cover for Corvette C4',    'category': 'Car Parts',   'startingPrice': 80.00,    'imageURL': None, 'condition': 'New',  'description': 'Custom-fit car cover for C4 Corvette, weatherproof, grey.',                'sellerLogin': 'seller3'},
            {'itemId': '12', 'itemName': '1:18 Scale 1969 Camaro Model', 'category': 'Collectibles', 'startingPrice': 35.00,    'imageURL': None, 'condition': 'New',  'description': 'Die-cast 1:18 scale model of 1969 Chevy Camaro SS, orange with stripes.',  'sellerLogin': 'seller4'}
        ]

        auctions = [
            {'auctionId': '1',  'auctionStatus': 'active',   'currentHighestBid': 8750.00, 'sellerLogin': 'seller1', 'itemId': '1',  'buyerLogin': None},
            {'auctionId': '2',  'auctionStatus': 'active',   'currentHighestBid': 7000.00, 'sellerLogin': 'seller1', 'itemId': '2',  'buyerLogin': None},
            {'auctionId': '3',  'auctionStatus': 'active',   'currentHighestBid': 6000.00, 'sellerLogin': 'seller2', 'itemId': '3',  'buyerLogin': None},
            {'auctionId': '4',  'auctionStatus': 'active',   'currentHighestBid': 19500.00,'sellerLogin': 'seller2', 'itemId': '4',  'buyerLogin': None},
            {'auctionId': '5',  'auctionStatus': 'active',   'currentHighestBid': 7500.00, 'sellerLogin': 'seller3', 'itemId': '5',  'buyerLogin': None},
            {'auctionId': '6',  'auctionStatus': 'active',   'currentHighestBid': 9500.00, 'sellerLogin': 'seller3', 'itemId': '6',  'buyerLogin': None},
            {'auctionId': '7',  'auctionStatus': 'active',   'currentHighestBid': 275.00,  'sellerLogin': 'seller4', 'itemId': '7',  'buyerLogin': None},
            {'auctionId': '8',  'auctionStatus': 'active',   'currentHighestBid': 200.00,  'sellerLogin': 'seller4', 'itemId': '8',  'buyerLogin': None},
            {'auctionId': '9',  'auctionStatus': 'closed',   'currentHighestBid': 360.00,  'sellerLogin': 'seller1', 'itemId': '9',  'buyerLogin': 'buyer1'},
            {'auctionId': '10', 'auctionStatus': 'closed',   'currentHighestBid': 60.00,   'sellerLogin': 'seller2', 'itemId': '10', 'buyerLogin': 'buyer2'},
            {'auctionId': '11', 'auctionStatus': 'closed',   'currentHighestBid': 95.00,   'sellerLogin': 'seller3', 'itemId': '11', 'buyerLogin': 'buyer3'},
            {'auctionId': '12', 'auctionStatus': 'closed',   'currentHighestBid': 50.00,   'sellerLogin': 'seller4', 'itemId': '12', 'buyerLogin': 'buyer4'}
        ]

        bids = [
            {'bidId': '1',  'auctionId': '1',  'buyerLogin': 'buyer1', 'bidAmount': 8200.00, 'bidTimestamp': datetime.datetime.fromisoformat('2026-06-01 10:00:00')},
            {'bidId': '2',  'auctionId': '1',  'buyerLogin': 'buyer2', 'bidAmount': 8500.00, 'bidTimestamp': datetime.datetime.fromisoformat('2026-06-02 11:00:00')},
            {'bidId': '3',  'auctionId': '1',  'buyerLogin': 'buyer3', 'bidAmount': 8750.00, 'bidTimestamp': datetime.datetime.fromisoformat('2026-06-03 12:00:00')},
            {'bidId': '4',  'auctionId': '2',  'buyerLogin': 'buyer4', 'bidAmount': 6700.00, 'bidTimestamp': datetime.datetime.fromisoformat('2026-06-01 09:00:00')},
            {'bidId': '5',  'auctionId': '2',  'buyerLogin': 'buyer5', 'bidAmount': 7000.00, 'bidTimestamp': datetime.datetime.fromisoformat('2026-06-02 14:00:00')},
            {'bidId': '6',  'auctionId': '3',  'buyerLogin': 'buyer1', 'bidAmount': 5700.00, 'bidTimestamp': datetime.datetime.fromisoformat('2026-06-03 08:00:00')},
            {'bidId': '7',  'auctionId': '3',  'buyerLogin': 'buyer2', 'bidAmount': 6000.00, 'bidTimestamp': datetime.datetime.fromisoformat('2026-06-04 09:00:00')},
            {'bidId': '8',  'auctionId': '4',  'buyerLogin': 'buyer3', 'bidAmount': 18500.00,'bidTimestamp': datetime.datetime.fromisoformat('2026-06-04 10:00:00')},
            {'bidId': '9',  'auctionId': '4',  'buyerLogin': 'buyer5', 'bidAmount': 19500.00,'bidTimestamp': datetime.datetime.fromisoformat('2026-06-05 11:00:00')},
            {'bidId': '10', 'auctionId': '5',  'buyerLogin': 'buyer4', 'bidAmount': 7200.00, 'bidTimestamp': datetime.datetime.fromisoformat('2026-06-02 15:00:00')},
            {'bidId': '11', 'auctionId': '5',  'buyerLogin': 'buyer5', 'bidAmount': 7500.00, 'bidTimestamp': datetime.datetime.fromisoformat('2026-06-03 16:00:00')},
            {'bidId': '12', 'auctionId': '6',  'buyerLogin': 'buyer1', 'bidAmount': 9200.00, 'bidTimestamp': datetime.datetime.fromisoformat('2026-06-05 11:00:00')},
            {'bidId': '13', 'auctionId': '6',  'buyerLogin': 'buyer2', 'bidAmount': 9500.00, 'bidTimestamp': datetime.datetime.fromisoformat('2026-06-05 14:00:00')},
            {'bidId': '14', 'auctionId': '7',  'buyerLogin': 'buyer3', 'bidAmount': 260.00,  'bidTimestamp': datetime.datetime.fromisoformat('2026-06-05 13:00:00')},
            {'bidId': '15', 'auctionId': '7',  'buyerLogin': 'buyer4', 'bidAmount': 275.00,  'bidTimestamp': datetime.datetime.fromisoformat('2026-06-05 15:00:00')},
            {'bidId': '16', 'auctionId': '8',  'buyerLogin': 'buyer5', 'bidAmount': 190.00,  'bidTimestamp': datetime.datetime.fromisoformat('2026-06-04 17:00:00')},
            {'bidId': '17', 'auctionId': '8',  'buyerLogin': 'buyer1', 'bidAmount': 200.00,  'bidTimestamp': datetime.datetime.fromisoformat('2026-06-05 18:00:00')},
            {'bidId': '18', 'auctionId': '9',  'buyerLogin': 'buyer1', 'bidAmount': 360.00,  'bidTimestamp': datetime.datetime.fromisoformat('2026-05-28 10:00:00')},
            {'bidId': '19', 'auctionId': '10', 'buyerLogin': 'buyer2', 'bidAmount': 60.00,   'bidTimestamp': datetime.datetime.fromisoformat('2026-05-29 11:00:00')},
            {'bidId': '20', 'auctionId': '11', 'buyerLogin': 'buyer3', 'bidAmount': 95.00,   'bidTimestamp': datetime.datetime.fromisoformat('2026-05-30 12:00:00')},
            {'bidId': '21', 'auctionId': '12', 'buyerLogin': 'buyer4', 'bidAmount': 50.00,   'bidTimestamp': datetime.datetime.fromisoformat('2026-05-31 13:00:00')}
        ]

        payments = [
            {'paymentId': '1', 'auctionId': '9',  'buyerLogin': 'buyer1', 'amount': 360.00, 'paymentStatus': 'completed'},
            {'paymentId': '2', 'auctionId': '10', 'buyerLogin': 'buyer2', 'amount': 60.00,  'paymentStatus': 'completed'},
            {'paymentId': '3', 'auctionId': '11', 'buyerLogin': 'buyer3', 'amount': 95.00,  'paymentStatus': 'pending'},
            {'paymentId': '4', 'auctionId': '12', 'buyerLogin': 'buyer4', 'amount': 50.00,  'paymentStatus': 'pending'}
        ]

        shipments = [
            {'shipmentId': '1', 'auctionId': '9',  'address': '100 Buyer Blvd, Riverside, CA',   'shipmentStatus': 'delivered', 'trackingNumber': 'TRK-0001-2026'},
            {'shipmentId': '2', 'auctionId': '10', 'address': '200 Bidder St, Fresno, CA',        'shipmentStatus': 'shipped',   'trackingNumber': 'TRK-0002-2026'},
            {'shipmentId': '3', 'auctionId': '11', 'address': '300 Auction Ave, Bakersfield, CA', 'shipmentStatus': 'pending',   'trackingNumber': None},
            {'shipmentId': '4', 'auctionId': '12', 'address': '400 Winning Way, Long Beach, CA',  'shipmentStatus': 'pending',   'trackingNumber': None}
        ]

        all_entries = []
        for user_data in users:
            if not User.query.get(user_data['login']):
                db.session.add(User(**user_data))
                all_entries.append(f"user:{user_data['login']}")

        for item_data in items:
            if not Item.query.get(item_data['itemId']):
                db.session.add(Item(**item_data))
                all_entries.append(f"item:{item_data['itemId']}")

        for auction_data in auctions:
            if not Auction.query.get(auction_data['auctionId']):
                db.session.add(Auction(**auction_data))
                all_entries.append(f"auction:{auction_data['auctionId']}")

        for bid_data in bids:
            if not Bid.query.get(bid_data['bidId']):
                db.session.add(Bid(**bid_data))
                all_entries.append(f"bid:{bid_data['bidId']}")

        for payment_data in payments:
            if not Payment.query.get(payment_data['paymentId']):
                db.session.add(Payment(**payment_data))
                all_entries.append(f"payment:{payment_data['paymentId']}")

        for shipment_data in shipments:
            if not Shipment.query.get(shipment_data['shipmentId']):
                db.session.add(Shipment(**shipment_data))
                all_entries.append(f"shipment:{shipment_data['shipmentId']}")

        db.session.commit()
        return all_entries

    with app.app_context():
        try:
            db.create_all()
        except OperationalError as exc:
            if database_url != 'sqlite:///app.db':
                print('Warning: could not connect to DATABASE_URL. Falling back to sqlite:///app.db')
                app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
                db.engine.dispose()
                db.create_all()
            else:
                raise

        if User.query.count() == 0:
            seeded_entries = seed_initial_data()
            print('Seeded initial database entries:', seeded_entries)

    @app.route('/api/status', methods=['GET'])
    def status():
        return jsonify({'status': 'ok'})

    @app.route('/api/users', methods=['GET'])
    def list_users():
        users = User.query.all()
        return jsonify([user.serialize() for user in users])

    @app.route('/api/items', methods=['GET', 'POST'])
    def items():
        if request.method == 'GET':
            return jsonify([item.serialize() for item in Item.query.all()])

        payload = request.get_json() or {}
        required = ['itemId', 'itemName', 'condition', 'startingPrice', 'sellerLogin']
        missing = [k for k in required if not payload.get(k)]
        if missing:
            return error('Missing fields: ' + ', '.join(missing))

        seller = User.query.filter_by(login=payload['sellerLogin'], role='Seller').first()
        if not seller:
            return error('sellerLogin must reference a Seller user')

        if Item.query.get(payload['itemId']):
            return error('itemId already exists')

        item = Item(
            itemId=payload['itemId'],
            itemName=payload['itemName'],
            category=payload.get('category'),
            imageURL=payload.get('imageURL'),
            condition=payload['condition'],
            startingPrice=float(payload['startingPrice']),
            description=payload.get('description'),
            sellerLogin=payload['sellerLogin']
        )
        db.session.add(item)
        db.session.commit()
        return jsonify(item.serialize()), 201

    @app.route('/api/auctions', methods=['GET', 'POST'])
    def auctions():
        if request.method == 'GET':
            return jsonify([auction.serialize() for auction in Auction.query.all()])

        payload = request.get_json() or {}
        required = ['auctionId', 'auctionStatus', 'sellerLogin', 'itemId']
        missing = [k for k in required if not payload.get(k)]
        if missing:
            return error('Missing fields: ' + ', '.join(missing))

        seller = User.query.filter_by(login=payload['sellerLogin'], role='Seller').first()
        if not seller:
            return error('sellerLogin must reference a Seller user')

        item = Item.query.get(payload['itemId'])
        if not item:
            return error('itemId must reference an existing item')

        if Auction.query.get(payload['auctionId']):
            return error('auctionId already exists')

        auction = Auction(
            auctionId=payload['auctionId'],
            auctionStatus=payload['auctionStatus'],
            currentHighestBid=float(payload.get('currentHighestBid', 0.0)),
            sellerLogin=payload['sellerLogin'],
            itemId=payload['itemId']
        )
        db.session.add(auction)
        db.session.commit()
        return jsonify(auction.serialize()), 201

    @app.route('/api/auctions/<auction_id>', methods=['PATCH'])
    def update_auction(auction_id):
        payload = request.get_json() or {}
        if not payload.get('adminLogin'):
            return error('adminLogin is required')

        admin = User.query.filter_by(login=payload['adminLogin'], role='Admin').first()
        if not admin:
            return error('adminLogin must reference an Admin user')

        auction = Auction.query.get(auction_id)
        if not auction:
            return error('auctionId does not exist')

        if 'auctionStatus' in payload:
            auction.auctionStatus = payload['auctionStatus']

        db.session.commit()
        return jsonify(auction.serialize())

    @app.route('/api/bids', methods=['GET', 'POST'])
    def bids():
        if request.method == 'GET':
            return jsonify([bid.serialize() for bid in Bid.query.order_by(Bid.bidTimestamp.desc()).all()])

        payload = request.get_json() or {}
        required = ['bidId', 'bidAmount', 'buyerLogin', 'auctionId']
        missing = [k for k in required if not payload.get(k)]
        if missing:
            return error('Missing fields: ' + ', '.join(missing))

        buyer = User.query.filter_by(login=payload['buyerLogin'], role='Buyer').first()
        if not buyer:
            return error('buyerLogin must reference a Buyer user')

        auction = Auction.query.get(payload['auctionId'])
        if not auction:
            return error('auctionId does not exist')
        if auction.auctionStatus != 'active':
            return error('Auction must be active to place a bid')

        bid_amount = float(payload['bidAmount'])
        if bid_amount <= auction.currentHighestBid:
            return error('bidAmount must be higher than the current highest bid')

        if Bid.query.get(payload['bidId']):
            return error('bidId already exists')

        bid = Bid(
            bidId=payload['bidId'],
            bidAmount=bid_amount,
            buyerLogin=payload['buyerLogin'],
            auctionId=payload['auctionId']
        )
        auction.currentHighestBid = bid_amount
        auction.buyerLogin = payload['buyerLogin']

        db.session.add(bid)
        db.session.commit()
        return jsonify(bid.serialize()), 201

    @app.route('/api/payments', methods=['GET', 'POST'])
    def payments():
        if request.method == 'GET':
            return jsonify([payment.serialize() for payment in Payment.query.all()])

        payload = request.get_json() or {}
        required = ['paymentId', 'amount', 'paymentStatus', 'buyerLogin', 'auctionId']
        missing = [k for k in required if not payload.get(k)]
        if missing:
            return error('Missing fields: ' + ', '.join(missing))

        buyer = User.query.filter_by(login=payload['buyerLogin'], role='Buyer').first()
        if not buyer:
            return error('buyerLogin must reference a Buyer user')

        auction = Auction.query.get(payload['auctionId'])
        if not auction:
            return error('auctionId does not exist')

        if Payment.query.filter_by(auctionId=payload['auctionId']).first():
            return error('auctionId already has payment')

        payment = Payment(
            paymentId=payload['paymentId'],
            amount=float(payload['amount']),
            paymentStatus=payload['paymentStatus'],
            buyerLogin=payload['buyerLogin'],
            auctionId=payload['auctionId']
        )
        db.session.add(payment)
        db.session.commit()
        return jsonify(payment.serialize()), 201

    @app.route('/api/shipments', methods=['GET', 'POST'])
    def shipments():
        if request.method == 'GET':
            return jsonify([shipment.serialize() for shipment in Shipment.query.all()])

        payload = request.get_json() or {}
        required = ['shipmentId', 'address', 'shipmentStatus', 'auctionId']
        missing = [k for k in required if not payload.get(k)]
        if missing:
            return error('Missing fields: ' + ', '.join(missing))

        auction = Auction.query.get(payload['auctionId'])
        if not auction:
            return error('auctionId does not exist')

        if Shipment.query.filter_by(auctionId=payload['auctionId']).first():
            return error('auctionId already has shipment')

        shipment = Shipment(
            shipmentId=payload['shipmentId'],
            address=payload['address'],
            shipmentStatus=payload['shipmentStatus'],
            trackingNumber=payload.get('trackingNumber'),
            auctionId=payload['auctionId']
        )
        db.session.add(shipment)
        db.session.commit()
        return jsonify(shipment.serialize()), 201

    @app.route('/api/seed', methods=['POST'])
    def seed_data():
        seeded_entries = seed_initial_data()
        return jsonify({'seeded': seeded_entries})

    return app


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5001, debug=True)
