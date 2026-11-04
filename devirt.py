"""Statically devirtualize Code Virtualizer VMs in an unpacked PE file.

Scan mode finds every jmp from the code section into the VM section,
devirtualizes it and patches the native code back in place:
    python2 devirt.py --vm TIGER --code-section 0 --vm-section 3 sample.exe -o sample.devirt.exe

Single mode devirtualizes the VM entry jmp at one address and prints the code
(add -o to also patch it in):
    python2 devirt.py --vm TIGER --address 0x401234 sample.exe
"""
import argparse
import os
import sys

import pefile

HERE = os.path.dirname(os.path.abspath(__file__))
# pyx86utils as built in place by x86utils/linux/build.sh, unless it is installed elsewhere
sys.path.append(os.path.join(os.environ.get("X86UTILS_DIR", os.path.join(HERE, "x86utils")), "python-cffi"))

import mappedfile
from vms import vmtools

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", help="unpacked PE file")
    parser.add_argument("-o", "--output", help="write the patched PE file here")
    parser.add_argument("--vm", choices=sorted(vmtools.VMS), required=True, help="VM type")
    parser.add_argument("--address", type=lambda x: int(x, 0), help="address of a jmp into the VM; devirtualize only this one")
    parser.add_argument("--code-section", type=int, default=0, help="index of the section to scan for VM entries (default: 0)")
    parser.add_argument("--vm-section", type=int, default=3, help="index of the section holding the VM (default: 3)")
    parser.add_argument("--small-macro", action="store_true", help="the VM entry macro is 6 bytes instead of 0x12")
    args = parser.parse_args()

    pe = pefile.PE(data=open(args.input, "rb").read(), fast_load=True)
    vm_type = vmtools.VMS[args.vm]
    big_macro = not args.small_macro

    if args.address is not None:
        file = mappedfile.PEMappedFile(pe)
        vm_type.decompile_vm(file, args.address, big_macro)
    else:
        vm_type.fix_vms(pe, args.code_section, args.vm_section, big_macro)

    if args.output:
        pe.write(filename=args.output)
        print "Wrote %s" % args.output


if __name__ == "__main__":
    main()
