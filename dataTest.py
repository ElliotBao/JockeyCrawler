import pandas as pd

info = pd.read_csv('/Users/ZeyangBao/Desktop/w/info.csv')
#win = pd.read_csv('/Users/ZeyangBao/Desktop/winodds1.csv')
#qoddsvm = pd.read_csv('/Users/ZeyangBao/Desktop/qodds.csv')

q = pd.read_csv('/Users/ZeyangBao/Desktop/w/qodds.csv')

pq = pd.read_csv('/Users/ZeyangBao/Desktop/w/qpodds.csv')

x = info['race number'].unique()
y = q['Pair'].unique()
y2 = q['Pair2'].unique()
w = pq['Pair'].unique()


print len(w)
print'------'
for i in range(0, len(y)):
	if y[i]!= w[i]:
		print i
