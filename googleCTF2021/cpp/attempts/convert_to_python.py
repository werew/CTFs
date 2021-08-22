

def is_int(val):
    try:
        int(val)
        return True
    except:
        return False

def register_var(k, v, nv):

    if k not in nv:
        nv[k] = v
    return nv

with open("cpp.c") as f:
    nv = {}
    nl = []

    # Global defs
    gd = []
    gd.append("FLAG = [97]*27")
    gd.append("ROM = [0]*0x1000")


    # Global funs
    gf = []
    gf.append(
        "def LD(bit){\n" +
        "   addr = (l7 << 7) | (l6 << 6) | (l5 << 5) | (l4 << 4) | (l3 << 3) | (l2 << 2) | (l1 << 1) | l0\n" +
        "   return ROM[addr*8 + bit]\n" +
        "}"
    )
    gf.append(
        "void fail(const char* msg){\n" +
        "   printf(\"%s\\n\", msg);\n"
        "   exit(1);\n"
        "}"
    )

    for l in f:

        if l[0] != "#":
            continue

        l = l.split()
        if l[0] == "#define":
            # Skip some macro defs
            if ("MA" in l[1] or 
                "LD" in l[1] or
                l[1] == "l"):
                continue

            if "ROM" in l[1]:
                _, addr, bit = l[1].split("_")
                addr = int(addr, 2) * 8
                bit = int(bit)
                nl.append(f"ROM[{addr}+{bit}] = {l[2]};")

            elif len(l) == 2:
                nv = register_var(l[1], 0, nv);
                nl.append(f"{l[1]} = 1;")

            elif len(l) == 3:
                nv = register_var(l[1], 0, nv);
                nl.append(f"{l[1]} = {l[2]};")

            else:
                print(l)
                assert(False)

        elif l[0] == "#undef":
            assert(len(l) == 2)
            nv = register_var(l[1], 0, nv);
            nl.append(f"{l[1]} = 0;")

        elif l[0] == "#if":
            if "FLAG" in l[1]:
                _, addr = l[1].split("_")
                addr = int(addr)
                nl.append(f"if (FLAG[{addr}] {''.join(l[2:])}) {{")
            elif "LD" in l[1]:
                addr = l[2][0]
                nl.append(f"if (LD({addr})) {{")

            else:
                #nv = register_var(l[1], 0, nv);
                nl.append(f"if ({''.join(l[1:])}) {{")

        elif l[0] == "#ifdef":
            nv = register_var(l[1], 0, nv);
            nl.append(f"if ({l[1]} == 1) {{")

        elif l[0] == "#ifndef":
            nv = register_var(l[1], 0, nv);
            nl.append(f"if ({l[1]} == 0) {{")

        elif l[0] == "#else":
            nl.append("} else {")

        elif l[0] == "#endif":
            nl.append("}")

        elif l[0] == "#error":
            nl.append(f"fail({' '.join(l[1:])});")

        elif l[0] == "#include" and "cpp.c" in l[1]:
            nl.append(f"chall(INCLUDE_LEVEL+1);")

        else:
            print("// MISSED ", l)

    # add extra defs
    for k,v in nv.items():
        gd.append(f"char {k} = {v};")

    # dump file
    print("#include <stdio.h>")
    print("#include <stdlib.h>")
    print("/******************* Global defs ****************/")
    for l in gd:
        print(l)

    print("/******************* Functions ****************/")
    for l in gf:
        print(l)

    print("/******************* Chall ****************/")

    print("void chall(int INCLUDE_LEVEL){")
    for l in nl:
        print(l)
    print("}")

    print("/******************* Main ****************/")

    print("int main(){")
    print(" chall(0);")
    print(" return 0;")
    print("}")
