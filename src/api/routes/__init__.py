"""API Routes"""
from flask import Flask
from .auth_routes import auth_bp
from .deck_routes import deck_bp
from .collection_routes import collection_bp
from .card_routes import card_bp
from .game_routes import game_bp


def register_blueprints(app: Flask):
    """Register all API blueprints"""
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(deck_bp, url_prefix='/api')
    app.register_blueprint(collection_bp, url_prefix='/api')
    app.register_blueprint(card_bp, url_prefix='/api')
    app.register_blueprint(game_bp, url_prefix='/api')


__all__ = ['register_blueprints']
