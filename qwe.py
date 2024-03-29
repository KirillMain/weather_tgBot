w, r = map(int, input().split())
n = int(input())
t = list(map(int, input().split()))

# total_time = 0
# last_time = 0
# repeated = set()

# for i in range(n):
#     if w > t[i]:
#         total_time += t[i]
#         last_time = w - t[i]
#     else:
#         total_time += r
#         repeated.add(i)
#         last_time = w - (t[i] - w)
#     if last_time >= t[i]:
#         t[i] - last_time
#         total_time += t[i]
#         total_time += r
#         repeated.add(i)
# print(total_time)
# print(len(repeated))


res = 0
rep = 0
time = w

i = 0
while i<n:
    if time>0:
        res+=t[i]
        time-=t[i]
    elif time==0:
        res+=r
        time=w
        i -= 1
    elif time<0:
        i-=1
        res+=r
        time=w-t[i-1]
        res+=t[i-1]
        rep+=1
    i+=1

if time<0:
        res+=r
        time=w-t[i-1]
        res+=t[i-1]
        rep+=1

print(rep, res, sep='\n')

# 12 5
# 14
# 7 3 4 6 10 8 7 12 9 7 5 4 5 7
