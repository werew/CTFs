import angr
import claripy

proj = angr.Project('./angrme')

flag_chars = [claripy.BVS('flag_%d' % i, 8) for i in range(50)]
flag = claripy.Concat(*flag_chars + [claripy.BVV(b'\n')])

st = proj.factory.full_init_state(
		args=['./angrme'],
		add_options=angr.options.unicorn,
		stdin=flag,
)

for k in flag_chars:
	st.solver.add(k != 0)

sm = proj.factory.simulation_manager(st)
sm.run()

out = b''
for pp in sm.deadended:
	inp = pp.posix.dumps(0)
	out = pp.posix.dumps(1)
	print(inp)
	print(out)
