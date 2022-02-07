from typing import List, Optional, Union

from pydantic import BaseModel


class BlackBEReturnDataFullInfo(BaseModel):
    area_code: str
    black_id: str
    info: str
    is_user: bool
    level: int
    name: str
    phone: str
    photos: List[str]
    qq: int
    server: str
    time: str
    uuid: str
    xuid: str


class BlackBEReturnDataInfo(BaseModel):
    uuid: Optional[str]
    name: Optional[str]
    black_id: Optional[str]
    xuid: Optional[str]
    info: Optional[str]
    level: Optional[int]
    qq: Optional[int]


class BlackBEReturnData(BaseModel):
    exist: bool
    info: List[Optional[BlackBEReturnDataInfo]]


class BlackBEReturn(BaseModel):
    success: bool
    status: int
    message: str
    version: str
    codename: str
    time: str
    data: Union[BlackBEReturnData, BlackBEReturnDataFullInfo, list[None]]
