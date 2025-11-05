# Templates (templates/)

This directory contains HTML templates for the web application. The application uses Flask's Jinja2 templating engine to render dynamic HTML pages.

## Directory Structure

```
templates/
├── index.html       # Main deck builder interface (One Piece TCG)
├── landing.html     # Landing page with TCG selection
└── onepiece.html    # One Piece TCG specific page
```

## Template Files

### landing.html
The landing page that users see when they first visit the application.

**Features**:
- Welcome message and application overview
- TCG selection grid (currently One Piece TCG)
- Clean, modern design
- Responsive layout

### onepiece.html
Dedicated page for One Piece Trading Card Game deck building.

**Features**:
- Strategy selection (Aggressive, Balanced, Control)
- Color picker
- Leader specification
- Deck building interface
- Links to deck builder functionality

### index.html
The main deck builder interface for One Piece TCG.

**Features**:
- User authentication UI (login/register)
- Deck building interface
- Deck display with card details
- Deck analysis panel
- Export functionality
- Collection management interface
- Combat simulation modal
- Deck improvement suggestions
- Interactive card filtering

## Templating Engine

The application uses **Jinja2**, Flask's default templating engine.

### Key Features Used:
- **Template inheritance**: `{% extends %}` for base layouts
- **Variables**: `{{ variable }}` for dynamic content
- **Control structures**: `{% if %}`, `{% for %}` for logic
- **Filters**: `{{ value|filter }}` for formatting
- **Static files**: `{{ url_for('static', filename='...') }}`

## Template Variables

Common variables passed to templates:

- `user`: Current authenticated user (if logged in)
- `deck`: Deck data including leader and main deck
- `cards`: List of available cards
- `strategies`: Available deck building strategies
- `colors`: Available card colors

## Development

When working with templates:

1. **Keep templates DRY**: Use template inheritance for shared layouts
2. **Separate concerns**: Keep business logic in Python, presentation in templates
3. **Use semantic HTML**: Proper HTML5 elements for accessibility
4. **Add comments**: Document complex template logic
5. **Test responsiveness**: Ensure templates work on all screen sizes

### Adding New Templates

When adding new templates:

1. Create the HTML file in `templates/`
2. Add a corresponding route in `app.py` or appropriate blueprint
3. Pass necessary data from the route to the template
4. Use Jinja2 syntax for dynamic content
5. Link to static assets using `url_for('static', filename='...')`

## Styling and Scripts

Templates reference static assets:

- **CSS**: `<link rel="stylesheet" href="{{ url_for('static', filename='css/...') }}">`
- **JavaScript**: `<script src="{{ url_for('static', filename='js/...') }}"></script>`

See [Static Assets Documentation](../static/README.md) for more information.

## Accessibility

Templates are designed with accessibility in mind:

- Semantic HTML elements
- Proper heading hierarchy
- ARIA labels where appropriate
- Keyboard navigation support
- Screen reader friendly

## Browser Compatibility

Templates are tested and compatible with:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Related Documentation

- [Main README](../README.md) - Application overview and features
- [Static Assets](../static/README.md) - CSS and JavaScript files
- [API Documentation](../docs/api/CARD_DATABASE.md) - Backend API endpoints
- [Architecture](../docs/architecture/ARCHITECTURE.md) - Application architecture

## Best Practices

When modifying templates:

1. **Test thoroughly**: Check all interactive features
2. **Validate HTML**: Use HTML validators to ensure proper structure
3. **Check responsive design**: Test on different screen sizes
4. **Maintain consistency**: Follow existing design patterns
5. **Document changes**: Add comments for complex template logic
