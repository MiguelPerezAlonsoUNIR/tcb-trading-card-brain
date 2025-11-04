// One Piece TCG Deck Builder - Frontend JavaScript

// Constants
const LOADING_MESSAGES = {
    buildDeck: 'Building your deck',
    analyzeDeck: 'Analyzing your deck'
};

let currentDeck = null;

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
});

// Handle deck building
async function handleBuildDeck(e) {
    e.preventDefault();
    
    const strategy = document.getElementById('strategy').value;
    const color = document.getElementById('color').value;
    const leader = document.getElementById('leader').value;

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

    return `
        <div class="card" data-type="${card.type}">
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

        cardsHTML += `
            <div class="card" data-type="${card.type}">
                <div class="card-name">${card.name} ${count > 1 ? `(x${count})` : ''}</div>
                <div class="card-meta">
                    <span class="card-type">${card.type}</span>
                    <span class="card-cost">Cost: ${card.cost}</span>
                    ${powerHTML}
                </div>
                <div class="card-colors">${colorsHTML}</div>
                <div class="card-effect">${card.effect || ''}</div>
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
