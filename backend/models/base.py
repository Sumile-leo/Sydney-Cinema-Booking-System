"""
Base Model Class for Sydney Cinema Booking System
Author: Zhou Li
Course: COMP9001
Date: October 13, 2025
"""

import psycopg
from psycopg import Error
from datetime import datetime
from typing import List, Optional, Dict, Any
import json
import os
import sys

# Add backend directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config


class BaseModel:
    """Base model class with common database operations"""
    
    # Database configuration from config file
    DB_CONFIG = config.get_database_config()
    
    @classmethod
    def get_connection(cls):
        """Get database connection"""
        try:
            return psycopg.connect(**cls.DB_CONFIG)
        except Error as e:
            print(f"Database connection error: {e}")
            return None
    
    @classmethod
    def execute_query(cls, query: str, params: tuple = None, fetch_one: bool = False, fetch_all: bool = False):
        """Execute database query"""
        connection = cls.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            else:
                result = cursor.rowcount
            
            connection.commit()
            return result
            
        except Error as e:
            print(f"Database query error: {e}")
            connection.rollback()
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            connection.close()
    
    @classmethod
    def get_by_id(cls, table_name: str, id_value: int, id_column: str = None):
        """Get record by ID"""
        if not id_column:
            id_column = f"{table_name[:-1]}_id"  # Remove 's' and add '_id'
        
        query = f"SELECT * FROM {table_name} WHERE {id_column} = %s"
        result = cls.execute_query(query, (id_value,), fetch_one=True)
        
        if result:
            return cls.from_db_row(result)
        return None
    
    @classmethod
    def get_all(cls, table_name: str, where_clause: str = None, params: tuple = None):
        """Get all records from table"""
        query = f"SELECT * FROM {table_name}"
        if where_clause:
            query += f" WHERE {where_clause}"
        
        results = cls.execute_query(query, params, fetch_all=True)
        if results:
            return [cls.from_db_row(row) for row in results]
        return []
    
    @classmethod
    def create(cls, table_name: str, data: Dict[str, Any]):
        """Create new record"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) RETURNING *"
        
        result = cls.execute_query(query, tuple(data.values()), fetch_one=True)
        if result:
            return cls.from_db_row(result)
        return None
    
    @classmethod
    def update(cls, table_name: str, id_value: int, data: Dict[str, Any], id_column: str = None):
        """Update record by ID"""
        if not id_column:
            id_column = f"{table_name[:-1]}_id"
        
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = %s RETURNING *"
        
        params = tuple(data.values()) + (id_value,)
        result = cls.execute_query(query, params, fetch_one=True)
        
        if result:
            return cls.from_db_row(result)
        return None
    
    @classmethod
    def delete(cls, table_name: str, id_value: int, id_column: str = None):
        """Delete record by ID"""
        if not id_column:
            id_column = f"{table_name[:-1]}_id"
        
        query = f"DELETE FROM {table_name} WHERE {id_column} = %s"
        return cls.execute_query(query, (id_value,))
    
    @classmethod
    def from_db_row(cls, row):
        """Convert database row to model instance - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement from_db_row method")
    
    def to_dict(self):
        """Convert model instance to dictionary"""
        return {key: value for key, value in self.__dict__.items() 
                if not key.startswith('_')}
    
    def to_json(self):
        """Convert model instance to JSON string"""
        def json_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
        return json.dumps(self.to_dict(), default=json_serializer, indent=2)
