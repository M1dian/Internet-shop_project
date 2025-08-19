#!/usr/bin/env python
"""
Script to run tests for the shop project.
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def run_tests():
    """Run Django tests."""
    # Setup Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    # Run tests
    test_args = ['manage.py', 'test']
    
    # Add specific test apps if provided
    if len(sys.argv) > 1:
        test_args.extend(sys.argv[1:])
    else:
        # Run all tests by default
        test_args.extend(['app.users', 'app.products', 'app.cart', 'app.orders'])
    
    execute_from_command_line(test_args)

if __name__ == '__main__':
    run_tests() 