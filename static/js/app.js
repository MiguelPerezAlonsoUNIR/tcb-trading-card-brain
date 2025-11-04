// One Piece TCG Deck Builder - Frontend JavaScript

// Constants
const LOADING_MESSAGES = {
    buildDeck: 'Building your deck',
    analyzeDeck: 'Analyzing your deck'
};

let currentDeck = null;
let currentUser = null;
let allCards = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('deck-builder-form');
    form.addEventListener('submit', handleBuildDeck);

    const analyzeDeckBtn = document.getElementById('analyze-deck-btn');
    analyzeDeckBtn.addEventListener('click', handleAnalyzeDeck);

    const exportDeckBtn = document.getElementById('export-deck-btn');
    exportDeckBtn.addEventListener('click', handleExportDeck);

    // Setup filter buttons
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(btn => {
        btn.addEventListener('click', handleFilterCards);
    });

    // Authentication event listeners
    document.getElementById('login-btn').addEventListener('click', () => openModal('login-modal'));
    document.getElementById('register-btn').addEventListener('click', () => openModal('register-modal'));
    document.getElementById('logout-btn').addEventListener('click', handleLogout);
    
    // Modal close buttons
    document.querySelectorAll('.modal .close').forEach(btn => {
        btn.addEventListener('click', function() {
            this.closest('.modal').style.display = 'none';
        });
    });

    // Authentication forms
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    document.getElementById('register-form').addEventListener('submit', handleRegister);
    
    // Deck management
    document.getElementById('save-deck-btn').addEventListener('click', () => openModal('save-deck-modal'));
    document.getElementById('save-deck-form').addEventListener('submit', handleSaveDeck);
    document.getElementById('my-decks-btn').addEventListener('click', showMyDecks);
    
    // Collection management
    document.getElementById('my-collection-btn').addEventListener('click', showMyCollection);
    document.getElementById('add-card-btn').addEventListener('click', () => openModal('add-card-modal'));
    document.getElementById('add-card-form').addEventListener('submit', handleAddCard);
    document.getElementById('suggest-deck-btn').addEventListener('click', handleSuggestDeck);

    // Check if user is logged in
    checkAuthStatus();
    
    // Load all cards for autocomplete
    loadAllCards();
});

// Authentication functions
async function checkAuthStatus() {
    try {
        const response = await fetch('/api/current-user', {
            credentials: 'include'
        });
        const data = await response.json();
        
        if (data.authenticated) {
            currentUser = data.user;
            updateUIForAuthenticatedUser();
        } else {
            updateUIForGuestUser();
        }
    } catch (error) {
        console.error('Error checking auth status:', error);
        updateUIForGuestUser();
    }
}

function updateUIForAuthenticatedUser() {
    document.getElementById('auth-section').style.display = 'none';
    document.getElementById('user-section').style.display = 'flex';
    document.getElementById('username-display').textContent = `👤 ${currentUser.username}`;
    document.getElementById('save-deck-btn').style.display = 'inline-block';
}

function updateUIForGuestUser() {
    document.getElementById('auth-section').style.display = 'flex';
    document.getElementById('user-section').style.display = 'none';
    document.getElementById('save-deck-btn').style.display = 'none';
    currentUser = null;
}

async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const errorDiv = document.getElementById('login-error');
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentUser = data.user;
            closeModal('login-modal');
            updateUIForAuthenticatedUser();
            document.getElementById('login-form').reset();
            errorDiv.style.display = 'none';
        } else {
            errorDiv.textContent = data.error;
            errorDiv.style.display = 'block';
        }
    } catch (error) {
        errorDiv.textContent = 'Login failed. Please try again.';
        errorDiv.style.display = 'block';
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const errorDiv = document.getElementById('register-error');
    
    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentUser = data.user;
            closeModal('register-modal');
            updateUIForAuthenticatedUser();
            document.getElementById('register-form').reset();
            errorDiv.style.display = 'none';
        } else {
            errorDiv.textContent = data.error;
            errorDiv.style.display = 'block';
        }
    } catch (error) {
        errorDiv.textContent = 'Registration failed. Please try again.';
        errorDiv.style.display = 'block';
    }
}

async function handleLogout() {
    try {
        await fetch('/api/logout', {
            method: 'POST',
            credentials: 'include'
        });
        updateUIForGuestUser();
        hideAllSections();
    } catch (error) {
        console.error('Logout failed:', error);
    }
}

// Deck management functions
async function handleSaveDeck(e) {
    e.preventDefault();
    if (!currentDeck) return;
    
    const name = document.getElementById('deck-name').value;
    const errorDiv = document.getElementById('save-deck-error');
    
    try {
        const response = await fetch('/api/decks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({
                name,
                strategy: currentDeck.strategy,
                color: currentDeck.color,
                leader: currentDeck.leader,
                main_deck: currentDeck.main_deck
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            closeModal('save-deck-modal');
            document.getElementById('save-deck-form').reset();
            errorDiv.style.display = 'none';
            alert('Deck saved successfully!');
        } else {
            errorDiv.textContent = data.error;
            errorDiv.style.display = 'block';
        }
    } catch (error) {
        errorDiv.textContent = 'Failed to save deck. Please try again.';
        errorDiv.style.display = 'block';
    }
}

async function showMyDecks() {
    hideAllSections();
    const section = document.getElementById('user-decks-section');
    section.style.display = 'block';
    const listDiv = document.getElementById('saved-decks-list');
    listDiv.innerHTML = '<div class="loading">Loading your decks...</div>';
    
    try {
        const response = await fetch('/api/decks', {
            credentials: 'include'
        });
        const data = await response.json();
        
        if (data.success && data.decks.length > 0) {
            listDiv.innerHTML = data.decks.map(deck => `
                <div class="saved-deck-item">
                    <h3>${deck.name}</h3>
                    <p>Strategy: ${deck.strategy} | Color: ${deck.color}</p>
                    <p>Leader: ${deck.leader.name}</p>
                    <button onclick="loadDeck(${deck.id})" class="btn btn-primary">Load</button>
                    <button onclick="deleteDeck(${deck.id})" class="btn btn-secondary">Delete</button>
                </div>
            `).join('');
        } else {
            listDiv.innerHTML = '<p>No saved decks yet. Build and save a deck to see it here!</p>';
        }
    } catch (error) {
        listDiv.innerHTML = '<p>Failed to load decks.</p>';
    }
}

async function loadDeck(deckId) {
    try {
        const response = await fetch(`/api/decks/${deckId}`, {
            credentials: 'include'
        });
        const data = await response.json();
        
        if (data.success) {
            currentDeck = data.deck;
            displayDeck(currentDeck);
            hideAllSections();
        }
    } catch (error) {
        alert('Failed to load deck');
    }
}

async function deleteDeck(deckId) {
    if (!confirm('Are you sure you want to delete this deck?')) return;
    
    try {
        const response = await fetch(`/api/decks/${deckId}`, {
            method: 'DELETE',
            credentials: 'include'
        });
        const data = await response.json();
        
        if (data.success) {
            showMyDecks();
        } else {
            alert('Failed to delete deck');
        }
    } catch (error) {
        alert('Failed to delete deck');
    }
}

// Collection management functions
async function loadAllCards() {
    try {
        const response = await fetch('/api/cards');
        const cards = await response.json();
        allCards = cards;
        
        // Populate datalist for autocomplete
        const datalist = document.getElementById('cards-list');
        datalist.innerHTML = cards.map(card => 
            `<option value="${card.name}">`
        ).join('');
    } catch (error) {
        console.error('Failed to load cards:', error);
    }
}

async function showMyCollection() {
    hideAllSections();
    const section = document.getElementById('user-collection-section');
    section.style.display = 'block';
    const listDiv = document.getElementById('collection-list');
    listDiv.innerHTML = '<div class="loading">Loading your collection...</div>';
    
    try {
        const response = await fetch('/api/collection', {
            credentials: 'include'
        });
        const data = await response.json();
        
        if (data.success && data.collection.length > 0) {
            listDiv.innerHTML = `
                <div class="collection-grid">
                    ${data.collection.map(item => `
                        <div class="collection-item">
                            <strong>${item.card_name}</strong>
                            <p>Quantity: ${item.quantity}</p>
                            <button onclick="removeFromCollection(${item.id})" class="btn btn-secondary">Remove</button>
                        </div>
                    `).join('')}
                </div>
            `;
        } else {
            listDiv.innerHTML = '<p>No cards in collection yet. Add cards to track what you own!</p>';
        }
    } catch (error) {
        listDiv.innerHTML = '<p>Failed to load collection.</p>';
    }
}

async function handleAddCard(e) {
    e.preventDefault();
    const cardName = document.getElementById('card-name-input').value;
    const quantity = parseInt(document.getElementById('card-quantity').value);
    const errorDiv = document.getElementById('add-card-error');
    
    try {
        const response = await fetch('/api/collection', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ card_name: cardName, quantity })
        });
        
        const data = await response.json();
        
        if (data.success) {
            closeModal('add-card-modal');
            document.getElementById('add-card-form').reset();
            errorDiv.style.display = 'none';
            showMyCollection();
        } else {
            errorDiv.textContent = data.error;
            errorDiv.style.display = 'block';
        }
    } catch (error) {
        errorDiv.textContent = 'Failed to add card. Please try again.';
        errorDiv.style.display = 'block';
    }
}

async function removeFromCollection(itemId) {
    if (!confirm('Remove this card from your collection?')) return;
    
    try {
        const response = await fetch(`/api/collection/${itemId}`, {
            method: 'DELETE',
            credentials: 'include'
        });
        const data = await response.json();
        
        if (data.success) {
            showMyCollection();
        } else {
            alert('Failed to remove card');
        }
    } catch (error) {
        alert('Failed to remove card');
    }
}

async function handleSuggestDeck() {
    const strategy = document.getElementById('strategy').value;
    const color = document.getElementById('color').value;
    
    hideAllSections();
    const deckDisplay = document.getElementById('deck-display');
    deckDisplay.style.display = 'block';
    deckDisplay.innerHTML = '<div class="loading">Building deck from your collection...</div>';
    
    try {
        const response = await fetch('/api/suggest-deck', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ strategy, color })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentDeck = data.deck;
            displayDeck(currentDeck);
            
            // Show collection coverage if available
            if (currentDeck.collection_coverage) {
                const coverage = currentDeck.collection_coverage;
                const statsDiv = document.getElementById('deck-stats-content');
                statsDiv.innerHTML += `
                    <div class="collection-coverage">
                        <h4>Collection Coverage</h4>
                        <p>You own ${coverage.cards_owned} out of ${coverage.total_cards} cards (${coverage.coverage_percentage}%)</p>
                        ${Object.keys(coverage.cards_needed).length > 0 ? `
                            <p>Cards you need:</p>
                            <ul>
                                ${Object.entries(coverage.cards_needed).map(([name, qty]) => 
                                    `<li>${name}: ${qty}x</li>`
                                ).join('')}
                            </ul>
                        ` : '<p>You have all the cards needed!</p>'}
                    </div>
                `;
            }
        } else {
            deckDisplay.innerHTML = `<div class="error">${data.error}</div>`;
        }
    } catch (error) {
        deckDisplay.innerHTML = '<div class="error">Failed to suggest deck</div>';
    }
}

// UI helper functions
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function hideAllSections() {
    document.getElementById('deck-display').style.display = 'none';
    document.getElementById('analysis-section').style.display = 'none';
    document.getElementById('user-decks-section').style.display = 'none';
    document.getElementById('user-collection-section').style.display = 'none';
}

// Handle deck building
async function handleBuildDeck(e) {
    e.preventDefault();
    
    const strategy = document.getElementById('strategy').value;
    const color = document.getElementById('color').value;
    const leader = document.getElementById('leader').value;

    // Hide other sections
    hideAllSections();
    
    // Show loading state
    const deckDisplay = document.getElementById('deck-display');
    deckDisplay.style.display = 'block';
    deckDisplay.innerHTML = `<div class="loading">${LOADING_MESSAGES.buildDeck}</div>`;

    try {
        const response = await fetch('/api/build-deck', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ strategy, color, leader: leader || null })
        });

        const data = await response.json();

        if (data.success) {
            currentDeck = data.deck;
            displayDeck(data.deck);
        } else {
            alert('Error building deck: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to build deck. Please try again.');
    }
}

// Display the built deck
function displayDeck(deck) {
    const deckDisplay = document.getElementById('deck-display');
    deckDisplay.style.display = 'block';
    deckDisplay.innerHTML = `
        <h2>Your Deck</h2>
        
        <div class="leader-section">
            <h3>Leader</h3>
            <div id="leader-card" class="card-display"></div>
        </div>

        <div class="deck-stats">
            <h3>Deck Statistics</h3>
            <div id="deck-stats-content"></div>
        </div>

        <div class="main-deck">
            <h3>Main Deck (50 cards)</h3>
            <div class="card-filters">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="Character">Characters</button>
                <button class="filter-btn" data-filter="Event">Events</button>
                <button class="filter-btn" data-filter="Stage">Stages</button>
            </div>
            <div id="main-deck-cards" class="cards-grid"></div>
        </div>

        <div class="deck-actions">
            <button id="analyze-deck-btn" class="btn btn-secondary">Analyze Deck</button>
            <button id="export-deck-btn" class="btn btn-secondary">Export Deck</button>
        </div>
    `;

    // Display leader
    const leaderCard = document.getElementById('leader-card');
    leaderCard.innerHTML = createCardHTML(deck.leader, true);

    // Display deck stats
    displayDeckStats(deck);

    // Display main deck cards
    displayMainDeck(deck.main_deck);

    // Re-attach event listeners
    document.getElementById('analyze-deck-btn').addEventListener('click', handleAnalyzeDeck);
    document.getElementById('export-deck-btn').addEventListener('click', handleExportDeck);
    
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(btn => {
        btn.addEventListener('click', handleFilterCards);
    });

    // Hide analysis section when new deck is built
    document.getElementById('analysis-section').style.display = 'none';
}

// Create HTML for a card
function createCardHTML(card, isLeader = false) {
    const colorsHTML = card.colors.map(color => 
        `<span class="color-badge color-${color}">${color}</span>`
    ).join('');

    const powerHTML = card.power ? `<span class="card-power">PWR: ${card.power}</span>` : '';
    const costHTML = !isLeader ? `<span class="card-cost">Cost: ${card.cost}</span>` : '';
    const lifeHTML = isLeader ? `<span class="card-power">Life: ${card.life}</span>` : '';
    
    // Add card image if available
    const imageHTML = card.image_url ? `
        <div class="card-image-container">
            <img src="${card.image_url}" alt="${card.name}" class="card-image" 
                 onerror="this.onerror=null; this.src='https://via.placeholder.com/300x420/667eea/ffffff?text=${encodeURIComponent(card.name)}'; this.classList.add('placeholder-image');">
        </div>
    ` : '';

    return `
        <div class="card ${isLeader ? 'leader-card' : ''}" data-type="${card.type}">
            ${imageHTML}
            <div class="card-content">
                <div class="card-name">${card.name}</div>
                <div class="card-meta">
                    <span class="card-type">${card.type}</span>
                    ${costHTML}
                    ${powerHTML}
                    ${lifeHTML}
                </div>
                <div class="card-colors">${colorsHTML}</div>
                <div class="card-effect">${card.effect || ''}</div>
            </div>
        </div>
    `;
}

// Display deck statistics
function displayDeckStats(deck) {
    const statsContent = document.getElementById('deck-stats-content');
    
    // Calculate statistics
    const typeCount = {};
    const colorCount = {};
    const costCurve = {};
    
    deck.main_deck.forEach(card => {
        // Type distribution
        typeCount[card.type] = (typeCount[card.type] || 0) + 1;
        
        // Color distribution
        card.colors.forEach(color => {
            colorCount[color] = (colorCount[color] || 0) + 1;
        });
        
        // Cost curve
        costCurve[card.cost] = (costCurve[card.cost] || 0) + 1;
    });

    const avgCost = (deck.main_deck.reduce((sum, card) => sum + card.cost, 0) / deck.main_deck.length).toFixed(2);

    let statsHTML = `
        <div class="stat-item">
            <span class="stat-label">Total Cards:</span>
            <span class="stat-value">${deck.main_deck.length}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Average Cost:</span>
            <span class="stat-value">${avgCost}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Strategy:</span>
            <span class="stat-value">${deck.strategy.charAt(0).toUpperCase() + deck.strategy.slice(1)}</span>
        </div>
    `;

    // Type distribution
    statsHTML += '<div class="stat-item"><span class="stat-label">Type Distribution:</span><br>';
    for (const [type, count] of Object.entries(typeCount)) {
        statsHTML += `${type}: ${count} (${((count/deck.main_deck.length)*100).toFixed(1)}%) `;
    }
    statsHTML += '</div>';

    // Color distribution
    statsHTML += '<div class="stat-item"><span class="stat-label">Color Distribution:</span><br>';
    for (const [color, count] of Object.entries(colorCount)) {
        statsHTML += `<span class="color-badge color-${color}">${color}: ${count}</span> `;
    }
    statsHTML += '</div>';

    statsContent.innerHTML = statsHTML;
}

// Display main deck cards
function displayMainDeck(mainDeck) {
    const mainDeckCards = document.getElementById('main-deck-cards');
    
    // Group cards by name and count
    const cardGroups = {};
    mainDeck.forEach(card => {
        if (!cardGroups[card.name]) {
            cardGroups[card.name] = { card: card, count: 0 };
        }
        cardGroups[card.name].count++;
    });

    let cardsHTML = '';
    for (const [name, data] of Object.entries(cardGroups)) {
        const card = data.card;
        const count = data.count;
        
        const colorsHTML = card.colors.map(color => 
            `<span class="color-badge color-${color}">${color}</span>`
        ).join('');

        const powerHTML = card.power ? `<span class="card-power">PWR: ${card.power}</span>` : '';
        
        // Add card image if available
        const imageHTML = card.image_url ? `
            <div class="card-image-container">
                <img src="${card.image_url}" alt="${card.name}" class="card-image" 
                     onerror="this.onerror=null; this.src='https://via.placeholder.com/300x420/667eea/ffffff?text=${encodeURIComponent(card.name)}'; this.classList.add('placeholder-image');">
            </div>
        ` : '';

        cardsHTML += `
            <div class="card" data-type="${card.type}">
                ${imageHTML}
                <div class="card-content">
                    <div class="card-name">${card.name} ${count > 1 ? `(x${count})` : ''}</div>
                    <div class="card-meta">
                        <span class="card-type">${card.type}</span>
                        <span class="card-cost">Cost: ${card.cost}</span>
                        ${powerHTML}
                    </div>
                    <div class="card-colors">${colorsHTML}</div>
                    <div class="card-effect">${card.effect || ''}</div>
                </div>
            </div>
        `;
    }

    mainDeckCards.innerHTML = cardsHTML;
}

// Handle card filtering
function handleFilterCards(e) {
    const filterType = e.target.dataset.filter;
    const cards = document.querySelectorAll('#main-deck-cards .card');
    
    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    e.target.classList.add('active');

    // Filter cards
    cards.forEach(card => {
        if (filterType === 'all' || card.dataset.type === filterType) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Handle deck analysis
async function handleAnalyzeDeck() {
    if (!currentDeck) {
        alert('Please build a deck first!');
        return;
    }

    const analysisSection = document.getElementById('analysis-section');
    analysisSection.style.display = 'block';
    analysisSection.innerHTML = `<div class="loading">${LOADING_MESSAGES.analyzeDeck}</div>`;

    try {
        const response = await fetch('/api/analyze-deck', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ deck: currentDeck.main_deck })
        });

        const data = await response.json();

        if (data.success) {
            displayAnalysis(data.analysis);
        } else {
            alert('Error analyzing deck: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to analyze deck. Please try again.');
    }
}

// Display deck analysis
function displayAnalysis(analysis) {
    const analysisSection = document.getElementById('analysis-section');
    
    let analysisHTML = '<h2>Deck Analysis</h2>';

    // Cost Curve
    analysisHTML += '<div class="chart-container">';
    analysisHTML += '<h3>Cost Curve</h3>';
    for (const [cost, count] of Object.entries(analysis.curve).sort((a, b) => a[0] - b[0])) {
        const percentage = (count / analysis.total_cards) * 100;
        analysisHTML += `
            <div class="stat-item">
                Cost ${cost}: ${count} cards (${percentage.toFixed(1)}%)
                <div style="background: #667eea; height: 10px; width: ${percentage * 3}px; margin-top: 5px; border-radius: 5px;"></div>
            </div>
        `;
    }
    analysisHTML += '</div>';

    // Type Distribution
    analysisHTML += '<div class="chart-container">';
    analysisHTML += '<h3>Type Distribution</h3>';
    for (const [type, count] of Object.entries(analysis.type_distribution)) {
        const percentage = (count / analysis.total_cards) * 100;
        analysisHTML += `
            <div class="stat-item">
                ${type}: ${count} cards (${percentage.toFixed(1)}%)
            </div>
        `;
    }
    analysisHTML += '</div>';

    // Color Distribution
    analysisHTML += '<div class="chart-container">';
    analysisHTML += '<h3>Color Distribution</h3>';
    for (const [color, count] of Object.entries(analysis.color_distribution)) {
        analysisHTML += `
            <div class="stat-item">
                <span class="color-badge color-${color}">${color}: ${count} cards</span>
            </div>
        `;
    }
    analysisHTML += '</div>';

    // Suggestions
    if (analysis.suggestions.length > 0) {
        analysisHTML += '<div class="chart-container">';
        analysisHTML += '<h3>AI Suggestions</h3>';
        analysis.suggestions.forEach(suggestion => {
            analysisHTML += `<div class="suggestion">💡 ${suggestion}</div>`;
        });
        analysisHTML += '</div>';
    }

    analysisSection.innerHTML = analysisHTML;
}

// Handle deck export
function handleExportDeck() {
    if (!currentDeck) {
        alert('Please build a deck first!');
        return;
    }

    // Create export text
    let exportText = '# One Piece TCG Deck\n\n';
    exportText += `## Leader\n${currentDeck.leader.name}\n\n`;
    exportText += '## Main Deck\n';

    const cardGroups = {};
    currentDeck.main_deck.forEach(card => {
        if (!cardGroups[card.name]) {
            cardGroups[card.name] = 0;
        }
        cardGroups[card.name]++;
    });

    for (const [name, count] of Object.entries(cardGroups)) {
        exportText += `${count}x ${name}\n`;
    }

    // Download as text file
    const blob = new Blob([exportText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'onepiece_deck.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}
