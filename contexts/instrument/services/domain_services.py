from ..models.instrument import Instrument








def filter_company_stocks(instruments_by_id)-> list[Instrument]:
    company_stocks = []

    for instr_id, instr in instruments_by_id.items():
        symbol = instr.symbol
        suffix = symbol.split("-")[-1] if "-" in symbol else None
        if suffix in (None, "BE", "SM", "ST", "BZ"):
            company_stocks.append(instr)
    return company_stocks
        










