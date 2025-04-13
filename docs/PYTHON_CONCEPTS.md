# Python Concepts in NLP Data Pipeline

## Table of Contents
1. [Base Classes and Abstract Methods](#base-classes-and-abstract-methods)
2. [Async/Await Programming](#asyncawait-programming)
3. [Decorators](#decorators)
4. [Type Hints](#type-hints)
5. [Logging](#logging)
6. [Error Handling](#error-handling)
7. [Context Managers](#context-managers)
8. [Configuration Management](#configuration-management)

## Base Classes and Abstract Methods

### What is a Base Class?
A base class (or parent class) is a class that other classes can inherit from. It provides common functionality that child classes can use.

```python
# Example of a simple base class
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        raise NotImplementedError("Subclass must implement this method")

# Child class inheriting from base class
class Dog(Animal):
    def speak(self):
        return "Woof!"

# Usage
dog = Dog("Buddy")
print(dog.speak())  # Output: Woof!
```

### Abstract Base Classes (ABC)
Abstract Base Classes are classes that contain one or more abstract methods. They cannot be instantiated directly and must be subclassed.

```python
from abc import ABC, abstractmethod

class BaseCollector(ABC):
    @abstractmethod
    def collect_data(self):
        """This method MUST be implemented by child classes"""
        pass

class NewsCollector(BaseCollector):
    def collect_data(self):
        return "Collecting news data..."

# This will work
news_collector = NewsCollector()
print(news_collector.collect_data())

# This will raise an error
base_collector = BaseCollector()  # TypeError: Can't instantiate abstract class
```

## Async/Await Programming

### What is Async/Await?
Async/await is a way to write concurrent code in Python. It allows you to write code that can handle multiple tasks without blocking.

```python
import asyncio

# Regular function
def regular_function():
    print("Start")
    time.sleep(1)  # Blocks the program
    print("End")

# Async function
async def async_function():
    print("Start")
    await asyncio.sleep(1)  # Doesn't block
    print("End")

# How to run async code
async def main():
    await async_function()

asyncio.run(main())
```

### Async Context Managers
Context managers that work with async code.

```python
class AsyncCollector:
    async def __aenter__(self):
        print("Setting up resources")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Cleaning up resources")
    
    async def collect(self):
        print("Collecting data")

# Usage
async def main():
    async with AsyncCollector() as collector:
        await collector.collect()

asyncio.run(main())
```

## Decorators

### What are Decorators?
Decorators are functions that modify the behavior of other functions.

```python
# Simple decorator
def log_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time} seconds")
        return result
    return wrapper

# Using the decorator
@log_time
def slow_function():
    time.sleep(1)
    return "Done"

# This will print the execution time
result = slow_function()
```

### Property Decorators
Used to define getter and setter methods.

```python
class DataCollector:
    def __init__(self):
        self._data = None
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            raise ValueError("Data must be a dictionary")
        self._data = value

# Usage
collector = DataCollector()
collector.data = {"key": "value"}  # Uses setter
print(collector.data)  # Uses getter
```

## Type Hints

### What are Type Hints?
Type hints help document the expected types of variables and function parameters.

```python
from typing import List, Dict, Optional, Union

def process_data(data: List[Dict[str, Union[str, int]]]) -> Optional[Dict]:
    if not data:
        return None
    return data[0]

# Usage
result = process_data([{"name": "John", "age": 30}])
```

## Logging

### What is Logging?
Logging is a way to record information about your program's execution.

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a logger
logger = logging.getLogger(__name__)

# Log messages
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

## Error Handling

### Try-Except Blocks
Used to catch and handle exceptions.

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
else:
    print("No errors occurred")
finally:
    print("This always runs")
```

### Custom Exceptions
Creating your own exception types.

```python
class DataCollectionError(Exception):
    def __init__(self, message, source):
        self.message = message
        self.source = source
        super().__init__(f"{message} (Source: {source})")

# Usage
try:
    raise DataCollectionError("Failed to collect data", "NewsAPI")
except DataCollectionError as e:
    print(f"Error: {e}")
```

## Context Managers

### What are Context Managers?
Context managers handle the setup and teardown of resources.

```python
class FileHandler:
    def __init__(self, filename):
        self.filename = filename
    
    def __enter__(self):
        self.file = open(self.filename, 'r')
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

# Usage
with FileHandler('example.txt') as file:
    content = file.read()
```

## Configuration Management

### Using YAML for Configuration
YAML files for storing configuration settings.

```python
import yaml

# config.yaml
"""
database:
  host: localhost
  port: 5432
  user: admin
"""

# Loading configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

print(config['database']['host'])  # Output: localhost
```

### Environment Variables
Using environment variables for sensitive configuration.

```python
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access environment variables
api_key = os.getenv('API_KEY')
database_url = os.getenv('DATABASE_URL')
```

## Practice Exercises

### Exercise 1: Create a Base Class
```python
class DataProcessor(ABC):
    @abstractmethod
    def process(self, data):
        pass

class TextProcessor(DataProcessor):
    def process(self, data):
        return data.lower()

# Your task: Create a NumberProcessor class
```

### Exercise 2: Implement Async Code
```python
async def fetch_data(url):
    # Your task: Implement async data fetching
    pass

async def main():
    data = await fetch_data("https://api.example.com/data")
    print(data)
```

### Exercise 3: Create a Decorator
```python
def validate_input(func):
    # Your task: Create a decorator that validates function input
    pass

@validate_input
def process_data(data):
    return data * 2
```

### Exercise 4: Error Handling
```python
class DataValidator:
    def validate(self, data):
        # Your task: Implement validation with proper error handling
        pass
```

## Next Steps
1. Practice each concept with the provided examples
2. Try implementing the exercises
3. Read the Python documentation for each concept
4. Experiment with combining different concepts

Remember: The best way to learn is by doing. Try modifying the examples and see what happens! 