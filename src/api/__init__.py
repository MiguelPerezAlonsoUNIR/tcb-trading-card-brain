"""API package"""
from flask import Flask
from .routes import register_blueprints

__all__ = ['register_blueprints']
