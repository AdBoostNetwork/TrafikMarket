import importlib
import pkgutil

from ai_assistant.logger import get_logger
from ai_assistant.tools import analytics, memory

logger = get_logger(__name__)

_PACKAGES = (analytics, memory)


def load_tools() -> None:
    """Импортирует модули инструментов — при импорте срабатывает @register и наполняет реестр."""
    count = 0
    for package in _PACKAGES:
        for module in pkgutil.iter_modules(package.__path__):
            importlib.import_module(f"{package.__name__}.{module.name}")
            count += 1
    logger.info("модули инструментов загружены | count=%s", count)
