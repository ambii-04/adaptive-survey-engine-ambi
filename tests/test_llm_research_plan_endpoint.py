from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.database import Base
from app.db.models import ResearchDimension, ResearchProject
from app.main import create_llm_research_plan
from app.schemas.llm_requests import LLMResearchPlanRequest
from app.schemas.research_plan import (
    Dimension_info,
    ResearchConstruct,
    ResearchHypothesis,
    ResearchPlan,
)


def test_llm_research_plan_loads_project_and_saves_plan_and_dimension_metrics(
    monkeypatch,
):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)

    project = ResearchProject(
        topic="Coffee preferences",
        target_audience="Coffee drinkers",
        geography="United States",
        dimensions=[
            ResearchDimension(
                name="Price",
                importance=0,
                target_coverage=0,
                achieved_coverage=0,
            )
        ],
    )
    plan = ResearchPlan(
        research_id=1,
        research_objectives=["Measure price sensitivity"],
        constructs=[
            ResearchConstruct(
                name="Price sensitivity",
                dimension="Price",
                measurement_method="Price-choice question",
            )
        ],
        hypotheses=[
            ResearchHypothesis(
                hypothesis_id="H1",
                statement="Price sensitivity varies by respondent.",
                dimension="Price",
            )
        ],
        dimension_info=[
            Dimension_info(
                dimension="Price",
                importance=8,
                target_coverage=0.75,
            )
        ],
    )

    def fake_generate_research_plan(**kwargs):
        assert kwargs == {
            "research_id": 1,
            "topic": "Coffee preferences",
            "target_audience": "Coffee drinkers",
            "geography": "United States",
            "dimensions": ["Price"],
        }
        return plan

    monkeypatch.setattr(
        "app.main.generate_research_plan_with_llm",
        fake_generate_research_plan,
    )

    with Session(engine) as db:
        db.add(project)
        db.commit()
        db.refresh(project)

        result = create_llm_research_plan(
            LLMResearchPlanRequest(research_id=project.id),
            db,
        )

        saved_project = db.get(ResearchProject, project.id)
        assert saved_project is not None
        assert saved_project.research_plan == plan.model_dump(mode="json")
        assert saved_project.dimensions[0].importance == 8
        assert saved_project.dimensions[0].target_coverage == 0.75
        assert result == plan.model_dump()
