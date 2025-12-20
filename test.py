from myLib.logic_global import config, load_forex_api, list_close
from myLib.logic_backtest import Logic_BackTest
logic = Logic_BackTest(execute_id=6)
logic.start()