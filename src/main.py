import asyncio
from viam.module.module import Module
try:
    from models.zone import Zone
except ModuleNotFoundError:
    # when running as local module with run.sh
    from .models.zone import Zone


if __name__ == '__main__':
    asyncio.run(Module.run_from_registry())
