# Static Assets (static/)

This directory contains all static assets for the web application, including CSS stylesheets and JavaScript files.

## Directory Structure

```
static/
├── css/           # Stylesheets
│   └── ...       # CSS files for styling the application
└── js/            # JavaScript files
    └── ...       # Client-side JavaScript code
```

## CSS Files (`css/`)

Contains stylesheets that define the visual appearance of the application:

- **Layout styles**: Page structure, grid systems, responsive design
- **Component styles**: Buttons, forms, cards, modals
- **Theme**: Color schemes, typography, spacing
- **Responsive design**: Media queries for different screen sizes

## JavaScript Files (`js/`)

Contains client-side JavaScript code for interactive features:

- **API interactions**: Fetch data from backend endpoints
- **UI components**: Interactive elements (modals, dropdowns, etc.)
- **Form handling**: Validation and submission logic
- **Deck builder UI**: Interface for building and managing decks
- **Simulation UI**: Combat simulation interface
- **Collection management**: UI for managing card collections

## Key Features

### Deck Building Interface
- Strategy and color selection
- Leader specification
- Deck display with filtering
- Deck analysis visualization
- Export functionality

### Combat Simulation
- Opponent deck selection
- Simulation results display
- Win rate visualization
- Strategic insights

### Collection Management
- Add/remove cards from collection
- Track card quantities
- Deck suggestions based on collection

## Browser Compatibility

The static assets are tested and compatible with:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Development

When modifying static assets:

1. **CSS**: Follow existing class naming conventions
2. **JavaScript**: Use consistent code style and add comments for complex logic
3. **Testing**: Test in multiple browsers
4. **Performance**: Minimize file sizes, optimize images
5. **Accessibility**: Ensure keyboard navigation and screen reader support

## Related Documentation

- [Main README](../README.md) - Application overview and setup
- [Features Documentation](../docs/features/) - Feature-specific documentation
- [Testing Guide](../tests/TESTING.md) - How to test the application

## Asset Organization

Static assets should be organized by type (CSS, JS) and purpose. When adding new assets:

- Place stylesheets in `css/`
- Place JavaScript files in `js/`
- Use descriptive filenames
- Add comments to explain complex code
- Keep files modular and focused on specific functionality
