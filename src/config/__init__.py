"""Configuration module"""
from .settings import Config, DevelopmentConfig, ProductionConfig, TestConfig, get_config

__all__ = ['Config', 'DevelopmentConfig', 'ProductionConfig', 'TestConfig', 'get_config']
