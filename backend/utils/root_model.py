from typing import Dict, Any

from pydantic import ConfigDict, BaseModel


class RootModel(BaseModel):
    model_config = ConfigDict(extra="allow")
