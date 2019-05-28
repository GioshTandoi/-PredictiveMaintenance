import pandas as pd
import numpy as np
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import matplotlib.pyplot as plt

#CONNECT
auth_provider = PlainTextAuthProvider(username='magazzini_automatici_esperto', password='esperto')
cluster = Cluster(["cassandra"], auth_provider = auth_provider)
session = cluster.connect()
session.set_keyspace('tenant_magazzini_automatici')
cluster.connect()
print("\n")
print("-----------------------CONNECTION-----------------")
print('Cluster contact points: \n'+str(cluster.contact_points))


#RETREIVE
rows = list(session.execute('select * from spread_icam_v1_events;'))
df = pd.DataFrame(rows)
print(df)
dates = df['date']
dates = pd.to_datetime(dates)
spread = pd.Series(data=df['spread'].values, index=dates)
spread.plot()
plt.show()