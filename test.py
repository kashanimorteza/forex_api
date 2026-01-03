from logic.startup import config, load_forex_api, list_close
from logic.back import Logic_Back
logic = Logic_Back(execute_id=6)
logic.run()
# items= {"id":1, "action":"buy", "amount":10000, "price_open":1.16917, "ask":1.16927, "bid":1.16927}
# logic.order_close(item =items)
# items= {"id":2, "action":"sell", "amount":10000, "price_open":1.16903, "ask":1.16893, "bid":1.16893}
# logic.order_close(item =items)