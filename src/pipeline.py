from src.ingestion.postgres_to_parquet import run as run_ingestion
from src.quality.parquet_quality import run as run_quality
from src.transformation.raw_to_processed import run as run_transformation
from src.warehouse.dim_cliente import run as run_dim_cliente
from src.warehouse.dim_produto import run as run_dim_produto
from src.warehouse.dim_data import run as run_dim_data
from src.warehouse.fact_vendas import run as run_fact_vendas

from src.utils.logger import get_logger, setup_logging
from src.utils.metrics import PipelineMetrics


logger = get_logger("pipeline")


def run() -> None:

    setup_logging()

    metrics = PipelineMetrics()

    logger.info("Pipeline iniciado")

    try:

        step_start = metrics.start_step(
            "1/7 - Ingestion"
        )

        run_ingestion()

        metrics.end_step(
            "1/7 - Ingestion",
            step_start,
        )

        step_start = metrics.start_step(
            "2/7 - Data Quality"
        )

        run_quality()

        metrics.end_step(
            "2/7 - Data Quality",
            step_start,
        )

        step_start = metrics.start_step(
            "3/7 - Transformation"
        )

        run_transformation()

        metrics.end_step(
            "3/7 - Transformation",
            step_start,
        )

        step_start = metrics.start_step(
            "4/7 - Dimensão Cliente"
        )

        run_dim_cliente()

        metrics.end_step(
            "4/7 - Dimensão Cliente",
            step_start,
        )

        step_start = metrics.start_step(
            "5/7 - Dimensão Produto"
        )

        run_dim_produto()

        metrics.end_step(
            "5/7 - Dimensão Produto",
            step_start,
        )

        step_start = metrics.start_step(
            "6/7 - Dimensão Data"
        )

        run_dim_data()

        metrics.end_step(
            "6/7 - Dimensão Data",
            step_start,
        )

        step_start = metrics.start_step(
            "7/7 - Fact Vendas"
        )

        run_fact_vendas()

        metrics.end_step(
            "7/7 - Fact Vendas",
            step_start,
        )

        metrics.finish()

        logger.info(
            "Pipeline concluído com sucesso"
        )

    except Exception:

        logger.exception(
            "Pipeline falhou"
        )

        raise


if __name__ == "__main__":
    run()