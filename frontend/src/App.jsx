import { useEffect, useState } from 'react'
import { fetchAll, postResource, patchResource } from './api'

const emptyLogin = { role: 'Buyer', login: '' }

function App() {
  const [user, setUser] = useState(emptyLogin)
  const [items, setItems] = useState([])
  const [auctions, setAuctions] = useState([])
  const [users, setUsers] = useState([])
  const [bids, setBids] = useState([])
  const [status, setStatus] = useState('')
  const [form, setForm] = useState({})

  const categories = [
    'Cars',
    'Car Parts',
    'Collectibles',
    'Electronics',
    'Clothing',
    'Other'
  ]

  function generateId(prefix = 'id') {
    const randomPart = Math.random().toString(36).slice(2, 8)
    return `${prefix}-${Date.now().toString(36)}-${randomPart}`
  }

  useEffect(() => {
    reloadData()
  }, [])

  async function reloadData() {
    setItems(await fetchAll('/api/items'))
    setAuctions(await fetchAll('/api/auctions'))
    setUsers(await fetchAll('/api/users'))
    setBids(await fetchAll('/api/bids'))
  }

  function handleChange(event) {
    const { name, value } = event.target
    setForm(prev => ({ ...prev, [name]: value }))
  }

  async function handleSubmit(path, payload) {
    const result = await postResource(path, payload)
    if (result.error) {
      setStatus(result.error)
      return
    }
    setStatus('Saved successfully.')
    setForm({})
    reloadData()
  }

  async function handlePatch(path, payload) {
    const result = await patchResource(path, payload)
    if (result.error) {
      setStatus(result.error)
      return
    }
    setStatus('Updated successfully.')
    setForm({})
    reloadData()
  }

  // --- Derived State Variables ---
  const buyerAuctions = auctions
  const sellerItems = items.filter(item => item.sellerLogin === user.login)
  //const sellerAuctions = auctions.filter(auction => auction.sellerLogin === user.login)
  const sellerAuctions = Object.values(
    auctions
      .filter(auction => auction.sellerLogin === user.login)
      .reduce((acc, auction) => {
        acc[auction.auctionId] = auction
        return acc
      }, {})
  )
  const userBids = bids.filter(bid => bid.buyerLogin === user.login)
  const currentWinningAuctions = auctions.filter(
    auction => auction.auctionStatus === 'active' && auction.buyerLogin === user.login
  )
  const wonAuctions = auctions.filter(
    auction => auction.auctionStatus === 'closed' && auction.buyerLogin === user.login
  )
  // Find current user
  const currentUserDetails = users.find(u => u.login === user.login) || {}
  
  // Find selected auction details if a user is currently bidding
  const selectedAuctionForBid = auctions.find(a => a.auctionId === form.auctionId)

  return (
    <div className="page">
      <header>
        <h1>Auction App</h1>
        <p>Choose a role and run buyer, seller, or admin workflows.</p>
      </header>

      <section className="card">
        <h2>Login / Role</h2>
        <div className="grid">
          <label>
            Role
            <select
              name="role"
              value={user.role}
              onChange={e => setUser({ ...user, role: e.target.value })}
            >
              <option value="Buyer">Buyer</option>
              <option value="Seller">Seller</option>
              <option value="Admin">Admin</option>
            </select>
          </label>
          <label>
            Login
            <input
              name="login"
              value={user.login}
              onChange={e => setUser({ ...user, login: e.target.value })}
              placeholder="buyer1 / seller1 / admin"
            />
          </label>
        </div>
      </section>

      <section className="card status-row">
        <strong>Status:</strong> {status || 'Ready'}
      </section>

      {user.role === 'Buyer' && (
        <section className="card">
          <h2>Buyer Dashboard</h2>
          <p>Browse active auctions and place a bid.</p>
          <div className="list">
            {buyerAuctions.length === 0 ? (
              <p>No auctions available yet.</p>
            ) : (
              buyerAuctions.map(auction => {
                const lastBid = auction.bids?.length > 0
                  ? [...auction.bids].sort((a, b) => new Date(b.bidTimestamp) - new Date(a.bidTimestamp))[0]
                  : null
                const lastBidTime = lastBid ? new Date(lastBid.bidTimestamp).toLocaleString() : null

                return (
                  <div key={auction.auctionId} className="item-row">
                    <div>
                      <strong>{auction.auctionId}</strong> — {auction.itemName || auction.itemId}
                      <div>Seller: {auction.sellerLogin}</div>
                      <div>Status: {auction.auctionStatus}</div>
                      <div>Category: {auction.category}</div>
                      <div>Condition: {auction.itemCondition || 'Unknown'}</div>
                      {auction.itemDescription && (
                        <div>Description: {auction.itemDescription}</div>
                      )}
                      <div>
                        Current bid: ${auction.currentHighestBid}
                        {lastBidTime && <span className="hint"> (Last bid: {lastBidTime})</span>}
                      </div>
                      {auction.auctionStatus === 'closed' && (
                        <div>Winner: {auction.buyerLogin || 'None'}</div>
                      )}
                      {auction.auctionStatus === 'active' && (
                        <div>Highest Bidder: {auction.buyerLogin || 'None'}</div>
                      )}
                    </div>
                    {auction.auctionStatus === 'active' ? (
                      <button
                        onClick={() => setForm({ type: 'bid', auctionId: auction.auctionId })}
                      >
                        Bid on this auction
                      </button>
                    ) : (
                      <div className="hint">Bidding is closed for this auction.</div>
                    )}
                  </div>
                )
              })
            )}

            {form.type === 'bid' && (
              <div className="form-panel">
                <h3>Place a bid</h3>
                <p className="hint">
                  Bidding on: <strong>{form.auctionId}</strong> 
                  {selectedAuctionForBid && (
                    <> — <span>{selectedAuctionForBid.itemName || selectedAuctionForBid.itemId}</span></>
                  )}
                </p>

                {selectedAuctionForBid && (
                  <div style={{ marginBottom: '15px' }}>
                    <strong>Current Bid:</strong> ${selectedAuctionForBid.currentHighestBid}
                  </div>
                )}

                <label>
                  Amount
                  <input
                    name="bidAmount"
                    type="number"
                    step="0.01"
                    value={form.bidAmount || ''}
                    onChange={handleChange}
                  />
                </label>
                <button
                  onClick={() =>
                    handleSubmit('/api/bids', {
                      bidId: form.bidId || generateId('bid'),
                      bidAmount: form.bidAmount,
                      buyerLogin: user.login,
                      auctionId: form.auctionId
                    })
                  }
                >
                  Submit Bid
                </button>
              </div>
            )}

            <div className="list">
              <h3>Your bids</h3>
              {userBids.length === 0 ? (
                <p>No bids placed yet.</p>
              ) : (
                userBids.map(bid => {
                  const auction = auctions.find(a => a.auctionId === bid.auctionId)
                  return (
                    <div key={bid.bidId} className="item-row">
                      {auction?.itemName || bid.auctionId} — ${bid.bidAmount} — {auction?.auctionStatus || 'unknown'} —{' '}
                      {new Date(bid.bidTimestamp).toLocaleString()}
                      <div>Highest bidder: {auction?.buyerLogin || 'None'}</div>
                    </div>
                  )
                })
              )}
            </div>

            <div className="list">
              <h3>Your current winnings</h3>
              {currentWinningAuctions.length === 0 ? (
                <p>No current winning bids.</p>
              ) : (
                currentWinningAuctions.map(auction => (
                  <div key={auction.auctionId} className="item-row">
                    {auction.itemId} - {auction.itemName || auction.itemId} — ${auction.currentHighestBid} — {auction.auctionStatus}
                  </div>
                ))
              )}
            </div>

<div className="list">
  <h3>Won items</h3>
  {wonAuctions.length === 0 ? (
    <p>No won items yet.</p>
  ) : (
    wonAuctions.map(auction => {
      const lastBid = auction.bids?.length > 0
        ? [...auction.bids].sort((a, b) => new Date(b.bidTimestamp) - new Date(a.bidTimestamp))[0]
        : null
      const lastBidTime = lastBid ? new Date(lastBid.bidTimestamp).toLocaleString() : 'N/A'
      const isPaid = auction.paymentStatus === 'paid'

      return (
        <div key={auction.auctionId} className="item-row" style={{ display: 'flex', justifyContent: 'between', alignItems: 'center' }}>
          <div>
            {auction.shipmentId || 'No Shipment ID'} - {auction.itemName} — ${auction.currentHighestBid} —{' '}
            {auction.shippingStatus || 'Not shipped'} — Winning Bid: {lastBidTime}
            <div><strong>Payment Status:</strong> {auction.paymentStatus || 'unpaid'}</div>
          </div>
          
          {!isPaid && (
            <button
              onClick={() =>
                handlePatch(`/api/auctions/${auction.auctionId}`, {
                  buyerLogin: user.login,
                  paymentStatus: 'paid'
                })
              }
              style={{ marginLeft: '10px' }}
            >
              Pay for this item
            </button>
          )}
        </div>
      )
    })
  )}
</div>

            <div className="list">
              <h3>Personal Data</h3>
              <div>Login: {user.login}</div>
              <div>Favorite category: {currentUserDetails.favoriteCategory || 'None'}</div>
              <div>Phone: {currentUserDetails.phoneNum || 'Unknown'}</div>
              <div>Address: {currentUserDetails.address || 'Unknown'}</div>
            </div>
          </div>
        </section>
      )}

      {user.role === 'Seller' && (
        <section className="card">
          <h2>Seller Dashboard</h2>
          <div className="grid">
            <div className="form-panel">
              <h3>Create Item</h3>
              <p className="hint">Item ID is assigned automatically when the item is created.</p>
              <label>
                Name
                <input name="itemName" value={form.itemName || ''} onChange={handleChange} />
              </label>
              <label>
                Category
                <select name="category" value={form.category || categories[0]} onChange={handleChange}>
                  {categories.map(category => (
                    <option key={category} value={category}>
                      {category}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Condition
                <select name="condition" value={form.condition || 'New'} onChange={handleChange}>
                  <option value="New">New</option>
                  <option value="Used">Used</option>
                </select>
              </label>
              <label>
                Price
                <input
                  name="startingPrice"
                  type="number"
                  step="0.01"
                  value={form.startingPrice || ''}
                  onChange={handleChange}
                />
              </label>
              <label>
                Image URL
                <input name="imageURL" value={form.imageURL || ''} onChange={handleChange} />
              </label>
              <label>
                Description
                <input name="description" value={form.description || ''} onChange={handleChange} />
              </label>
              <button
                onClick={() =>
                  handleSubmit('/api/items', {
                    itemId: generateId('item'),
                    itemName: form.itemName,
                    category: form.category || categories[0],
                    condition: form.condition,
                    startingPrice: form.startingPrice,
                    imageURL: form.imageURL,
                    description: form.description,
                    sellerLogin: user.login
                  })
                }
              >
                Create Item
              </button>
            </div>

            <div className="form-panel">
              <h3>Create Auction</h3>
              <p className="hint">Auction ID is assigned automatically when the auction is created.</p>
              <label>
                Item
                <select
                  name="listedItemId"
                  value={form.listedItemId || ''}
                  onChange={e => setForm(prev => ({ ...prev, listedItemId: e.target.value }))}
                >
                  <option value="">Select one of your items</option>
                  {sellerItems.map(item => (
                    <option key={item.itemId} value={item.itemId}>
                      {item.itemName} — {item.category}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Status
                <select name="auctionStatus" value={form.auctionStatus || 'active'} onChange={handleChange}>
                  <option value="active">active</option>
                  <option value="closed">closed</option>
                  <option value="cancelled">cancelled</option>
                </select>
              </label>
              <button
                disabled={!form.listedItemId}
                onClick={() =>
                  handleSubmit('/api/auctions', {
                    auctionId: generateId('auction'),
                    auctionStatus: form.auctionStatus,
                    currentHighestBid: form.currentHighestBid || 0,
                    sellerLogin: user.login,
                    itemId: form.listedItemId
                  })
                }
              >
                Create Auction
              </button>
            </div>
          </div>

          <div className="list">
            <h3>Your items</h3>
            {sellerItems.length === 0 ? <p>No items yet.</p> : sellerItems.map(item => (
              <div key={item.itemId} className="item-row">
                <strong>{item.itemName}</strong> {item.category} - ${item.startingPrice}
              </div>
            ))}
          </div>

          <div className="list">
            <h3>Your auctions</h3>
            {sellerAuctions.length === 0 ? (
              <p>No auctions yet.</p>
            ) : (
              sellerAuctions.map(auction => (
                <div key={auction.auctionId} className="item-row">
                  <strong>{auction.itemName || auction.itemId}</strong>
                  <div>Status: {auction.auctionStatus}</div>
                  <div>Winning bid: ${auction.currentHighestBid}</div>
                  {auction.auctionStatus === 'closed' && (
                    <>
                      <div>Winner: {auction.buyerLogin || 'None'}</div>
                      <div>Winner phone: {auction.buyerPhone || 'Unknown'}</div>
                      <div>Shipping status: {auction.shippingStatus || 'Not shipped'}</div>
                      {auction.shippingAddress && (
                        <div>Shipping address: {auction.shippingAddress}</div>
                      )}
                    </>
                  )}
                </div>
              ))
            )}
          </div>
        </section>
      )}

      {user.role === 'Admin' && (
        <section className="card">
          <h2>Admin Dashboard</h2>
          <p>Review users and auction state.</p>
          <div className="list">
            <h3>Users</h3>
            {users.map(u => (
              <div key={u.login} className="item-row">
                {u.login} — {u.role} — {u.favoriteCategory || 'No favorite'}
              </div>
            ))}
          </div>

          <div className="form-panel">
            <h3>Manage Listings</h3>
            <label>
              Auction
              <select
                name="modifyAuctionId"
                value={form.modifyAuctionId || ''}
                onChange={handleChange}
              >
                <option value="">Select auction</option>
                {auctions.map(a => (
                  <option key={a.auctionId} value={a.auctionId}>
                    {a.auctionId} — {a.itemName || a.itemId}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Status
              <select
                name="modifyAuctionStatus"
                value={form.modifyAuctionStatus || 'active'}
                onChange={handleChange}
              >
                <option value="active">active</option>
                <option value="closed">closed</option>
                <option value="cancelled">cancelled</option>
              </select>
            </label>
            <button
              disabled={!form.modifyAuctionId}
              onClick={() =>
                handlePatch(`/api/auctions/${form.modifyAuctionId}`, {
                  adminLogin: user.login,
                  auctionStatus: form.modifyAuctionStatus
                })
              }
            >
              Update Listing
            </button>
          </div>

          <div className="list">
            <h3>Auctions</h3>
            {auctions.map(a => (
              <div key={a.auctionId} className="item-row">
                {a.auctionId} — {a.itemName || a.itemId} — seller: {a.sellerLogin} — {a.auctionStatus} — ${a.currentHighestBid} — highest bidder: {a.buyerLogin || 'None'}
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}

export default App