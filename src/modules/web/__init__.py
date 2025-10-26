"""Web automation module.

Este módulo fornece classes e utilitários para automação web usando Selenium.
"""

from .driveroptions import DriverOptions
from .webdriver import Browser, WebDriver

__all__ = ["Browser", "WebDriver", "DriverOptions"]
