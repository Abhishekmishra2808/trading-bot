let currentSide = 'BUY';

const popularSymbols = [
    { symbol: 'BTCUSDT', name: 'Bitcoin', type: 'Crypto' },
    { symbol: 'ETHUSDT', name: 'Ethereum', type: 'Crypto' },
    { symbol: 'BNBUSDT', name: 'Binance Coin', type: 'Crypto' },
    { symbol: 'SOLUSDT', name: 'Solana', type: 'Crypto' },
    { symbol: 'XRPUSDT', name: 'Ripple', type: 'Crypto' },
    { symbol: 'ADAUSDT', name: 'Cardano', type: 'Crypto' },
    { symbol: 'DOGEUSDT', name: 'Dogecoin', type: 'Crypto' },
    { symbol: 'MATICUSDT', name: 'Polygon', type: 'Crypto' },
    { symbol: 'DOTUSDT', name: 'Polkadot', type: 'Crypto' },
    { symbol: 'AVAXUSDT', name: 'Avalanche', type: 'Crypto' },
    { symbol: 'SHIBUSDT', name: 'Shiba Inu', type: 'Crypto' },
    { symbol: 'LTCUSDT', name: 'Litecoin', type: 'Crypto' },
    { symbol: 'LINKUSDT', name: 'Chainlink', type: 'Crypto' },
    { symbol: 'TRXUSDT', name: 'TRON', type: 'Crypto' },
    { symbol: 'ATOMUSDT', name: 'Cosmos', type: 'Crypto' },
    { symbol: 'UNIUSDT', name: 'Uniswap', type: 'Crypto' },
    { symbol: 'XLMUSDT', name: 'Stellar', type: 'Crypto' },
    { symbol: 'ETCUSDT', name: 'Ethereum Classic', type: 'Crypto' },
    { symbol: 'ALGOUSDT', name: 'Algorand', type: 'Crypto' },
    { symbol: 'FILUSDT', name: 'Filecoin', type: 'Crypto' }
];

function initAutocomplete() {
    const symbolInputs = document.querySelectorAll('.symbol-input');
    
    symbolInputs.forEach(input => {
        const dropdown = input.nextElementSibling;
        
        input.addEventListener('input', function(e) {
            const value = e.target.value.toUpperCase();
            
            if (value.length === 0) {
                dropdown.style.display = 'none';
                return;
            }
            
            const matches = popularSymbols.filter(s => 
                s.symbol.includes(value) || s.name.toUpperCase().includes(value)
            ).slice(0, 8);
            
            if (matches.length > 0) {
                dropdown.innerHTML = matches.map(s => `
                    <div class="autocomplete-item" data-symbol="${s.symbol}">
                        <div>
                            <div class="symbol-label">${s.symbol}</div>
                            <div class="symbol-type">${s.name}</div>
                        </div>
                        <i class="bi bi-arrow-return-left text-secondary"></i>
                    </div>
                `).join('');
                dropdown.style.display = 'block';
                
                dropdown.querySelectorAll('.autocomplete-item').forEach(item => {
                    item.addEventListener('click', function() {
                        input.value = this.dataset.symbol;
                        dropdown.style.display = 'none';
                    });
                });
            } else {
                dropdown.style.display = 'none';
            }
        });
        
        input.addEventListener('blur', function() {
            setTimeout(() => dropdown.style.display = 'none', 200);
        });
        
        input.addEventListener('focus', function() {
            if (this.value.length > 0) {
                this.dispatchEvent(new Event('input'));
            }
        });
    });
}

function showAlert(message, type = 'success') {
    const alertContainer = document.getElementById('alertContainer');
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    
    let icon = type === 'success' ? 'check-circle' : 'exclamation-triangle';
    
    alertDiv.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="bi bi-${icon} me-2"></i>
            <div>${message}</div>
        </div>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    alertContainer.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 8000);
}

function showAPIKeyError() {
    showAlert(`
        <strong>API Key Error!</strong><br>
        Your testnet API keys may have expired or are invalid.<br>
        <strong>Solution:</strong> Visit <a href="https://testnet.binancefuture.com/" target="_blank" class="text-decoration-underline">testnet.binancefuture.com</a> to generate new keys.<br>
        Then update your .env file and restart the app.<br>
        See <strong>API_KEY_SETUP.txt</strong> for detailed instructions.
    `, 'danger');
}

function addActivity(message, type = 'info') {
    const activityLog = document.getElementById('activityLog');
    const timestamp = new Date().toLocaleTimeString();
    const activityItem = document.createElement('div');
    activityItem.className = 'mb-2 pb-2 border-bottom border-secondary';
    activityItem.innerHTML = `
        <small class="text-secondary">${timestamp}</small><br>
        <span class="${type === 'success' ? 'text-success' : type === 'error' ? 'text-danger' : 'text-info'}">${message}</span>
    `;
    
    if (activityLog.querySelector('p.text-secondary')) {
        activityLog.innerHTML = '';
    }
    
    activityLog.insertBefore(activityItem, activityLog.firstChild);
    
    const items = activityLog.children;
    if (items.length > 10) {
        activityLog.removeChild(items[items.length - 1]);
    }
}

async function loadBalance() {
    const balanceContainer = document.getElementById('balanceContainer');
    balanceContainer.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"></div></div>';
    
    try {
        const response = await fetch('/api/balance');
        const data = await response.json();
        
        if (data.success) {
            const balances = data.balance.filter(b => parseFloat(b.balance) > 0);
            
            if (balances.length === 0) {
                balanceContainer.innerHTML = '<p class="text-secondary text-center">No balance found</p>';
                return;
            }
            
            let html = '';
            balances.forEach(balance => {
                html += `
                    <div class="balance-item">
                        <div class="d-flex justify-content-between">
                            <span class="balance-asset">${balance.asset}</span>
                            <span class="balance-amount">${parseFloat(balance.balance).toFixed(4)}</span>
                        </div>
                        <small class="text-secondary">Available: ${parseFloat(balance.availableBalance).toFixed(4)}</small>
                    </div>
                `;
            });
            balanceContainer.innerHTML = html;
            addActivity('Balance refreshed', 'success');
        } else {
            balanceContainer.innerHTML = '<p class="text-danger">Failed to load balance</p>';
            showAlert(data.message, 'danger');
        }
    } catch (error) {
        balanceContainer.innerHTML = '<p class="text-danger">Error loading balance</p>';
        showAlert('Failed to load balance: ' + error.message, 'danger');
    }
}

async function handleMarketOrder(e) {
    e.preventDefault();
    const form = e.target;
    const button = document.activeElement;
    const side = button.dataset.side;
    
    const formData = new FormData(form);
    const data = {
        symbol: formData.get('symbol').toUpperCase(),
        side: side,
        quantity: formData.get('quantity')
    };
    
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Processing...';
    
    try {
        const response = await fetch('/api/market-order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert(`✅ Market ${side} order placed successfully! Order ID: ${result.order.orderId}`, 'success');
            addActivity(`Market ${side} ${data.quantity} ${data.symbol} - Order ID: ${result.order.orderId}`, 'success');
            form.reset();
            loadBalance();
        } else {
            if (result.message.includes('-2015') || result.message.includes('API-key')) {
                showAPIKeyError();
            } else {
                showAlert(`❌ Order failed: ${result.message}`, 'danger');
            }
            addActivity(`Failed: Market ${side} ${data.quantity} ${data.symbol}`, 'error');
        }
    } catch (error) {
        showAlert(`❌ Error: ${error.message}`, 'danger');
        addActivity(`Error placing market order`, 'error');
    } finally {
        button.disabled = false;
        button.innerHTML = side === 'BUY' ? '<i class="bi bi-arrow-up-circle"></i> Buy' : '<i class="bi bi-arrow-down-circle"></i> Sell';
    }
}

async function handleLimitOrder(e) {
    e.preventDefault();
    const form = e.target;
    const button = document.activeElement;
    const side = button.dataset.side;
    
    const formData = new FormData(form);
    const data = {
        symbol: formData.get('symbol').toUpperCase(),
        side: side,
        quantity: formData.get('quantity'),
        price: formData.get('price')
    };
    
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Processing...';
    
    try {
        const response = await fetch('/api/limit-order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert(`✅ Limit ${side} order placed successfully! Order ID: ${result.order.orderId}`, 'success');
            addActivity(`Limit ${side} ${data.quantity} ${data.symbol} @ ${data.price} - ID: ${result.order.orderId}`, 'success');
            form.reset();
            loadBalance();
        } else {
            showAlert(`❌ Order failed: ${result.message}`, 'danger');
            addActivity(`Failed: Limit ${side} ${data.quantity} ${data.symbol}`, 'error');
        }
    } catch (error) {
        showAlert(`❌ Error: ${error.message}`, 'danger');
        addActivity(`Error placing limit order`, 'error');
    } finally {
        button.disabled = false;
        button.innerHTML = side === 'BUY' ? '<i class="bi bi-arrow-up-circle"></i> Buy' : '<i class="bi bi-arrow-down-circle"></i> Sell';
    }
}

async function handleStopLimitOrder(e) {
    e.preventDefault();
    const form = e.target;
    const button = document.activeElement;
    const side = button.dataset.side;
    
    const formData = new FormData(form);
    const data = {
        symbol: formData.get('symbol').toUpperCase(),
        side: side,
        quantity: formData.get('quantity'),
        price: formData.get('price'),
        stopPrice: formData.get('stopPrice')
    };
    
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Processing...';
    
    try {
        const response = await fetch('/api/stop-limit-order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert(`✅ Stop-Limit ${side} order placed successfully!`, 'success');
            addActivity(`Stop-Limit ${side} ${data.quantity} ${data.symbol} - ID: ${result.order.orderId}`, 'success');
            form.reset();
        } else {
            showAlert(`❌ Order failed: ${result.message}`, 'danger');
            addActivity(`Failed: Stop-Limit order`, 'error');
        }
    } catch (error) {
        showAlert(`❌ Error: ${error.message}`, 'danger');
        addActivity(`Error placing stop-limit order`, 'error');
    } finally {
        button.disabled = false;
        button.innerHTML = side === 'BUY' ? '<i class="bi bi-arrow-up-circle"></i> Buy' : '<i class="bi bi-arrow-down-circle"></i> Sell';
    }
}

async function handleOCOOrder(e) {
    e.preventDefault();
    const form = e.target;
    const button = document.activeElement;
    const side = button.dataset.side;
    
    const formData = new FormData(form);
    const data = {
        symbol: formData.get('symbol').toUpperCase(),
        side: side,
        quantity: formData.get('quantity'),
        takeProfitPrice: formData.get('takeProfitPrice'),
        stopLossPrice: formData.get('stopLossPrice')
    };
    
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Processing...';
    
    try {
        const response = await fetch('/api/oco-order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert(`✅ OCO order placed successfully!`, 'success');
            addActivity(`OCO ${side} ${data.quantity} ${data.symbol} (TP: ${data.takeProfitPrice}, SL: ${data.stopLossPrice})`, 'success');
            form.reset();
        } else {
            showAlert(`❌ Order failed: ${result.message}`, 'danger');
            addActivity(`Failed: OCO order`, 'error');
        }
    } catch (error) {
        showAlert(`❌ Error: ${error.message}`, 'danger');
        addActivity(`Error placing OCO order`, 'error');
    } finally {
        button.disabled = false;
        button.innerHTML = side === 'BUY' ? '<i class="bi bi-arrow-up-circle"></i> Buy' : '<i class="bi bi-arrow-down-circle"></i> Sell';
    }
}

async function handleTWAP(e) {
    e.preventDefault();
    const form = e.target;
    const button = document.activeElement;
    const side = button.dataset.side;
    
    const formData = new FormData(form);
    const data = {
        symbol: formData.get('symbol').toUpperCase(),
        side: side,
        totalQuantity: formData.get('totalQuantity'),
        duration: formData.get('duration'),
        numOrders: formData.get('numOrders')
    };
    
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Executing...';
    
    try {
        const response = await fetch('/api/twap', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert(`✅ TWAP strategy completed! ${result.result.successful_orders}/${result.result.total_orders} orders executed`, 'success');
            addActivity(`TWAP ${side} ${data.totalQuantity} ${data.symbol} over ${data.duration}min`, 'success');
            form.reset();
            loadBalance();
        } else {
            showAlert(`❌ TWAP failed: ${result.message}`, 'danger');
            addActivity(`Failed: TWAP strategy`, 'error');
        }
    } catch (error) {
        showAlert(`❌ Error: ${error.message}`, 'danger');
        addActivity(`Error executing TWAP`, 'error');
    } finally {
        button.disabled = false;
        button.innerHTML = side === 'BUY' ? '<i class="bi bi-arrow-up-circle"></i> Buy' : '<i class="bi bi-arrow-down-circle"></i> Sell';
    }
}

async function handleOrderStatus(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const data = {
        symbol: formData.get('symbol').toUpperCase(),
        orderId: formData.get('orderId')
    };
    
    const resultDiv = document.getElementById('orderStatusResult');
    resultDiv.innerHTML = '<div class="text-center"><div class="spinner-border spinner-border-sm text-primary"></div></div>';
    
    try {
        const response = await fetch('/api/order-status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            const order = result.order;
            const statusColor = order.status === 'FILLED' ? 'success' : order.status === 'CANCELED' ? 'danger' : 'warning';
            
            resultDiv.innerHTML = `
                <div class="balance-item">
                    <h6>Order Details</h6>
                    <div class="row">
                        <div class="col-6"><small class="text-secondary">Order ID:</small><br>${order.orderId}</div>
                        <div class="col-6"><small class="text-secondary">Status:</small><br><span class="badge bg-${statusColor}">${order.status}</span></div>
                        <div class="col-6 mt-2"><small class="text-secondary">Symbol:</small><br>${order.symbol}</div>
                        <div class="col-6 mt-2"><small class="text-secondary">Side:</small><br><span class="badge bg-${order.side === 'BUY' ? 'success' : 'danger'}">${order.side}</span></div>
                        <div class="col-6 mt-2"><small class="text-secondary">Type:</small><br>${order.type}</div>
                        <div class="col-6 mt-2"><small class="text-secondary">Price:</small><br>${order.price || 'Market'}</div>
                        <div class="col-6 mt-2"><small class="text-secondary">Quantity:</small><br>${order.origQty}</div>
                        <div class="col-6 mt-2"><small class="text-secondary">Executed:</small><br>${order.executedQty}</div>
                    </div>
                </div>
            `;
            addActivity(`Checked order ${data.orderId} - Status: ${order.status}`, 'info');
        } else {
            resultDiv.innerHTML = `<p class="text-danger">${result.message}</p>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<p class="text-danger">Error: ${error.message}</p>`;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    initAutocomplete();
    
    document.getElementById('marketOrderForm').addEventListener('submit', handleMarketOrder);
    document.getElementById('limitOrderForm').addEventListener('submit', handleLimitOrder);
    document.getElementById('stopLimitOrderForm').addEventListener('submit', handleStopLimitOrder);
    document.getElementById('ocoOrderForm').addEventListener('submit', handleOCOOrder);
    document.getElementById('twapForm').addEventListener('submit', handleTWAP);
    document.getElementById('orderStatusForm').addEventListener('submit', handleOrderStatus);
    
    addActivity('Bot ready for trading', 'info');
});
