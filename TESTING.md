# Testing Guide for One Piece TCG Deck Builder

## Test Organization

Tests are now organized in the `tests/` directory by type:
- **`tests/unit/`** - Unit tests that don't require dependencies
- **`tests/system/`** - Integration/system tests that require Flask and database

See `tests/README.md` for detailed information about test organization.

## Quick Test (No Dependencies Required)

### Run All Tests with Helper Script

The easiest way to run all tests is using the test runner script:

```bash
bash run_tests.sh
```

This script will:
- Run all unit tests (no dependencies required)
- Run system tests if Flask is installed
- Display a summary of passed/failed tests

### Run Individual Tests

The core deck building logic can be tested without installing any dependencies:

```bash
python tests/unit/test_deck_builder.py
```

This will run a comprehensive test suite that verifies:
- Deck builder initialization
- Balanced, aggressive, and control strategies
- Color-based deck building
- Specific leader selection
- Deck analysis functionality
- Card copy limit enforcement

### Run all unit tests manually:
```bash
for test in tests/unit/test_*.py; do
    echo "Running $test..."
    python "$test"
done
```

## Full Application Testing (Requires Flask)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### 3. Test the Web Interface

1. **Build a Deck**:
   - Select a strategy (Balanced, Aggressive, or Control)
   - Choose a color (Red, Blue, Green, Purple, Black, Yellow, or Any)
   - Optionally specify a leader name
   - Click "Build Deck"

2. **View Deck Details**:
   - Check the leader card
   - Review deck statistics (total cards, average cost, type distribution)
   - Browse the main deck cards
   - Use filters to view specific card types

3. **Analyze Deck**:
   - Click "Analyze Deck" button
   - Review cost curve analysis
   - Check type and color distributions
   - Read AI-powered suggestions

4. **Export Deck**:
   - Click "Export Deck" button
   - Download the deck list as a text file

## Docker Testing

### Build and Run with Docker

```bash
# Build the image
docker build -t onepiece-deck-builder .

# Run the container
docker run -p 5000:5000 onepiece-deck-builder
```

### Using Docker Compose

```bash
# Start the application
docker-compose up

# Stop the application
docker-compose down
```

## API Testing

You can test the API endpoints directly using curl or tools like Postman:

### 1. Get All Cards

```bash
curl http://localhost:5000/api/cards
```

### 2. Build a Deck

```bash
curl -X POST http://localhost:5000/api/build-deck \
  -H "Content-Type: application/json" \
  -d '{
    "strategy": "balanced",
    "color": "Red",
    "leader": null
  }'
```

### 3. Analyze a Deck

```bash
curl -X POST http://localhost:5000/api/analyze-deck \
  -H "Content-Type: application/json" \
  -d '{
    "deck": [...]
  }'
```

## Expected Test Results

### Deck Building
- ✓ All decks should have exactly 50 cards in the main deck
- ✓ All decks should have 1 leader card
- ✓ No card should appear more than 4 times (except leaders)
- ✓ Cards should match the selected color when specified
- ✓ Deck composition should reflect the chosen strategy

### Strategy Verification

**Balanced Decks**:
- ~65% Characters
- ~30% Events
- ~5% Stages
- Varied cost curve

**Aggressive Decks**:
- ~70% Characters (low cost)
- ~30% Events
- Lower average cost (≤4)

**Control Decks**:
- ~60% Characters (high cost)
- ~40% Events
- Higher average cost (≥5)

### Analysis Results
- Cost curve should show distribution across all costs
- Type distribution should be accurate
- Color distribution should match deck composition
- Suggestions should be meaningful and actionable

## Troubleshooting

### Issue: "Module not found: flask"
**Solution**: Install dependencies with `pip install -r requirements.txt`

### Issue: "Port 5000 already in use"
**Solution**: Stop other services using port 5000 or change the port in `app.py`

### Issue: Deck has fewer than 50 cards
**Solution**: This can happen if there aren't enough unique cards for the selected color. The system will automatically fill with available cards.

### Issue: Docker build fails
**Solution**: Ensure Docker is running and you have internet connectivity for pulling base images and installing packages.

## Performance Benchmarks

Expected performance on a standard development machine:

- Deck building: < 1 second
- Deck analysis: < 0.5 seconds
- API response time: < 2 seconds
- Page load: < 1 second

## Browser Compatibility

The web interface has been tested and works on:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Known Limitations

1. **Card Database**: Currently contains 47 sample cards. Production version should include the full One Piece TCG card database.

2. **AI Suggestions**: Currently rule-based. Future versions could integrate machine learning models for more sophisticated analysis.

3. **Deck Validation**: Validates copy limits but doesn't check for official format rules (e.g., banned cards, restricted lists).

4. **Multi-player Features**: No deck sharing or community features in this version.

## Test Organization

All tests are now organized in the `tests/` directory:
- **Unit tests**: `tests/unit/` - No dependencies required
- **System tests**: `tests/system/` - Requires Flask and database setup

For more details, see `tests/README.md`.

## Next Steps for Testing

1. Add pytest integration for automated test discovery
2. Add end-to-end tests with Selenium
3. Add performance tests with locust
4. Add security tests (OWASP Top 10)
5. Add continuous integration pipeline
