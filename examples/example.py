from stopverify import solve, prophet, verify_certificate, threshold_policy
from stopverify.audit import check_prophet_bound
D = [[(1,1)],[(0,'1/2'),(2,'1/2')]]
v = solve(D)
assert verify_certificate(D, v, threshold_policy(D,v))[0]
print('stopping',v[0],'prophet',prophet(D))
print(check_prophet_bound(D,'7/5'))
