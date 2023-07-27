from webull import webull  # for paper trading, import 'paper_webull'


email = 'rraithel@gmail.com'
password = 'GigiSofiaBeth27!@!@!'
wb = webull()

print(wb.get_mfa(email))
mfa_code = input("MFA code: ")
print(wb.get_security(email))
answer = input("Security Question Answer: ")
question_id = input("Question Id: ")
data = wb.login(email, password, 'PythonTest', mfa_code, question_id, answer)
print(wb.get_trade_token('489132'))
wb.place_order(stock='HLBZ', quant=1)  # price=90.0
orders = wb.get_current_orders()
print(orders)




# wb = webull()
# wb.login('rraithel@gmail.com', 'GigiSofiaBeth27!@!@!')
# wb.get_trade_token('489132')
#
# # order stock
# wb.place_order(stock='HLBZ', quant=1)  # price=90.0

# # check standing orders
# orders = wb.get_current_orders()
#
# # cancel standing orders
# wb.cancel_all_orders()
