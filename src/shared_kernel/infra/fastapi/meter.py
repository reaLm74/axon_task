from opentelemetry import metrics

meter = metrics.get_meter_provider().get_meter("Standard Metrics")
cubes_total = meter.create_counter("shift_service.cubes_total_amount")
products_total = meter.create_counter("shift_service.products_total_amount")
tasks_total = meter.create_counter("shift_service.tasks_total_amount")

products_aggregated = meter.create_counter("shift_service.products_aggregated")
cubes_aggregated = meter.create_counter("shift_service.cubes_aggregated")
close_task = meter.create_counter("shift_service.close_task")


def record_total(
        model_name: str,
) -> None:
    if model_name == "cubes":
        cubes_total.add(1)
    elif model_name == "products":
        products_total.add(1)
    else:
        tasks_total.add(1)


def record_aggregated(
        model_name: str,
) -> None:
    if model_name == "cubes":
        cubes_aggregated.add(1)
    else:
        products_aggregated.add(1)


def record_deaggregated(
        model_name: str,
) -> None:
    if model_name == "cubes":
        cubes_aggregated.add(-1)
    else:
        products_aggregated.add(-1)
