"""
Metrics collection for Composition Assistant using Prometheus.

Provides comprehensive metrics for audio processing and agent performance tracking.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import time
import asyncio
from functools import wraps
from contextlib import contextmanager

from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    Summary,
    Info,
    generate_latest,
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
)

# Create a custom registry for our metrics
REGISTRY = CollectorRegistry()

# =============================================================================
# System-wide Metrics
# =============================================================================

# Info metrics for system information
system_info = Info(
    'composition_assistant_info',
    'Composition Assistant system information',
    registry=REGISTRY
)

# Overall workflow metrics
workflow_total = Counter(
    'composition_assistant_workflow_total',
    'Total number of workflow executions',
    ['status'],
    registry=REGISTRY
)

workflow_duration = Histogram(
    'composition_assistant_workflow_duration_seconds',
    'Duration of complete workflow execution',
    buckets=(0.5, 1, 2, 5, 10, 30, 60, 120, 300),
    registry=REGISTRY
)

workflow_active = Gauge(
    'composition_assistant_workflow_active',
    'Number of currently active workflows',
    registry=REGISTRY
)

# API endpoint metrics
api_requests_total = Counter(
    'composition_assistant_api_requests_total',
    'Total number of API requests',
    ['endpoint', 'method', 'status_code'],
    registry=REGISTRY
)

api_request_duration = Histogram(
    'composition_assistant_api_request_duration_seconds',
    'Duration of API request processing',
    ['endpoint', 'method'],
    buckets=(0.01, 0.05, 0.1, 0.5, 1, 2.5, 5, 10, 30),
    registry=REGISTRY
)

# =============================================================================
# Audio Processing Metrics
# =============================================================================

audio_files_processed = Counter(
    'composition_assistant_audio_files_processed_total',
    'Total number of audio files processed',
    ['status'],
    registry=REGISTRY
)

audio_file_duration = Summary(
    'composition_assistant_audio_file_duration_seconds',
    'Duration of processed audio files in seconds',
    registry=REGISTRY
)

audio_file_size = Summary(
    'composition_assistant_audio_file_size_bytes',
    'Size of processed audio files in bytes',
    registry=REGISTRY
)

# =============================================================================
# Transcription Metrics
# =============================================================================

transcription_total = Counter(
    'composition_assistant_transcription_total',
    'Total number of transcription operations',
    ['status'],
    registry=REGISTRY
)

transcription_duration = Histogram(
    'composition_assistant_transcription_duration_seconds',
    'Duration of audio to MIDI transcription',
    buckets=(0.5, 1, 2, 5, 10, 30, 60, 120),
    registry=REGISTRY
)

notes_extracted = Summary(
    'composition_assistant_notes_extracted',
    'Number of notes extracted from audio',
    registry=REGISTRY
)

# =============================================================================
# LLM Agent Metrics
# =============================================================================

llm_requests_total = Counter(
    'composition_assistant_llm_requests_total',
    'Total number of LLM requests',
    ['model', 'status'],
    registry=REGISTRY
)

llm_request_duration = Histogram(
    'composition_assistant_llm_request_duration_seconds',
    'Duration of LLM requests',
    ['model'],
    buckets=(0.5, 1, 2, 5, 10, 30, 60, 120),
    registry=REGISTRY
)

llm_response_length = Summary(
    'composition_assistant_llm_response_length_chars',
    'Length of LLM responses in characters',
    registry=REGISTRY
)

# =============================================================================
# MIDI Processing Metrics
# =============================================================================

midi_conversion_total = Counter(
    'composition_assistant_midi_conversion_total',
    'Total number of MIDI conversion operations',
    ['direction', 'status'],  # direction: to_json, to_midi, to_wav
    registry=REGISTRY
)

midi_conversion_duration = Histogram(
    'composition_assistant_midi_conversion_duration_seconds',
    'Duration of MIDI conversion operations',
    ['direction'],
    buckets=(0.1, 0.5, 1, 2, 5, 10),
    registry=REGISTRY
)

notes_modified = Summary(
    'composition_assistant_notes_modified',
    'Number of notes modified by LLM',
    registry=REGISTRY
)

# =============================================================================
# Output Generation Metrics
# =============================================================================

output_generation_total = Counter(
    'composition_assistant_output_generation_total',
    'Total number of output file generations',
    ['format', 'status'],  # format: wav, midi
    registry=REGISTRY
)

output_file_size = Summary(
    'composition_assistant_output_file_size_bytes',
    'Size of generated output files in bytes',
    registry=REGISTRY
)

# =============================================================================
# Error Metrics
# =============================================================================

errors_total = Counter(
    'composition_assistant_errors_total',
    'Total number of errors',
    ['stage', 'error_type'],  # stage: transcription, llm, midi_conversion, output
    registry=REGISTRY
)

# =============================================================================
# Resource Metrics
# =============================================================================

memory_usage = Gauge(
    'composition_assistant_memory_usage_bytes',
    'Current memory usage in bytes',
    registry=REGISTRY
)

# =============================================================================
# Metric Collection Utilities
# =============================================================================

class MetricsCollector:
    """Singleton metrics collector for Composition Assistant."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.start_time = time.time()
        
        # Set system info
        system_info.info({
            'version': '1.0.0',
            'environment': 'production',
            'app_name': 'Composition Assistant'
        })
    
    @contextmanager
    def track_duration(self, histogram: Histogram, labels: Dict[str, str] = None):
        """Context manager to track duration of operations."""
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            if labels:
                histogram.labels(**labels).observe(duration)
            else:
                histogram.observe(duration)
    
    def track_workflow(self):
        """Decorator to track complete workflow execution."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                workflow_active.inc()
                status = "success"
                
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    status = "error"
                    errors_total.labels(stage="workflow", error_type=type(e).__name__).inc()
                    raise
                finally:
                    duration = time.time() - start_time
                    workflow_active.dec()
                    workflow_total.labels(status=status).inc()
                    workflow_duration.observe(duration)
            
            return wrapper
        return decorator
    
    def track_transcription(self):
        """Decorator to track transcription operations."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                status = "success"
                
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    status = "error"
                    errors_total.labels(stage="transcription", error_type=type(e).__name__).inc()
                    raise
                finally:
                    duration = time.time() - start_time
                    transcription_total.labels(status=status).inc()
                    transcription_duration.observe(duration)
            
            return wrapper
        return decorator
    
    def track_llm_request(self, model: str):
        """Decorator to track LLM request metrics."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                status = "success"
                
                try:
                    result = func(*args, **kwargs)
                    
                    # Track response length
                    if isinstance(result, str):
                        llm_response_length.observe(len(result))
                    
                    return result
                except Exception as e:
                    status = "error"
                    errors_total.labels(stage="llm", error_type=type(e).__name__).inc()
                    raise
                finally:
                    duration = time.time() - start_time
                    llm_requests_total.labels(model=model, status=status).inc()
                    llm_request_duration.labels(model=model).observe(duration)
            
            return wrapper
        return decorator
    
    def track_midi_conversion(self, direction: str):
        """Decorator to track MIDI conversion operations."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                status = "success"
                
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    status = "error"
                    errors_total.labels(stage="midi_conversion", error_type=type(e).__name__).inc()
                    raise
                finally:
                    duration = time.time() - start_time
                    midi_conversion_total.labels(direction=direction, status=status).inc()
                    midi_conversion_duration.labels(direction=direction).observe(duration)
            
            return wrapper
        return decorator
    
    def record_audio_file(self, file_size: int, status: str = "success"):
        """Record audio file processing metrics."""
        audio_files_processed.labels(status=status).inc()
        audio_file_size.observe(file_size)
    
    def record_notes_extracted(self, count: int):
        """Record number of notes extracted."""
        notes_extracted.observe(count)
    
    def record_notes_modified(self, count: int):
        """Record number of notes modified."""
        notes_modified.observe(count)
    
    def record_output_file(self, format: str, file_size: int, status: str = "success"):
        """Record output file generation metrics."""
        output_generation_total.labels(format=format, status=status).inc()
        output_file_size.observe(file_size)
    
    def record_api_request(self, endpoint: str, method: str, status_code: int, duration: float):
        """Record API request metrics."""
        api_requests_total.labels(
            endpoint=endpoint,
            method=method,
            status_code=str(status_code)
        ).inc()
        api_request_duration.labels(
            endpoint=endpoint,
            method=method
        ).observe(duration)
    
    def update_resource_metrics(self):
        """Update resource usage metrics."""
        try:
            import psutil
            process = psutil.Process()
            memory_usage.set(process.memory_info().rss)
        except ImportError:
            pass  # psutil not installed
    
    def get_metrics(self) -> bytes:
        """Generate Prometheus metrics output."""
        self.update_resource_metrics()
        return generate_latest(REGISTRY)


# Global metrics collector instance
metrics_collector = MetricsCollector()


def get_metrics_output() -> bytes:
    """Get current metrics in Prometheus format."""
    return metrics_collector.get_metrics()
