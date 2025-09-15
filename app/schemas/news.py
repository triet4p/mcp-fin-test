from typing import List
from pydantic import BaseModel, Field


class RelevantNewsPoint(BaseModel):
    news_uuid: str
    title: str
    summary: str|None = None
    provider: str|None = None
    link: str|None = None
    publish_ts: int|None = None
    collect_ts: int
    class Config:
        from_attributes = True
        
class RelevantNews(BaseModel):
    ticker: str = Field(..., description="Mã symbol của ticker")
    datas: List[RelevantNewsPoint] = Field(..., description='news')