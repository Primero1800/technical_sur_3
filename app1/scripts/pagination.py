from typing import Optional, Any, Sequence


async def paginate_result(
    query_list: Sequence[Any] | list[Any],
    page: Optional[int] = 1,
    size: Optional[int] = 10,
    sort_by: Optional[str] = None,
) -> Sequence | list[Any]:

    if sort_by:
        query_list = sorted(query_list, key=lambda x: x.get(sort_by, 0))

    start_index = (page - 1) * size
    end_index = start_index + size

    return query_list[start_index:end_index]