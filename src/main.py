"""
Composition Assistant - Main FastAPI Application
AI-powered music transformation and composition assistant
"""
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse, HTMLResponse, Response
import os
import time

from src.agents.agent import run_agent
from src.utils.metrics import metrics_collector, get_metrics_output
from src.utils.diagram_generator import generate_html_diagram
from src.core.config import (
    OLLAMA_HOST,
    OLLAMA_MODEL,
    SOUNDFONT_PATH,
    API_PORT,
    UI_PORT,
    LOG_LEVEL,
    get_config_summary,
    validate_config,
)
from src.clients.llm import check_ollama_connection

app = FastAPI(
    title="Composition Assistant API",
    description="AI-powered music transformation and composition assistant",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS so UI can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure folders exist
os.makedirs("tmp/input", exist_ok=True)
os.makedirs("tmp/output", exist_ok=True)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": "Composition Assistant",
        "version": "1.0.0"
    }


@app.get("/status")
async def status_check():
    """
    Detailed status check including Ollama connection.
    
    Returns:
        Detailed status of all components
    """
    ollama_status = check_ollama_connection()
    config_valid = validate_config()
    
    return {
        "status": "healthy" if ollama_status["connected"] else "degraded",
        "app": "Composition Assistant",
        "version": "1.0.0",
        "ollama": ollama_status,
        "config_valid": config_valid,
    }


@app.post("/process-wav/")
async def process_wav(
    request: Request,
    file: UploadFile = File(...),
    prompt: str = Form("")
):
    """
    Process a WAV audio file with AI-powered music transformation.
    
    Args:
        file: WAV audio file to process
        prompt: User's transformation goal/instructions
    
    Returns:
        Filename of the processed audio file
    """
    start_time = time.time()
    status_code = 200
    
    try:
        input_path = f"./tmp/input/{file.filename}"
        output_path = "./tmp/output/agent_output.wav"

        # Read and save uploaded file
        file_content = await file.read()
        file_size = len(file_content)
        
        with open(input_path, "wb") as f:
            f.write(file_content)

        # Record audio file metrics
        metrics_collector.record_audio_file(file_size, "success")

        # Run agent WITH prompt
        run_agent(input_path, prompt)

        # Record output file metrics
        if os.path.exists(output_path):
            output_size = os.path.getsize(output_path)
            metrics_collector.record_output_file("wav", output_size, "success")

        return {"filename": os.path.basename(output_path)}
    
    except Exception as e:
        status_code = 500
        metrics_collector.record_audio_file(0, "error")
        raise
    
    finally:
        duration = time.time() - start_time
        metrics_collector.record_api_request("/process-wav/", "POST", status_code, duration)


@app.get("/download/{filename}")
async def download_file(request: Request, filename: str):
    """
    Download a processed audio file.
    
    Args:
        filename: Name of the file to download
    
    Returns:
        The audio file as a download
    """
    start_time = time.time()
    status_code = 200
    
    try:
        path = f"./tmp/output/{filename}"
        if os.path.exists(path):
            return FileResponse(
                path,
                media_type="audio/wav",
                filename=filename
            )
        status_code = 404
        return {"error": "File not found"}
    
    finally:
        duration = time.time() - start_time
        metrics_collector.record_api_request("/download/", "GET", status_code, duration)


@app.get("/metrics", response_class=PlainTextResponse)
async def get_metrics() -> Response:
    """
    Get Prometheus-compatible metrics for the Composition Assistant.
    
    This endpoint exposes comprehensive metrics including:
    - Workflow execution counts and durations
    - Audio file processing metrics
    - Transcription operation metrics
    - LLM request metrics
    - MIDI conversion metrics
    - Output generation metrics
    - Error counts
    - Resource usage
    
    Returns:
        Prometheus-formatted metrics text
    """
    try:
        metrics_output = get_metrics_output()
        return Response(
            content=metrics_output,
            media_type="text/plain; version=0.0.4; charset=utf-8"
        )
    except Exception as e:
        return Response(
            content=f"# Error generating metrics: {str(e)}",
            media_type="text/plain",
            status_code=500
        )


@app.get("/workflow-diagram", response_class=HTMLResponse)
async def get_workflow_diagram() -> HTMLResponse:
    """
    Get an interactive HTML diagram of the workflow.
    
    Shows:
    - Complete audio processing pipeline
    - Transcription and conversion stages
    - LLM transformation process
    - Output generation flow
    
    Returns:
        Interactive HTML page with workflow diagram
    """
    try:
        html_content = generate_html_diagram()
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(
            content=f"<html><body><h1>Error generating diagram</h1><p>{str(e)}</p></body></html>",
            status_code=500
        )


@app.get("/config")
async def get_configuration():
    """
    Get current system configuration.
    
    Returns:
        System configuration information
    """
    return {
        "app_name": "Composition Assistant",
        "version": "1.0.0",
        "config": get_config_summary(),
        "endpoints": {
            "process_wav": "/process-wav/",
            "download": "/download/{filename}",
            "metrics": "/metrics",
            "workflow_diagram": "/workflow-diagram",
            "health": "/health",
            "status": "/status",
            "docs": "/docs"
        },
        "supported_transformations": [
            "Interval changes (transpose notes)",
            "Modal shifts (change scale)",
            "Rhythmic alterations (adjust timing)",
            "Register changes (octave shifts)"
        ],
    }


@app.get("/ollama/status")
async def get_ollama_status():
    """
    Check Ollama connection status and available models.
    
    Returns:
        Ollama connection status and model availability
    """
    return check_ollama_connection()
