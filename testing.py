import pickle 

with open('customer_data/vikas.pkl', 'rb') as f:
    profile = pickle.load(f)

for key in profile:
    print(key)
print(type(profile))