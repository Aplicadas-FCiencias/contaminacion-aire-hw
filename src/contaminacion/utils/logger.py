"""
Módulo simple de logger para terminal.

Uso:
    from your_project.utils.logger import get_logger
    
    log = get_logger()
    log.info("Este es un mensaje informativo")
    log.error("Este es un mensaje de error")
    log.warning("Este es un mensaje de advertencia")
    log.debug("Este es un mensaje de depuración")
"""
import logging
import sys


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Obtiene una instancia de logger configurada.
    
    Args:
        name (str): Nombre del logger.
        level (str): Nivel de logging (por defecto: INFO)
    
    Returns:
        (logging.Logger) Instancia de logger configurada
    
    Ejemplos:
        >>> log = get_logger()
        >>> log.info("Procesamiento iniciado")
        
        >>> log = get_logger(__name__)
        >>> log.debug("Mensaje de depuración")  # No se mostrará por defecto
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(level)
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    return logger


def configure_logging(level: int = logging.INFO) -> None:
    """
    Configura el logger raíz globalmente.
    
    Args:
        level: Nivel de logging
    
    Ejemplo:
        >>> import logging
        >>> configure_logging(logging.DEBUG)  # Mostrar todos los mensajes
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
