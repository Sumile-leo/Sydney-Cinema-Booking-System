"""
Configuration Management for Sydney Cinema Booking System
Author: Zhou Li
Course: COMP9001
Date: October 19, 2025
"""

import configparser
import os
from typing import Dict, Any


class Config:
    """Configuration manager for the application"""
    
    def __init__(self, config_file: str = 'config.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        # Look for config.ini in the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(project_root, self.config_file)
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        self.config.read(config_path)
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration"""
        return {
            'host': self.config.get('database', 'host'),
            'port': self.config.getint('database', 'port'),
            'user': self.config.get('database', 'user'),
            'password': self.config.get('database', 'password'),
            'dbname': self.config.get('database', 'dbname')
        }
    
    def get_flask_config(self) -> Dict[str, Any]:
        """Get Flask configuration"""
        return {
            'host': self.config.get('flask', 'host'),
            'port': self.config.getint('flask', 'port'),
            'debug': self.config.getboolean('flask', 'debug'),
            'secret_key': self.config.get('flask', 'secret_key')
        }
    
    def get_app_config(self) -> Dict[str, Any]:
        """Get application configuration"""
        return {
            'name': self.config.get('app', 'name'),
            'author': self.config.get('app', 'author'),
            'course': self.config.get('app', 'course'),
            'version': self.config.get('app', 'version')
        }
    
    def get(self, section: str, key: str, fallback: Any = None) -> Any:
        """Get a specific configuration value"""
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback
    
    def getint(self, section: str, key: str, fallback: int = None) -> int:
        """Get a specific configuration value as integer"""
        try:
            return self.config.getint(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback
    
    def getboolean(self, section: str, key: str, fallback: bool = None) -> bool:
        """Get a specific configuration value as boolean"""
        try:
            return self.config.getboolean(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback


# Global configuration instance
config = Config()
