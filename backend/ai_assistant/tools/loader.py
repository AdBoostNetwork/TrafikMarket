import importlib
import pkgutil

from ai_assistant.logger import get_logger
from ai_assistant.tools import analytics

logger = get_logger(__name__)


def load_tools() -> None:
    """Импортирует модули инструментов — при импорте срабатывает @register и наполняет реестр."""
    count = 0
    for module in pkgutil.iter_modules(analytics.__path__):
        importlib.import_module(f"{analytics.__name__}.{module.name}")
        count += 1
    logger.info("модули инструментов загружены | analytics=%s", count)
