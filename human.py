#code:utf-8
import pandas_datareader.data as web
# import fix_yahoo_finance as yf
import datetime
import matplotlib.pyplot as plt

# yf.pdr_override()
start = datetime.datetime(2016,1,1)#获取数据的时间段-起始时间
end = datetime.date.today()#获取数据的时间段-结束时间
stock = web.DataReader("000001.SS", "yahoo", start, end)#获取浙大网新2017年1月1日至今的股票数据

print(stock.head(5))
print(stock.tail(5))
print(stock.index)
print(stock.columns)

# 增加涨跌幅度
change = stock.Close.diff()
stock['Change'] = change
print(stock.head(5))

stock['pct_change'] = 100.0 * (stock['Change'] / stock['Close'].shift(1))#

plt.plot(stock['Close'], 'r')
plt.show()

# 如果股票低于3000点，连续下跌三次开始购入，购入时长一星期且至少保本则开始出售
continuousFallNum = 0
isHold = False
boughtDate = 0
boughtPrice = 0
benifit = 0

details = {}

for i in range(1, stock.shape[0]):
	pct_change = stock.ix[i]['pct_change']
	if isHold:
		# 先判断时间是不是有七天
		dateDiff = stock.ix[i].name - boughtDate
		# 在判断差价是否为正
		priceDiff = stock.ix[i]['Close'] - boughtPrice
		if dateDiff.days >= 7 and stock.ix[i]['Close'] > boughtPrice:
			isHold = False # 卖掉咯
			# 假设每次投资10000
			benifit += priceDiff * 10000.0 / boughtPrice
			continuousFallNum = 0
			# 记录一下
			details[stock.ix[i].name] = [boughtDate, priceDiff * 10000.0 / boughtPrice, boughtPrice, stock.ix[i]['Close']]
	elif not isHold:
		if pct_change <= 0:
			continuousFallNum += 1
		if continuousFallNum >= 3 and stock.ix[i]['Close'] < 3000:
			isHold = True
			boughtDate = stock.ix[i].name
			boughtPrice = stock.ix[i]['Close']

print(benifit)