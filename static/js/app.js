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

    // Combat simulation
    document.getElementById('simulate-combat-btn').addEventListener('click', openSimulationModal);

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
            showSuccessMessage('Deck saved successfully!');
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
            showSuccessMessage('Deck loaded successfully!');
        }
    } catch (error) {
        showErrorMessage('Failed to load deck');
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
            showSuccessMessage('Deck deleted successfully!');
        } else {
            showErrorMessage('Failed to delete deck');
        }
    } catch (error) {
        showErrorMessage('Failed to delete deck');
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

function showSuccessMessage(message) {
    const messageDiv = createMessageDiv(message, 'success');
    document.body.appendChild(messageDiv);
    setTimeout(() => messageDiv.remove(), 3000);
}

function showErrorMessage(message) {
    const messageDiv = createMessageDiv(message, 'error');
    document.body.appendChild(messageDiv);
    setTimeout(() => messageDiv.remove(), 4000);
}

function createMessageDiv(message, type) {
    const div = document.createElement('div');
    div.className = `toast-message toast-${type}`;
    div.textContent = message;
    return div;
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

// Combat Simulation Functions
async function openSimulationModal() {
    if (!currentDeck) {
        showErrorMessage('Please build a deck first before running a simulation');
        return;
    }
    
    openModal('simulation-modal');
    
    // Reset simulation results
    document.getElementById('simulation-results').style.display = 'none';
    document.getElementById('opponent-selection').style.display = 'block';
    
    // Load opponent decks
    await loadOpponentDecks();
}

async function loadOpponentDecks() {
    const listDiv = document.getElementById('opponent-decks-list');
    listDiv.innerHTML = '<div class="loading">Loading opponent decks...</div>';
    
    try {
        const response = await fetch('/api/opponent-decks');
        const data = await response.json();
        
        if (data.success && data.decks.length > 0) {
            listDiv.innerHTML = data.decks.map(deck => `
                <div class="opponent-deck-card" onclick="selectOpponentDeck('${deck.id}')">
                    <h4>${deck.name}</h4>
                    <p class="deck-strategy"><strong>Strategy:</strong> ${deck.strategy}</p>
                    <p class="deck-color"><strong>Color:</strong> ${deck.color}</p>
                    <p class="deck-description">${deck.description}</p>
                    <p class="deck-winrate">🏆 Tournament Win Rate: <strong>${deck.win_rate}%</strong></p>
                    <button class="btn btn-primary btn-small">Select Opponent</button>
                </div>
            `).join('');
        } else {
            listDiv.innerHTML = '<p>No opponent decks available.</p>';
        }
    } catch (error) {
        listDiv.innerHTML = '<p>Failed to load opponent decks.</p>';
        console.error('Error loading opponent decks:', error);
    }
}

async function selectOpponentDeck(opponentDeckId) {
    const listDiv = document.getElementById('opponent-decks-list');
    listDiv.innerHTML = '<div class="loading">Running simulation... This may take a moment.</div>';
    
    try {
        const response = await fetch('/api/simulate-combat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                player_deck: currentDeck,
                opponent_deck_id: opponentDeckId,
                num_simulations: 1000
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displaySimulationResults(data.results);
        } else {
            showErrorMessage(data.error || 'Failed to run simulation');
            await loadOpponentDecks();
        }
    } catch (error) {
        showErrorMessage('Failed to run simulation. Please try again.');
        console.error('Error running simulation:', error);
        await loadOpponentDecks();
    }
}

function displaySimulationResults(results) {
    // Hide opponent selection and show results
    document.getElementById('opponent-selection').style.display = 'none';
    document.getElementById('simulation-results').style.display = 'block';
    
    const statsDiv = document.getElementById('simulation-stats');
    const insightsDiv = document.getElementById('simulation-insights');
    
    // Determine win rate color
    let winRateClass = 'neutral';
    if (results.win_rate >= 65) {
        winRateClass = 'high';
    } else if (results.win_rate >= 55) {
        winRateClass = 'good';
    } else if (results.win_rate >= 45) {
        winRateClass = 'neutral';
    } else if (results.win_rate >= 35) {
        winRateClass = 'low';
    } else {
        winRateClass = 'very-low';
    }
    
    // Display statistics
    statsDiv.innerHTML = `
        <div class="simulation-header">
            <h3>Your Deck vs ${results.opponent_name}</h3>
            <p class="opponent-desc">${results.opponent_description}</p>
        </div>
        
        <div class="simulation-matchup">
            <h4>Matchup: ${results.matchup_type}</h4>
        </div>
        
        <div class="simulation-winrate winrate-${winRateClass}">
            <div class="winrate-label">Predicted Win Rate</div>
            <div class="winrate-value">${results.win_rate}%</div>
            <div class="winrate-bar">
                <div class="winrate-fill" style="width: ${results.win_rate}%"></div>
            </div>
        </div>
        
        <div class="simulation-details">
            <div class="stat-card">
                <div class="stat-label">Simulations Run</div>
                <div class="stat-value">${results.simulations_run.toLocaleString()}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Wins</div>
                <div class="stat-value stat-positive">${results.wins.toLocaleString()}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Losses</div>
                <div class="stat-value stat-negative">${results.losses.toLocaleString()}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Win Turns</div>
                <div class="stat-value">${results.avg_win_turns}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Loss Turns</div>
                <div class="stat-value">${results.avg_loss_turns}</div>
            </div>
        </div>
        
        <div class="deck-comparison">
            <div class="deck-info">
                <h4>Your Deck</h4>
                <p>Strategy: <strong>${results.deck1_stats.strategy}</strong></p>
                <p>Primary Color: <strong>${results.deck1_stats.color}</strong></p>
                <p>Avg Cost: <strong>${results.deck1_stats.avg_cost.toFixed(2)}</strong></p>
                <p>Character Ratio: <strong>${(results.deck1_stats.character_ratio * 100).toFixed(1)}%</strong></p>
            </div>
            <div class="vs-divider">VS</div>
            <div class="deck-info">
                <h4>Opponent Deck</h4>
                <p>Strategy: <strong>${results.deck2_stats.strategy}</strong></p>
                <p>Primary Color: <strong>${results.deck2_stats.color}</strong></p>
                <p>Avg Cost: <strong>${results.deck2_stats.avg_cost.toFixed(2)}</strong></p>
                <p>Character Ratio: <strong>${(results.deck2_stats.character_ratio * 100).toFixed(1)}%</strong></p>
            </div>
        </div>
    `;
    
    // Display insights
    let insightsHTML = '<h4>AI Insights</h4><div class="insights-list">';
    results.insights.forEach(insight => {
        insightsHTML += `<div class="insight-item">${insight}</div>`;
    });
    insightsHTML += '</div>';
    
    // Display key cards if available
    if (results.key_cards) {
        insightsHTML += '<h4>Key Cards in Your Deck</h4><div class="key-cards">';
        
        if (results.key_cards.high_power && results.key_cards.high_power.length > 0) {
            insightsHTML += `<div class="key-card-group">
                <strong>High Power Threats:</strong> ${results.key_cards.high_power.join(', ')}
            </div>`;
        }
        
        if (results.key_cards.low_cost && results.key_cards.low_cost.length > 0) {
            insightsHTML += `<div class="key-card-group">
                <strong>Early Game Cards:</strong> ${results.key_cards.low_cost.join(', ')}
            </div>`;
        }
        
        if (results.key_cards.events && results.key_cards.events.length > 0) {
            insightsHTML += `<div class="key-card-group">
                <strong>Key Events:</strong> ${results.key_cards.events.join(', ')}
            </div>`;
        }
        
        insightsHTML += '</div>';
    }
    
    insightsDiv.innerHTML = insightsHTML;
    
    // Setup "Run Another Simulation" button
    document.getElementById('run-another-simulation').onclick = async () => {
        document.getElementById('simulation-results').style.display = 'none';
        document.getElementById('opponent-selection').style.display = 'block';
        await loadOpponentDecks();
    };
}

// Structure Deck Management
let currentStructureDeck = null;
let allStructureDecks = [];

// Add event listeners for structure deck functionality
document.addEventListener('DOMContentLoaded', () => {
    const structureDecksBtn = document.getElementById('structure-decks-btn');
    if (structureDecksBtn) {
        structureDecksBtn.addEventListener('click', showStructureDecks);
    }
    
    const backToCollectionBtn = document.getElementById('back-to-collection-btn');
    if (backToCollectionBtn) {
        backToCollectionBtn.addEventListener('click', showMyCollection);
    }
    
    const colorFilter = document.getElementById('structure-deck-color-filter');
    if (colorFilter) {
        colorFilter.addEventListener('change', filterStructureDecks);
    }
    
    const addStructureDeckBtn = document.getElementById('add-structure-deck-confirm-btn');
    if (addStructureDeckBtn) {
        addStructureDeckBtn.addEventListener('click', handleAddStructureDeck);
    }
    
    const cancelStructureDeckBtn = document.getElementById('cancel-structure-deck-btn');
    if (cancelStructureDeckBtn) {
        cancelStructureDeckBtn.addEventListener('click', () => closeModal('structure-deck-modal'));
    }
    
    const simulateStructureDeckBtn = document.getElementById('simulate-structure-deck-btn');
    if (simulateStructureDeckBtn) {
        simulateStructureDeckBtn.addEventListener('click', handleSimulateStructureDeck);
    }
});

async function showStructureDecks() {
    if (!currentUser) {
        alert('Please login to view structure decks');
        return;
    }
    
    hideAllSections();
    const section = document.getElementById('structure-decks-section');
    section.style.display = 'block';
    const listDiv = document.getElementById('structure-decks-list');
    listDiv.innerHTML = '<div class="loading">Loading structure decks...</div>';
    
    try {
        const response = await fetch('/api/structure-decks');
        const data = await response.json();
        
        if (data.success) {
            allStructureDecks = data.decks;
            displayStructureDecks(allStructureDecks);
        } else {
            listDiv.innerHTML = '<p>Failed to load structure decks.</p>';
        }
    } catch (error) {
        console.error('Error loading structure decks:', error);
        listDiv.innerHTML = '<p>Failed to load structure decks.</p>';
    }
}

function displayStructureDecks(decks) {
    const listDiv = document.getElementById('structure-decks-list');
    
    if (decks.length === 0) {
        listDiv.innerHTML = '<p>No structure decks found matching your filter.</p>';
        return;
    }
    
    listDiv.innerHTML = decks.map(deck => `
        <div class="structure-deck-card" onclick="showStructureDeckDetails('${deck.code}')">
            <div class="structure-deck-header">
                <h3>${deck.code}</h3>
                <span class="color-badge color-${deck.color.toLowerCase()}">${deck.color}</span>
            </div>
            <h4>${deck.name}</h4>
            <p class="structure-deck-description">${deck.description}</p>
            <p class="structure-deck-leader"><strong>Leader:</strong> ${deck.leader}</p>
            <button class="btn btn-primary" onclick="event.stopPropagation(); showStructureDeckDetails('${deck.code}')">
                View Details
            </button>
        </div>
    `).join('');
}

function filterStructureDecks() {
    const colorFilter = document.getElementById('structure-deck-color-filter').value;
    
    let filteredDecks = allStructureDecks;
    if (colorFilter !== 'all') {
        filteredDecks = allStructureDecks.filter(deck => deck.color === colorFilter);
    }
    
    displayStructureDecks(filteredDecks);
}

async function showStructureDeckDetails(deckCode) {
    try {
        const response = await fetch(`/api/structure-decks/${deckCode}`);
        const data = await response.json();
        
        if (data.success) {
            currentStructureDeck = data.deck;
            displayStructureDeckModal(data.deck);
            openModal('structure-deck-modal');
        } else {
            alert('Failed to load structure deck details');
        }
    } catch (error) {
        console.error('Error loading structure deck details:', error);
        alert('Failed to load structure deck details');
    }
}

function displayStructureDeckModal(deck) {
    document.getElementById('structure-deck-modal-title').textContent = `${deck.code} - ${deck.name}`;
    
    const infoDiv = document.getElementById('structure-deck-info');
    infoDiv.innerHTML = `
        <div class="structure-deck-modal-info">
            <p><strong>Color:</strong> <span class="color-badge color-${deck.color.toLowerCase()}">${deck.color}</span></p>
            <p><strong>Leader:</strong> ${deck.leader}</p>
            <p><strong>Description:</strong> ${deck.description}</p>
            <p><strong>Total Cards:</strong> ${Object.values(deck.cards).reduce((sum, qty) => sum + qty, 0)}</p>
        </div>
    `;
    
    const cardsDiv = document.getElementById('structure-deck-cards-list');
    const cardEntries = Object.entries(deck.cards).sort((a, b) => {
        // Sort leader first, then by quantity descending
        if (a[0] === deck.leader) return -1;
        if (b[0] === deck.leader) return 1;
        return b[1] - a[1];
    });
    
    cardsDiv.innerHTML = `
        <h3>Card List</h3>
        <div class="structure-deck-cards-grid">
            ${cardEntries.map(([cardName, quantity]) => `
                <div class="structure-deck-card-item ${cardName === deck.leader ? 'leader-card' : ''}">
                    <span class="card-quantity">×${quantity}</span>
                    <span class="card-name">${cardName}</span>
                    ${cardName === deck.leader ? '<span class="leader-badge">Leader</span>' : ''}
                </div>
            `).join('')}
        </div>
    `;
}

async function handleAddStructureDeck() {
    if (!currentStructureDeck) {
        alert('No structure deck selected');
        return;
    }
    
    const errorDiv = document.getElementById('structure-deck-error');
    const addBtn = document.getElementById('add-structure-deck-confirm-btn');
    
    // Disable button and show loading
    addBtn.disabled = true;
    addBtn.textContent = 'Adding...';
    errorDiv.style.display = 'none';
    
    try {
        const response = await fetch('/api/collection/add-structure-deck', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ deck_code: currentStructureDeck.code })
        });
        
        const data = await response.json();
        
        if (data.success) {
            closeModal('structure-deck-modal');
            alert(`Successfully added ${data.deck_code} to your collection!\n\nTotal cards modified: ${data.total_cards_modified}\nNew cards: ${data.added_cards.length}\nUpdated cards: ${data.updated_cards.length}`);
            showMyCollection();
        } else {
            errorDiv.textContent = data.error || 'Failed to add structure deck';
            errorDiv.style.display = 'block';
        }
    } catch (error) {
        console.error('Error adding structure deck:', error);
        errorDiv.textContent = 'Failed to add structure deck. Please try again.';
        errorDiv.style.display = 'block';
    } finally {
        // Re-enable button
        addBtn.disabled = false;
        addBtn.textContent = 'Add to Collection';
    }
}

async function handleSimulateStructureDeck() {
    if (!currentStructureDeck) {
        alert('No structure deck selected');
        return;
    }
    
    const errorDiv = document.getElementById('structure-deck-error');
    const simulateBtn = document.getElementById('simulate-structure-deck-btn');
    
    // Disable button and show loading
    simulateBtn.disabled = true;
    simulateBtn.textContent = 'Loading...';
    errorDiv.style.display = 'none';
    
    try {
        // Convert structure deck to combat format
        const response = await fetch(`/api/structure-decks/${currentStructureDeck.code}/convert`);
        const data = await response.json();
        
        if (data.success) {
            // Set the converted deck as current deck for simulation
            currentDeck = data.deck;
            
            // Close structure deck modal
            closeModal('structure-deck-modal');
            
            // Open simulation modal
            await openSimulationModal();
        } else {
            errorDiv.textContent = data.error || 'Failed to prepare deck for simulation';
            errorDiv.style.display = 'block';
        }
    } catch (error) {
        console.error('Error preparing structure deck for simulation:', error);
        errorDiv.textContent = 'Failed to prepare deck for simulation. Please try again.';
        errorDiv.style.display = 'block';
    } finally {
        // Re-enable button
        simulateBtn.disabled = false;
        simulateBtn.textContent = '⚔️ Simulate Combat';
    }
}
