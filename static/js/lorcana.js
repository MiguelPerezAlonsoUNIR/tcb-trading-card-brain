// Disney Lorcana Deck Builder JavaScript
// Main application logic for the Lorcana deck builder

let currentDeck = null;
let currentUser = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    checkAuthStatus();
    setupEventListeners();
});

function checkAuthStatus() {
    fetch('/api/current-user')
        .then(response => response.json())
        .then(data => {
            if (data.authenticated) {
                currentUser = data.user;
                showUserSection();
            } else {
                showAuthSection();
            }
        })
        .catch(error => console.error('Error checking auth status:', error));
}

function showUserSection() {
    document.getElementById('auth-section').style.display = 'none';
    document.getElementById('user-section').style.display = 'flex';
    document.getElementById('username-display').textContent = `Welcome, ${currentUser.username}! ✨`;
    document.getElementById('save-deck-btn').style.display = 'inline-block';
}

function showAuthSection() {
    document.getElementById('auth-section').style.display = 'flex';
    document.getElementById('user-section').style.display = 'none';
    document.getElementById('save-deck-btn').style.display = 'none';
}

function setupEventListeners() {
    // Deck builder form
    document.getElementById('deck-builder-form').addEventListener('submit', handleBuildDeck);
    
    // Auth buttons
    document.getElementById('login-btn').addEventListener('click', () => showModal('login-modal'));
    document.getElementById('register-btn').addEventListener('click', () => showModal('register-modal'));
    document.getElementById('logout-btn').addEventListener('click', handleLogout);
    
    // Auth forms
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    document.getElementById('register-form').addEventListener('submit', handleRegister);
    
    // Deck actions
    document.getElementById('analyze-deck-btn').addEventListener('click', handleAnalyzeDeck);
    document.getElementById('export-deck-btn').addEventListener('click', handleExportDeck);
    document.getElementById('save-deck-btn').addEventListener('click', () => showModal('save-deck-modal'));
    document.getElementById('suggest-improvements-btn').addEventListener('click', handleSuggestImprovements);
    
    // Save deck form
    document.getElementById('save-deck-form').addEventListener('submit', handleSaveDeck);
    
    // User sections
    document.getElementById('my-decks-btn').addEventListener('click', showMyDecks);
    document.getElementById('my-collection-btn').addEventListener('click', showMyCollection);
    document.getElementById('back-to-builder-btn').addEventListener('click', backToBuilder);
    document.getElementById('back-from-collection-btn').addEventListener('click', backToBuilder);
    document.getElementById('back-from-analysis-btn').addEventListener('click', backToDeck);
    document.getElementById('back-from-improvements-btn').addEventListener('click', backToDeck);
    
    // Collection actions
    document.getElementById('add-card-btn').addEventListener('click', () => showModal('add-card-modal'));
    document.getElementById('add-card-form').addEventListener('submit', handleAddCard);
    document.getElementById('suggest-from-collection-btn').addEventListener('click', handleSuggestFromCollection);
    
    // Card filters
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', handleFilterCards);
    });
    
    // Modal close buttons
    document.querySelectorAll('.close').forEach(closeBtn => {
        closeBtn.addEventListener('click', function() {
            this.closest('.modal').style.display = 'none';
        });
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    });
}

// Build Deck
function handleBuildDeck(event) {
    event.preventDefault();
    
    const strategy = document.getElementById('strategy').value;
    const color1 = document.getElementById('color1').value;
    const color2 = document.getElementById('color2').value;
    
    // Validate that two different colors are selected
    if (!color1 || !color2) {
        alert('Please select both ink colors');
        return;
    }
    
    if (color1 === color2) {
        alert('Please select two different ink colors');
        return;
    }
    
    fetch('/api/lorcana/build-deck', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ strategy, colors: [color1, color2] })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentDeck = data.deck;
            displayDeck(currentDeck);
        } else {
            alert('Error building deck: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to build deck');
    });
}

function displayDeck(deck) {
    document.getElementById('deck-display').style.display = 'block';
    document.querySelector('.deck-builder').scrollIntoView({ behavior: 'smooth' });
    
    // Display stats
    displayDeckStats(deck);
    
    // Display cards
    displayCards(deck.main_deck);
}

function displayDeckStats(deck) {
    const stats = calculateDeckStats(deck.main_deck);
    const statsContent = document.getElementById('deck-stats-content');
    
    statsContent.innerHTML = `
        <div class="stat-box">
            <span class="stat-value">${stats.totalCards}</span>
            <span class="stat-label">Total Cards</span>
        </div>
        <div class="stat-box">
            <span class="stat-value">${stats.avgCost}</span>
            <span class="stat-label">Avg Cost</span>
        </div>
        <div class="stat-box">
            <span class="stat-value">${stats.characters}</span>
            <span class="stat-label">Characters</span>
        </div>
        <div class="stat-box">
            <span class="stat-value">${stats.actions}</span>
            <span class="stat-label">Actions</span>
        </div>
    `;
}

function calculateDeckStats(cards) {
    const totalCards = cards.length;
    const totalCost = cards.reduce((sum, card) => sum + (card.cost || 0), 0);
    const avgCost = totalCards > 0 ? (totalCost / totalCards).toFixed(1) : 0;
    
    const characters = cards.filter(c => c.type === 'Character').length;
    const actions = cards.filter(c => c.type === 'Action').length;
    const items = cards.filter(c => c.type === 'Item').length;
    
    return { totalCards, avgCost, characters, actions, items };
}

function displayCards(cards, filter = 'all') {
    const cardsGrid = document.getElementById('main-deck-cards');
    const filteredCards = filter === 'all' ? cards : cards.filter(c => c.type === filter);
    
    cardsGrid.innerHTML = filteredCards.map(card => `
        <div class="card">
            <div class="card-name">${card.name}</div>
            <span class="card-type">${card.type}</span>
            <div class="card-colors">
                ${card.colors.map(color => `<div class="color-badge ${color}" title="${color}"></div>`).join('')}
            </div>
            <div class="card-stats">
                <div class="card-stat">💰 Cost: ${card.cost}</div>
                ${card.power ? `<div class="card-stat">⚔️ Power: ${card.power}</div>` : ''}
            </div>
            ${card.effect ? `<div class="card-effect">${card.effect}</div>` : ''}
        </div>
    `).join('');
}

function handleFilterCards(event) {
    const filter = event.target.dataset.filter;
    
    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Filter cards
    if (currentDeck) {
        displayCards(currentDeck.main_deck, filter);
    }
}

// Authentication
function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentUser = data.user;
            showUserSection();
            closeAllModals();
            alert('Welcome back! ✨');
        } else {
            alert('Login failed: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Login failed');
    });
}

function handleRegister(event) {
    event.preventDefault();
    
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    
    fetch('/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentUser = data.user;
            showUserSection();
            closeAllModals();
            alert('Registration successful! Welcome to Lorcana! ✨');
        } else {
            alert('Registration failed: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Registration failed');
    });
}

function handleLogout() {
    fetch('/api/logout', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentUser = null;
            showAuthSection();
            alert('Logged out successfully');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Deck Management
function handleSaveDeck(event) {
    event.preventDefault();
    
    if (!currentDeck) {
        alert('No deck to save');
        return;
    }
    
    const name = document.getElementById('deck-name').value;
    
    const deckData = {
        name: name,
        strategy: currentDeck.strategy,
        color: currentDeck.color,
        main_deck: currentDeck.main_deck,
        game: 'lorcana'
    };
    
    fetch('/api/decks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(deckData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Deck saved successfully! ⭐');
            closeAllModals();
            document.getElementById('deck-name').value = '';
        } else {
            alert('Failed to save deck: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to save deck');
    });
}

function showMyDecks() {
    fetch('/api/decks')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayUserDecks(data.decks.filter(d => d.game === 'lorcana' || !d.game));
            showSection('user-decks-section');
        } else {
            alert('Failed to load decks');
        }
    })
    .catch(error => console.error('Error:', error));
}

function displayUserDecks(decks) {
    const decksList = document.getElementById('user-decks-list');
    
    if (decks.length === 0) {
        decksList.innerHTML = '<p>No saved decks yet. Build and save your first deck! ✨</p>';
        return;
    }
    
    decksList.innerHTML = decks.map(deck => `
        <div class="deck-item">
            <h3>${deck.name}</h3>
            <p>Strategy: ${deck.strategy} | Color: ${deck.color}</p>
            <p>Cards: ${deck.main_deck ? deck.main_deck.length : 0}</p>
            <div class="deck-item-actions">
                <button class="btn btn-small btn-primary" onclick="loadDeck(${deck.id})">Load</button>
                <button class="btn btn-small btn-secondary" onclick="deleteDeck(${deck.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

function loadDeck(deckId) {
    fetch(`/api/decks/${deckId}`)
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentDeck = data.deck;
            displayDeck(currentDeck);
            backToBuilder();
        } else {
            alert('Failed to load deck');
        }
    })
    .catch(error => console.error('Error:', error));
}

function deleteDeck(deckId) {
    if (!confirm('Are you sure you want to delete this deck?')) {
        return;
    }
    
    fetch(`/api/decks/${deckId}`, { method: 'DELETE' })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Deck deleted');
            showMyDecks();
        } else {
            alert('Failed to delete deck');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Collection Management
function showMyCollection() {
    fetch('/api/collection')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayCollection(data.collection);
            showSection('collection-section');
        } else {
            alert('Failed to load collection');
        }
    })
    .catch(error => console.error('Error:', error));
}

function displayCollection(collection) {
    const collectionList = document.getElementById('collection-list');
    
    if (collection.length === 0) {
        collectionList.innerHTML = '<p>Your collection is empty. Add some cards! ⭐</p>';
        return;
    }
    
    collectionList.innerHTML = collection.map(item => `
        <div class="collection-item">
            <h3>${item.card_name}</h3>
            <p>Quantity: ${item.quantity}</p>
            <div class="collection-item-actions">
                <button class="btn btn-small btn-secondary" onclick="removeFromCollection(${item.id})">Remove</button>
            </div>
        </div>
    `).join('');
}

function handleAddCard(event) {
    event.preventDefault();
    
    const cardName = document.getElementById('card-name').value;
    const quantity = parseInt(document.getElementById('card-quantity').value);
    
    fetch('/api/collection', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ card_name: cardName, quantity: quantity })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Card added to collection! ✨');
            closeAllModals();
            document.getElementById('card-name').value = '';
            document.getElementById('card-quantity').value = '1';
        } else {
            alert('Failed to add card: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to add card');
    });
}

function removeFromCollection(itemId) {
    fetch(`/api/collection/${itemId}`, { method: 'DELETE' })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Card removed from collection');
            showMyCollection();
        } else {
            alert('Failed to remove card');
        }
    })
    .catch(error => console.error('Error:', error));
}

function handleSuggestFromCollection() {
    const strategy = prompt('Enter strategy (balanced/aggressive/control):', 'balanced');
    const color1 = prompt('Enter first ink color (Amber/Amethyst/Emerald/Ruby/Sapphire/Steel):', 'Amber');
    const color2 = prompt('Enter second ink color (Amber/Amethyst/Emerald/Ruby/Sapphire/Steel):', 'Sapphire');
    
    if (!strategy || !color1 || !color2) return;
    
    if (color1 === color2) {
        alert('Please select two different ink colors');
        return;
    }
    
    fetch('/api/lorcana/suggest-deck', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ strategy, colors: [color1, color2] })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentDeck = data.deck;
            displayDeck(currentDeck);
            backToBuilder();
            
            if (data.deck.collection_info) {
                alert(`Deck built! You own ${data.deck.collection_info.percentage_owned}% of the cards. ✨`);
            }
        } else {
            alert('Failed to suggest deck: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to suggest deck');
    });
}

// Deck Analysis
function handleAnalyzeDeck() {
    if (!currentDeck) {
        alert('No deck to analyze');
        return;
    }
    
    fetch('/api/lorcana/analyze-deck', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ deck: currentDeck.main_deck })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayAnalysis(data.analysis);
            showSection('analysis-section');
        } else {
            alert('Failed to analyze deck');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to analyze deck');
    });
}

function displayAnalysis(analysis) {
    const analysisContent = document.getElementById('analysis-content');
    
    analysisContent.innerHTML = `
        <div class="analysis-content">
            <h3>Deck Overview</h3>
            <p><strong>Total Cards:</strong> ${analysis.total_cards}</p>
            <p><strong>Average Cost:</strong> ${analysis.average_cost}</p>
            
            <h3>Type Distribution</h3>
            ${Object.entries(analysis.type_distribution).map(([type, count]) => `
                <p>${type}: ${count} cards</p>
            `).join('')}
            
            <h3>Cost Distribution</h3>
            ${Object.entries(analysis.cost_distribution).map(([cost, count]) => `
                <p>Cost ${cost}: ${count} cards</p>
            `).join('')}
            
            <h3>Suggestions</h3>
            <ul>
                ${analysis.suggestions.map(s => `<li>${s}</li>`).join('')}
            </ul>
        </div>
    `;
}

// Deck Improvements
function handleSuggestImprovements() {
    if (!currentDeck) {
        alert('No deck to improve');
        return;
    }
    
    fetch('/api/lorcana/suggest-improvements', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ deck: currentDeck })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayImprovements(data.improvements);
            showSection('improvements-section');
        } else {
            alert('Failed to suggest improvements');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to suggest improvements');
    });
}

function displayImprovements(improvements) {
    const improvementsContent = document.getElementById('improvements-content');
    
    improvementsContent.innerHTML = Object.entries(improvements).map(([type, improvement]) => `
        <div class="improvement-option">
            <h3>${type.charAt(0).toUpperCase() + type.slice(1)} Deck</h3>
            <p>${improvement.description}</p>
            <p><strong>Cards:</strong> ${improvement.deck.main_deck.length}</p>
            ${improvement.deck.collection_coverage ? `
                <p><strong>Collection Coverage:</strong> ${improvement.deck.collection_coverage.percentage}%</p>
            ` : ''}
            <button class="btn btn-primary" onclick="adoptImprovement('${type}')">Use This Deck</button>
        </div>
    `).join('');
}

function adoptImprovement(type) {
    // Load the improved deck
    fetch('/api/lorcana/suggest-improvements', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ deck: currentDeck })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.improvements[type]) {
            currentDeck = data.improvements[type].deck;
            displayDeck(currentDeck);
            backToDeck();
            alert(`${type.charAt(0).toUpperCase() + type.slice(1)} deck loaded! ✨`);
        }
    })
    .catch(error => console.error('Error:', error));
}

// Export Deck
function handleExportDeck() {
    if (!currentDeck) {
        alert('No deck to export');
        return;
    }
    
    let exportText = `Disney Lorcana Deck - ${currentDeck.strategy} (${currentDeck.color})\n`;
    exportText += `${'='.repeat(50)}\n\n`;
    exportText += `Main Deck (${currentDeck.main_deck.length} cards):\n`;
    
    // Count cards
    const cardCounts = {};
    currentDeck.main_deck.forEach(card => {
        cardCounts[card.name] = (cardCounts[card.name] || 0) + 1;
    });
    
    // Sort and format
    Object.entries(cardCounts)
        .sort((a, b) => a[0].localeCompare(b[0]))
        .forEach(([name, count]) => {
            exportText += `${count}x ${name}\n`;
        });
    
    // Download as file
    const blob = new Blob([exportText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `lorcana-deck-${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
}

// UI Helpers
function showModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeAllModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.style.display = 'none';
    });
}

function showSection(sectionId) {
    // Hide all sections
    ['deck-display', 'user-decks-section', 'collection-section', 'analysis-section', 'improvements-section'].forEach(id => {
        document.getElementById(id).style.display = 'none';
    });
    
    // Show requested section
    document.getElementById(sectionId).style.display = 'block';
}

function backToBuilder() {
    showSection('deck-display');
    if (currentDeck) {
        displayDeck(currentDeck);
    }
}

function backToDeck() {
    showSection('deck-display');
}
