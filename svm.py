#code:utf-8
import pandas_datareader.data as web
# import filoc_yahoo_finance as yf
import datetime
import matplotlib.pyplot as plt
from sklearn import svm
import copy
import tqdm
# yf.pdr_override()
start = datetime.datetime(1991,1,1)#获取数据的时间段-起始时间
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

plt.plot(stock['Close'], 'r', color='#FF0000')
plt.show()

paramsDim = 100
predictNum = 100
y = []
x = []
params = [0] * paramsDim
for j in range(1, paramsDim + 1):
	params[j - 1] = stock.iloc[j]['pct_change']

for i in range(paramsDim + 1, stock.shape[0] - predictNum):
	pct_change = stock.iloc[i]['pct_change']
	y.append(pct_change)
	x.append(copy.deepcopy(params))
	# print(params[-1])
	params[:-1] = params[1:]
	params[-1] = pct_change

clf = svm.SVR()
clf.fit(x, y)

predictNum = 10
result = []
for i in tqdm.tqdm(range(predictNum)):
	for j in range(paramsDim):
		params[j] = stock.iloc[stock.shape[0] - paramsDim + j - predictNum + 1 + i]['pct_change']
	# print(params[-1])
	result.append(clf.predict([params]))

plt.plot(stock.index[-predictNum:], result, linewidth = '1', label = "test", color='#00FF00', linestyle=':', marker='|')
plt.plot(stock[-predictNum:]['pct_change'], 'r', color='#FF0000')
plt.show()