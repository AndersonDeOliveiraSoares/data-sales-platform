from time import perf_counter

from src.utils.logger import get_logger


logger = get_logger("metrics")


class PipelineMetrics:

    def __init__(self) -> None:
        self.start_time = perf_counter()

    def start_step(
        self,
        step_name: str,
    ) -> float:

        logger.info(
            "Etapa iniciada | step=%s",
            step_name,
        )

        return perf_counter()

    def end_step(
        self,
        step_name: str,
        start_time: float,
        records: int | None = None,
    ) -> None:

        duration = perf_counter() - start_time

        if records is not None:

            logger.info(
                "Etapa concluída | "
                "step=%s | "
                "records=%d | "
                "duration=%.2fs",
                step_name,
                records,
                duration,
            )

        else:

            logger.info(
                "Etapa concluída | "
                "step=%s | "
                "duration=%.2fs",
                step_name,
                duration,
            )

    def finish(self) -> None:

        duration = perf_counter() - self.start_time

        logger.info(
            "Pipeline finalizado | "
            "duration=%.2fs",
            duration,
        )