from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles

from app.ats import calculate_ats_report
from app.config import load_config
from app.matcher import MatchResult
from app.repository import (
    AnalysisRecord,
    JobDescriptionRecord,
    get_analysis_result,
    list_analysis_results,
    list_job_descriptions,
    save_analysis_result,
    save_job_description,
    search_similar_jobs,
)
from app.schemas import (
    AnalysisDetailResponse,
    AnalysisHistoryItem,
    AnalyzeRequest,
    AnalyzeResponse,
    HealthResponse,
    JobDescriptionCreateRequest,
    JobDescriptionResponse,
    JobSearchRequest,
    ResumeUploadAnalyzeResponse,
)
from app.services import get_analyzer
from app.resume_documents import extract_text_from_upload, get_extension
from app.resume_rewriter import (
    build_rewrite_guidance,
    create_rewrite_docx,
    create_rewrite_txt,
    estimate_years_experience,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = PROJECT_ROOT / "app" / "static"

app = FastAPI(
    title="AI Job Match Assistant",
    description="Compare resumes against job descriptions and return skill-gap analysis.",
    version="0.1.0",
    openapi_tags=[
        {"name": "System", "description": "Health and local app entry points."},
        {"name": "Analysis", "description": "Resume and job description matching."},
        {"name": "Resume", "description": "Resume upload, ATS review, and rewrite draft workflows."},
        {"name": "History", "description": "Saved analysis history."},
        {"name": "Jobs", "description": "Stored job descriptions and local similarity search."},
    ],
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def web_app() -> HTMLResponse:
    return HTMLResponse((STATIC_DIR / "index.html").read_text(encoding="utf-8"))


def match_result_to_response(
    result: MatchResult, provider: str, record_id: int | None = None
) -> AnalyzeResponse:
    return AnalyzeResponse(
        id=record_id,
        score=result.score,
        readiness_level=result.readiness_level,
        resume_skills=result.resume_skills,
        job_skills=result.job_skills,
        matched_skills=result.matched_skills,
        missing_skills=result.missing_skills,
        missing_skills_by_category=result.missing_skills_by_category,
        suggestions=result.suggestions,
        learning_plan=result.learning_plan,
        provider=provider,
    )


def record_to_history_item(record: AnalysisRecord) -> AnalysisHistoryItem:
    return AnalysisHistoryItem(
        id=record.id,
        created_at=record.created_at,
        provider=record.provider,
        model_provider=record.model_provider,
        model_name=record.model_name,
        score=record.score,
        readiness_level=record.readiness_level,
    )


def record_to_detail_response(record: AnalysisRecord) -> AnalysisDetailResponse:
    return AnalysisDetailResponse(
        id=record.id,
        created_at=record.created_at,
        provider=record.provider,
        model_provider=record.model_provider,
        model_name=record.model_name,
        score=record.score,
        readiness_level=record.readiness_level,
        resume_text=record.resume_text,
        job_description_text=record.job_description_text,
        result=record.result,
    )


def job_record_to_response(record: JobDescriptionRecord) -> JobDescriptionResponse:
    return JobDescriptionResponse(
        id=record.id,
        created_at=record.created_at,
        title=record.title,
        company=record.company,
        description=record.description,
        similarity=record.similarity,
    )


@app.get("/health", response_model=HealthResponse, tags=["System"])
def health() -> HealthResponse:
    config = load_config()
    return HealthResponse(
        status="ok",
        app_env=config.app_env,
        model_provider=config.model_provider,
        model_name=config.model_name,
        has_openai_api_key=config.has_openai_api_key,
    )


@app.post("/analyze", response_model=AnalyzeResponse, tags=["Analysis"])
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    config = load_config()
    try:
        analyzer = get_analyzer(config)
        result = analyzer.analyze(
            resume_text=request.resume_text,
            job_description_text=request.job_description_text,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc

    record = save_analysis_result(
        resume_text=request.resume_text,
        job_description_text=request.job_description_text,
        result=result,
        provider=analyzer.provider_name,
        config=config,
    )

    return match_result_to_response(
        result, provider=analyzer.provider_name, record_id=record.id
    )


@app.post("/resume/analyze", response_model=ResumeUploadAnalyzeResponse, tags=["Resume"])
async def analyze_uploaded_resume(
    resume_file: UploadFile = File(...),
    job_description_text: str = Form(...),
) -> ResumeUploadAnalyzeResponse:
    content = await resume_file.read()
    resume_text = extract_text_from_upload(resume_file.filename or "resume", content)
    config = load_config()

    try:
        analyzer = get_analyzer(config)
        result = analyzer.analyze(resume_text, job_description_text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    record = save_analysis_result(
        resume_text=resume_text,
        job_description_text=job_description_text,
        result=result,
        provider=analyzer.provider_name,
        config=config,
    )
    ats = calculate_ats_report(resume_text, job_description_text)

    return ResumeUploadAnalyzeResponse(
        filename=resume_file.filename or "resume",
        years_experience_estimate=estimate_years_experience(resume_text),
        ats={
            "score": ats.score,
            "strengths": ats.strengths,
            "issues": ats.issues,
            "recommendations": ats.recommendations,
        },
        analysis=match_result_to_response(
            result, provider=analyzer.provider_name, record_id=record.id
        ),
        resume_preview=resume_text[:1200],
    )


@app.post("/resume/rewrite", tags=["Resume"])
async def rewrite_uploaded_resume(
    resume_file: UploadFile = File(...),
    job_description_text: str = Form(...),
) -> Response:
    content = await resume_file.read()
    filename = resume_file.filename or "resume.txt"
    extension = get_extension(filename)
    resume_text = extract_text_from_upload(filename, content)
    config = load_config()
    analyzer = get_analyzer(config)
    result = analyzer.analyze(resume_text, job_description_text)
    guidance = build_rewrite_guidance(resume_text, job_description_text, result)

    if extension == ".docx":
        rewritten = create_rewrite_docx(content, guidance)
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        output_filename = "targeted_resume_rewrite.docx"
    else:
        rewritten = create_rewrite_txt(resume_text, guidance)
        media_type = "text/plain"
        output_filename = "targeted_resume_rewrite.txt"

    return Response(
        content=rewritten,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{output_filename}"'},
    )


@app.get("/history", response_model=list[AnalysisHistoryItem], tags=["History"])
def history(limit: int = 10) -> list[AnalysisHistoryItem]:
    records = list_analysis_results(limit=limit)
    return [record_to_history_item(record) for record in records]


@app.get("/history/{record_id}", response_model=AnalysisDetailResponse, tags=["History"])
def history_detail(record_id: int) -> AnalysisDetailResponse:
    record = get_analysis_result(record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Analysis record not found.")
    return record_to_detail_response(record)


@app.post("/jobs", response_model=JobDescriptionResponse, tags=["Jobs"])
def create_job(request: JobDescriptionCreateRequest) -> JobDescriptionResponse:
    record = save_job_description(
        title=request.title,
        company=request.company,
        description=request.description,
    )
    return job_record_to_response(record)


@app.get("/jobs", response_model=list[JobDescriptionResponse], tags=["Jobs"])
def jobs(limit: int = 10) -> list[JobDescriptionResponse]:
    records = list_job_descriptions(limit=limit)
    return [job_record_to_response(record) for record in records]


@app.post("/jobs/search", response_model=list[JobDescriptionResponse], tags=["Jobs"])
def job_search(request: JobSearchRequest) -> list[JobDescriptionResponse]:
    records = search_similar_jobs(query_text=request.query_text, limit=request.limit)
    return [job_record_to_response(record) for record in records]
