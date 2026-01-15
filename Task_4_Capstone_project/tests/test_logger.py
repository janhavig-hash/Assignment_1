import logging
from app.core.logger import get_logger

def test_get_logger_creation():
    """
    Test that the logger is created with correct settings.
    """
    # 1. Call the function
    logger_name = "test_module"
    logger = get_logger(logger_name)

    # 2. Assert it is a real Logger object
    assert isinstance(logger, logging.Logger)

    # 3. Assert the name matches exactly (Your code doesn't add prefixes)
    assert logger.name == logger_name

    # 4. Assert the default level is INFO
    assert logger.level == logging.INFO

    # 5. Assert it has a handler attached (The StreamHandler)
    assert len(logger.handlers) > 0
    assert isinstance(logger.handlers[0], logging.StreamHandler)