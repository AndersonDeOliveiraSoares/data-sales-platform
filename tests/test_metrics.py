from src.utils.metrics import PipelineMetrics


def test_pipeline_metrics_start_step():
    metrics = PipelineMetrics()

    start_time = metrics.start_step(
        "1/7 - Ingestion"
    )

    assert isinstance(start_time, float)
    assert start_time > 0


def test_pipeline_metrics_end_step():
    metrics = PipelineMetrics()

    start_time = metrics.start_step(
        "1/7 - Ingestion"
    )

    result = metrics.end_step(
        "1/7 - Ingestion",
        start_time,
    )

    assert result is None


def test_pipeline_metrics_finish():
    metrics = PipelineMetrics()

    result = metrics.finish()

    assert result is None


def test_pipeline_metrics_complete_execution():
    metrics = PipelineMetrics()

    start_time = metrics.start_step(
        "1/7 - Ingestion"
    )

    metrics.end_step(
        "1/7 - Ingestion",
        start_time,
    )

    start_time = metrics.start_step(
        "2/7 - Data Quality"
    )

    metrics.end_step(
        "2/7 - Data Quality",
        start_time,
    )

    result = metrics.finish()

    assert result is None