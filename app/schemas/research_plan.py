from pydantic import BaseModel


class ResearchConstruct(BaseModel):
    name: str
    dimension: str
    measurement_method: str


class ResearchHypothesis(BaseModel):
    hypothesis_id: str
    statement: str
    dimension: str

class Dimension_info(BaseModel):
    dimension: str
    importance: float
    target_coverage: float

class ResearchPlan(BaseModel):
    research_id: int
    research_objectives: list[str]
    constructs: list[ResearchConstruct]
    hypotheses: list[ResearchHypothesis]
    dimension_info: list[Dimension_info]
    
