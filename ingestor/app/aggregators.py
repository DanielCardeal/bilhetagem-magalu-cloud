from dataclasses import asdict
from typing import Callable, Generator, Sequence
import pandas as pd

from app.data import PulseData, AggregateData


PulseAggregator = Callable[[Sequence[PulseData]], Generator[AggregateData, None, None]]
"""Tipo para funções agregadoras de pulso.

Args:
    pulses (Sequence[Pulse]): Sequência de pulsos a serem agregados.


Yield:
    PulseAggregate: Objeto contendo os dados agregados para cada combinação única de tenant, product_sku e use_unity.
"""


def pandas_pulse_aggregator(
    pulses: Sequence[PulseData],
) -> Generator[AggregateData, None, None]:
    """Agrega pulsos utilizando dataframes pandas para cálculo eficiente.

    Processa uma sequência de pulsos, agrupando por tenant, product_sku e use_unity,
    e calcula a soma das quantidades utilizadas (used_amount) para cada grupo.

    Args:
        pulses (Sequence[Pulse]): Sequência de pulsos a serem agregados.

    Yields:
        PulseAggregate: Objeto contendo os dados agregados para cada combinação única de tenant, product_sku e use_unity.
    """
    if len(pulses) == 0:
        return

    pulses_df = pd.DataFrame.from_records(asdict(p) for p in pulses)
    aggregate_sum_df = pulses_df.groupby(["tenant", "product_sku", "use_unity"])[
        "used_amount"
    ].sum()

    for (tenant, product_sku, use_unity), aggregate_amount in aggregate_sum_df.items():  # type: ignore
        yield AggregateData(
            tenant=tenant,
            product_sku=product_sku,
            use_unity=use_unity,
            aggregate_amount=aggregate_amount,  # type: ignore
        )
