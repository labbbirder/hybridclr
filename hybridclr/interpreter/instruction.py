import os
import re
import json

type_size = {
    "uint8_t":1,
    "uint16_t":2,
    "uint32_t":4,
    "int32_t":4,
    "uint64_t":8,
    "const char*":4,
}

def inport():
    instructs = []
    with open("instruction.h","r",encoding="utf-8") as f:
        content = f.read()
        for res in re.findall(r"//!!!{{INST(.*)//!!!}}INST",content,re.DOTALL):
            for klass,fields in re.findall(r"struct (.*?) : IRCommon\s*\{(.*?)\};",res,re.DOTALL):
                jklass =  {
                    "name":klass,
                    "fields":[]
                }
                instructs.append(jklass)
                for ftype,fname in re.findall(r"\s*([^\n;]*)\s+(.*?)\s*;",fields):
                    if not fname.startswith("__pad"):
                        jklass["fields"].append((ftype,fname))
                        _ = type_size[ftype]
    # for ins in instructs:
    with open("instr.txt","w",encoding="utf-8") as f:
        for ins in instructs:
            f.write(ins["name"]+":\n")
            for t,n in ins["fields"]:
                f.write(f"\t{t} {n}\n")
            f.write(";\n")

def export():
    with open("instr.txt","r",encoding="utf-8") as f:
        content = f.read()
        for klass,fields in re.findall(r"(\S+?):\n(.*?);",content,re.DOTALL):
            jklass =  {
                "name":klass,
                "fields":[]
            }
            # instructs.append(jklass)
            tsize = 0
            for ftype,fname in re.findall(r"\t([^\n;]*) (.+?)",fields):
                tsize += type_size[ftype]
            desized_size = ~-(-~tsize|7)
            print(f"{klass} {tsize} {desized_size}")

if __name__ == "__main__":
    os.chdir(__file__+"/..")
    export()