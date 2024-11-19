from pydantic import BaseModel


class CourseQueryInput(BaseModel):
    text: str


class CourseQueryOutput(BaseModel):
    input: str
    output: str
    intermediate_steps: list[str]