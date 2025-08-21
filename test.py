import yfinance as yf

ASIA = yf.Market("ASIA")

status = ASIA.status
summary = ASIA.summary

print(summary)

# # get historical market data
# # dat.history(period='1mo')
#
# # options
# dat.option_chain(dat.options[0]).calls
#
# # get financials
# dat.balance_sheet
# dat.quarterly_income_stmt
#
# # dates
# dat.calendar
#
# # general info
# dat.info
#
# # analysis
# dat.analyst_price_targets
#
# # websocket
# dat.live()