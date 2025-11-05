#!/usr/bin/env python
"""
Test script for TCG selection landing page
Verifies that the new landing page and routing work correctly
"""
import sys
import os

# Add the project root directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from app import app

def test_tcg_selection_routes():
    """Test TCG selection landing page and routes"""
    print("=" * 60)
    print("TCG Selection Landing Page - Test Suite")
    print("=" * 60)
    
    # Set up test app context
    app.config['TESTING'] = True
    client = app.test_client()
    
    # Test 1: Landing page loads correctly
    print("\n" + "-" * 60)
    print("Test 1: Landing Page Route")
    print("-" * 60)
    response = client.get('/')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print(f"✓ Landing page loads successfully (status: {response.status_code})")
    
    # Check that the landing page content is present
    html = response.data.decode('utf-8')
    assert 'TCB Trading Card Brain' in html, "Landing page title not found"
    print(f"✓ Landing page title found")
    
    assert 'Select Your Trading Card Game' in html, "TCG selection heading not found"
    print(f"✓ TCG selection heading found")
    
    assert 'One Piece TCG' in html, "One Piece TCG card not found"
    print(f"✓ One Piece TCG card found")
    
    # Test 2: One Piece deck builder route
    print("\n" + "-" * 60)
    print("Test 2: One Piece Deck Builder Route")
    print("-" * 60)
    response = client.get('/onepiece')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print(f"✓ One Piece deck builder loads successfully (status: {response.status_code})")
    
    # Check that the deck builder content is present
    html = response.data.decode('utf-8')
    assert 'One Piece TCG Deck Builder' in html, "Deck builder title not found"
    print(f"✓ Deck builder title found")
    
    assert 'Build Your Deck' in html, "Build deck section not found"
    print(f"✓ Build deck section found")
    
    # Test 3: Verify landing page uses correct template
    print("\n" + "-" * 60)
    print("Test 3: Template Verification")
    print("-" * 60)
    response = client.get('/')
    html = response.data.decode('utf-8')
    assert 'landing.css' in html, "Landing page CSS not linked"
    print(f"✓ Landing page uses correct CSS (landing.css)")
    
    response = client.get('/onepiece')
    html = response.data.decode('utf-8')
    assert 'style.css' in html, "Deck builder CSS not linked"
    print(f"✓ Deck builder uses correct CSS (style.css)")
    
    print("\n" + "=" * 60)
    print("All Tests Passed! ✓")
    print("=" * 60)
    print("\nSummary:")
    print("✓ Landing page route working correctly")
    print("✓ One Piece deck builder route working correctly")
    print("✓ Correct templates and CSS being used")
    print("✓ All required content elements present")

if __name__ == '__main__':
    try:
        test_tcg_selection_routes()
        print("\n✅ All tests completed successfully!")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
