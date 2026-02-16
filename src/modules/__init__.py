from .base import BaseModule
from .mihoyo.module import MihoyoModule

MODULES = {
    "mihoyo": MihoyoModule,
}


def get_module(name: str | None) -> BaseModule:
    """Get a module instance by name. Returns BaseModule if name is None."""
    if name is None:
        return BaseModule()

    if name not in MODULES:
        available = ", ".join(MODULES.keys())
        raise ValueError(f"Unknown module '{name}'. Available modules: {available}")

    return MODULES[name]()
