from time import perf_counter

from src.utils.logger import get_logger


logger = get_logger("metrics")


class PipelineMetrics:

    def __init__(self) -> None:
        self.start_time = perf_counter()

    def start_step(self, step_name: str) -> float:
        logger.info(
            "Iniciando etapa: %s",
            step_name,
        )

        return perf_counter()

    def end_step(
        self,
        step_name: str,
        start_time: float,
    ) -> None:

        duration = perf_counter() - start_time

        logger.info(
            "Etapa concluída: %s | duração=%.2fs",
            step_name,
            duration,
        )

    def finish(self) -> None:

        duration = perf_counter() - self.start_time

        logger.info(
            "Pipeline finalizado | duração_total=%.2fs",
            duration,
        )