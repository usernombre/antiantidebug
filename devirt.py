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


def list_sections(pe):
    for i, section in enumerate(pe.sections):
        start = pe.OPTIONAL_HEADER.ImageBase + section.VirtualAddress
        print "%2d %-8s 0x%08x-0x%08x raw=0x%08x entropy=%.2f" % (
            i, section.Name.rstrip("\0"), start, start + section.Misc_VirtualSize,
            section.SizeOfRawData, section.get_entropy())


def jump_target(file, address):
    mask = (1 << file.mode) - 1
    if file.read_byte(address) == 0xe9:
        return (file.read_format(address + 1, "<l") + address + 5) & mask
    if file.read_byte(address) == 0xeb:
        return (file.read_format(address + 1, "<b") + address + 2) & mask
    raise ValueError("No jmp at 0x%x" % address)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", help="unpacked PE file")
    parser.add_argument("-o", "--output", help="write the patched PE file here")
    parser.add_argument("--vm", choices=sorted(vmtools.VMS), help="VM type")
    parser.add_argument("--address", type=lambda x: int(x, 0), help="address of a jmp into the VM; devirtualize only this one")
    parser.add_argument("--code-section", type=int, default=0, help="index of the section to scan for VM entries (default: 0)")
    parser.add_argument("--vm-section", type=int, default=3, help="index of the section holding the VM (default: 3)")
    parser.add_argument("--small-macro", action="store_true", help="the VM entry macro is 6 bytes instead of 0x12")
    parser.add_argument("--list-sections", action="store_true", help="print the section indices and exit")
    args = parser.parse_args()

    pe = pefile.PE(data=open(args.input, "rb").read(), fast_load=True)
    if args.list_sections:
        list_sections(pe)
        return
    if args.vm is None:
        parser.error("--vm is required")
    vm_type = vmtools.VMS[args.vm]
    big_macro = not args.small_macro

    if args.address is not None:
        file = mappedfile.PEMappedFile(pe)
        if args.output:
            vm_type.decompile_vm(file, args.address, big_macro) # Prints the code and patches it in
        else:
            print vm_type.get_vm(file, jump_target(file, args.address)).get_code()
    else:
        vm_type.fix_vms(pe, args.code_section, args.vm_section, big_macro)

    if args.output:
        pe.write(filename=args.output)
        print "Wrote %s" % args.output


if __name__ == "__main__":
    main()
