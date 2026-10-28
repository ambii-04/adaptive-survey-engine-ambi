from pydantic import BaseModel, ConfigDict, Field


class LLMResearchPlanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    research_id: int = Field(gt=0)


class LLMSurveyRequest(BaseModel):
    research_id: int = Field(gt=0)
    topic: str = Field(min_length=3)
    dimensions: list[str] = Field(min_length=1)
    research_plan: dict
    target_audience: str = "Target respondents"
    geography: str = "Not specified"
    max_questions: int = Field(default=15, ge=2, le=50)