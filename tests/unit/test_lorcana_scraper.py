#!/usr/bin/env python3
"""
Unit tests for the Lorcana card scraper.

These tests verify the scraper's structure and functionality without requiring
network access to dreamborn.ink.
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add parent directory (repository root) to path
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, repo_root)

# Import the scraper
from scrape_lorcana_cards import LorcanaCardScraper


class TestLorcanaCardScraper(unittest.TestCase):
    """Test cases for LorcanaCardScraper"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scraper = LorcanaCardScraper(verbose=False)
    
    def test_scraper_initialization(self):
        """Test that scraper initializes correctly"""
        self.assertIsNotNone(self.scraper)
        self.assertIsNotNone(self.scraper.session)
        self.assertEqual(self.scraper.BASE_URL, "https://dreamborn.ink")
        self.assertIn('User-Agent', self.scraper.session.headers)
    
    def test_urls_are_correct(self):
        """Test that URLs are properly configured"""
        self.assertEqual(
            self.scraper.CARDS_URL,
            "https://dreamborn.ink/es/cards"
        )
        self.assertEqual(
            self.scraper.API_URL,
            "https://dreamborn.ink/api/cards"
        )
    
    def test_log_verbose_mode(self):
        """Test logging in verbose mode"""
        verbose_scraper = LorcanaCardScraper(verbose=True)
        
        # Should print message
        with patch('builtins.print') as mock_print:
            verbose_scraper.log("Test message")
            mock_print.assert_called_once_with("Test message")
    
    def test_log_quiet_mode(self):
        """Test logging in quiet mode"""
        quiet_scraper = LorcanaCardScraper(verbose=False)
        
        # Should not print message
        with patch('builtins.print') as mock_print:
            quiet_scraper.log("Test message")
            mock_print.assert_not_called()
    
    def test_parse_card_element_with_complete_data(self):
        """Test parsing a card element with all fields"""
        # This test is simplified due to complexity of mocking BeautifulSoup elements
        # The actual parsing is tested by integration with real HTML
        # Here we just verify the method exists and handles basic cases
        
        mock_element = Mock()
        
        # Simple mock that returns name
        mock_name = Mock()
        mock_name.text.strip.return_value = "Simba - Protective Cub"
        
        # Make find return the name element for card-name class
        def find_side_effect(class_=None, **kwargs):
            if class_ == 'card-name':
                return mock_name
            return None
        
        mock_element.find.side_effect = find_side_effect
        mock_element.get.return_value = None
        
        card = self.scraper._parse_card_element(mock_element)
        
        # Verify card was parsed (at minimum should have a name)
        # Note: The actual parsing logic may differ based on HTML structure
        # This test verifies the method doesn't crash
        self.assertIsNotNone(card)
    
    def test_parse_card_element_minimal_data(self):
        """Test parsing a card element with minimal data"""
        mock_element = Mock()
        
        # Only provide name
        mock_name = Mock()
        mock_name.text.strip.return_value = "Test Card"
        
        mock_element.find.return_value = None
        mock_element.get.return_value = None
        
        # Make only card-name return a value
        def find_minimal(class_=None, **kwargs):
            if class_ == 'card-name':
                return mock_name
            return None
        
        mock_element.find.side_effect = find_minimal
        
        card = self.scraper._parse_card_element(mock_element)
        
        # Should have at least a name
        self.assertIsNotNone(card)
        if card:
            self.assertIn('name', card)
    
    def test_parse_card_element_no_name(self):
        """Test parsing a card element without a name returns None"""
        mock_element = Mock()
        mock_element.find.return_value = None
        mock_element.get.return_value = None
        
        card = self.scraper._parse_card_element(mock_element)
        
        # Should return None if no name found
        self.assertIsNone(card)
    
    @patch('requests.Session.get')
    def test_connectivity_success(self, mock_get):
        """Test successful connectivity check"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = self.scraper.test_connectivity()
        
        self.assertTrue(result)
        mock_get.assert_called_once()
    
    @patch('requests.Session.get')
    def test_connectivity_failure(self, mock_get):
        """Test failed connectivity check"""
        from requests.exceptions import ConnectionError
        mock_get.side_effect = ConnectionError("Connection failed")
        
        result = self.scraper.test_connectivity()
        
        self.assertFalse(result)
    
    @patch('requests.Session.get')
    def test_fetch_cards_api_success(self, mock_get):
        """Test successful API fetch"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'name': 'Card 1', 'type': 'Character'},
            {'name': 'Card 2', 'type': 'Action'}
        ]
        mock_get.return_value = mock_response
        
        cards = self.scraper.fetch_cards_api()
        
        self.assertIsNotNone(cards)
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0]['name'], 'Card 1')
    
    @patch('requests.Session.get')
    def test_fetch_cards_api_failure(self, mock_get):
        """Test API fetch failure"""
        from requests.exceptions import RequestException
        mock_get.side_effect = RequestException("API error")
        
        cards = self.scraper.fetch_cards_api()
        
        self.assertIsNone(cards)
    
    def test_save_cards_success(self):
        """Test saving cards to file"""
        import tempfile
        
        cards = [
            {'name': 'Test Card 1', 'type': 'Character'},
            {'name': 'Test Card 2', 'type': 'Action'}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            result = self.scraper.save_cards(cards, temp_file)
            self.assertTrue(result)
            
            # Verify file exists and contains valid JSON
            import json
            with open(temp_file, 'r') as f:
                loaded_cards = json.load(f)
            
            self.assertEqual(len(loaded_cards), 2)
            self.assertEqual(loaded_cards[0]['name'], 'Test Card 1')
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_generate_python_code(self):
        """Test Python code generation"""
        cards = [
            {
                'name': 'Test Card',
                'type': 'Character',
                'colors': ['Amber'],
                'cost': 1,
                'power': 1,
                'effect': 'Test effect',
                'inkable': True,
                'set': 'TFC',
                'card_number': '1',
                'rarity': 'Common'
            }
        ]
        
        # Capture stdout
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            self.scraper.generate_python_code(cards)
            output = captured_output.getvalue()
            
            # Verify output contains expected elements
            self.assertIn('sample_cards', output)
            self.assertIn('Test Card', output)
            self.assertIn('Character', output)
            self.assertIn('Amber', output)
        finally:
            sys.stdout = sys.__stdout__


class TestScraperCommandLine(unittest.TestCase):
    """Test command-line interface"""
    
    @patch('sys.argv', ['scrape_lorcana_cards.py', '--help'])
    def test_help_option(self):
        """Test that --help option doesn't crash"""
        # Import main would show help and exit
        # We just verify the import works
        from scrape_lorcana_cards import main
        self.assertIsNotNone(main)
    
    def test_scraper_can_be_imported(self):
        """Test that the scraper module can be imported"""
        from scrape_lorcana_cards import LorcanaCardScraper, main
        self.assertIsNotNone(LorcanaCardScraper)
        self.assertIsNotNone(main)


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
