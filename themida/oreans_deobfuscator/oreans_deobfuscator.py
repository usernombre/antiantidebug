import os
import sys

from _oreans_deobfuscator import ffi, lib

REGISTERS = {    
    "AL": lib.UD_R_AL,
    "CL": lib.UD_R_CL,
    "DL": lib.UD_R_DL,
    "BL": lib.UD_R_BL,
    "AH": lib.UD_R_AH,
    "CH": lib.UD_R_CH,
    "DH": lib.UD_R_DH,
    "BH": lib.UD_R_BH,
    "SPL": lib.UD_R_SPL,
    "BPL": lib.UD_R_BPL,
    "SIL": lib.UD_R_SIL,
    "DIL": lib.UD_R_DIL,
    "R8B": lib.UD_R_R8B,
    "R9B": lib.UD_R_R9B,
    "R10B": lib.UD_R_R10B,
    "R11B": lib.UD_R_R11B,
    "R12B": lib.UD_R_R12B,
    "R13B": lib.UD_R_R13B,
    "R14B": lib.UD_R_R14B,
    "R15B": lib.UD_R_R15B,
    "AX": lib.UD_R_AX,
    "CX": lib.UD_R_CX,
    "DX": lib.UD_R_DX,
    "BX": lib.UD_R_BX,
    "SP": lib.UD_R_SP,
    "BP": lib.UD_R_BP,
    "SI": lib.UD_R_SI,
    "DI": lib.UD_R_DI,
    "R8W": lib.UD_R_R8W,
    "R9W": lib.UD_R_R9W,
    "R10W": lib.UD_R_R10W,
    "R11W": lib.UD_R_R11W,
    "R12W": lib.UD_R_R12W,
    "R13W": lib.UD_R_R13W,
    "R14W": lib.UD_R_R14W,
    "R15W": lib.UD_R_R15W,
    "EAX": lib.UD_R_EAX,
    "ECX": lib.UD_R_ECX,
    "EDX": lib.UD_R_EDX,
    "EBX": lib.UD_R_EBX,
    "ESP": lib.UD_R_ESP,
    "EBP": lib.UD_R_EBP,
    "ESI": lib.UD_R_ESI,
    "EDI": lib.UD_R_EDI,
    "R8D": lib.UD_R_R8D,
    "R9D": lib.UD_R_R9D,
    "R10D": lib.UD_R_R10D,
    "R11D": lib.UD_R_R11D,
    "R12D": lib.UD_R_R12D,
    "R13D": lib.UD_R_R13D,
    "R14D": lib.UD_R_R14D,
    "R15D": lib.UD_R_R15D,
    "RAX": lib.UD_R_RAX,
    "RCX": lib.UD_R_RCX,
    "RDX": lib.UD_R_RDX,
    "RBX": lib.UD_R_RBX,
    "RSP": lib.UD_R_RSP,
    "RBP": lib.UD_R_RBP,
    "RSI": lib.UD_R_RSI,
    "RDI": lib.UD_R_RDI,
    "R8": lib.UD_R_R8,
    "R9": lib.UD_R_R9,
    "R10": lib.UD_R_R10,
    "R11": lib.UD_R_R11,
    "R12": lib.UD_R_R12,
    "R13": lib.UD_R_R13,
    "R14": lib.UD_R_R14,
    "R15": lib.UD_R_R15,
    "ES": lib.UD_R_ES,
    "CS": lib.UD_R_CS,
    "SS": lib.UD_R_SS,
    "DS": lib.UD_R_DS,
    "FS": lib.UD_R_FS,
    "GS": lib.UD_R_GS,
    "CR0": lib.UD_R_CR0,
    "CR1": lib.UD_R_CR1,
    "CR2": lib.UD_R_CR2,
    "CR3": lib.UD_R_CR3,
    "CR4": lib.UD_R_CR4,
    "CR5": lib.UD_R_CR5,
    "CR6": lib.UD_R_CR6,
    "CR7": lib.UD_R_CR7,
    "CR8": lib.UD_R_CR8,
    "CR9": lib.UD_R_CR9,
    "CR10": lib.UD_R_CR10,
    "CR11": lib.UD_R_CR11,
    "CR12": lib.UD_R_CR12,
    "CR13": lib.UD_R_CR13,
    "CR14": lib.UD_R_CR14,
    "CR15": lib.UD_R_CR15,
    "DR0": lib.UD_R_DR0,
    "DR1": lib.UD_R_DR1,
    "DR2": lib.UD_R_DR2,
    "DR3": lib.UD_R_DR3,
    "DR4": lib.UD_R_DR4,
    "DR5": lib.UD_R_DR5,
    "DR6": lib.UD_R_DR6,
    "DR7": lib.UD_R_DR7,
    "DR8": lib.UD_R_DR8,
    "DR9": lib.UD_R_DR9,
    "DR10": lib.UD_R_DR10,
    "DR11": lib.UD_R_DR11,
    "DR12": lib.UD_R_DR12,
    "DR13": lib.UD_R_DR13,
    "DR14": lib.UD_R_DR14,
    "DR15": lib.UD_R_DR15,
    "MM0": lib.UD_R_MM0,
    "MM1": lib.UD_R_MM1,
    "MM2": lib.UD_R_MM2,
    "MM3": lib.UD_R_MM3,
    "MM4": lib.UD_R_MM4,
    "MM5": lib.UD_R_MM5,
    "MM6": lib.UD_R_MM6,
    "MM7": lib.UD_R_MM7,
    "ST0": lib.UD_R_ST0,
    "ST1": lib.UD_R_ST1,
    "ST2": lib.UD_R_ST2,
    "ST3": lib.UD_R_ST3,
    "ST4": lib.UD_R_ST4,
    "ST5": lib.UD_R_ST5,
    "ST6": lib.UD_R_ST6,
    "ST7": lib.UD_R_ST7,
    "XMM0": lib.UD_R_XMM0,
    "XMM1": lib.UD_R_XMM1,
    "XMM2": lib.UD_R_XMM2,
    "XMM3": lib.UD_R_XMM3,
    "XMM4": lib.UD_R_XMM4,
    "XMM5": lib.UD_R_XMM5,
    "XMM6": lib.UD_R_XMM6,
    "XMM7": lib.UD_R_XMM7,
    "XMM8": lib.UD_R_XMM8,
    "XMM9": lib.UD_R_XMM9,
    "XMM10": lib.UD_R_XMM10,
    "XMM11": lib.UD_R_XMM11,
    "XMM12": lib.UD_R_XMM12,
    "XMM13": lib.UD_R_XMM13,
    "XMM14": lib.UD_R_XMM14,
    "XMM15": lib.UD_R_XMM15,
    "RIP": lib.UD_R_RIP,
}

class Cleaner(object):
    def __init__(self, read, mode):
        self.read_func = read
        self.mode = mode
        self.fake_jumps = {}
        self.options = {}
        # Print every original instruction run next to the instruction it was reduced to (OREANS_TRACE=1)
        self.trace = bool(os.environ.get("OREANS_TRACE"))
        self.trace_file = sys.stderr

        @ffi.callback("int(void*, uint64_t, unsigned char*, size_t)")
        def _read(null, address, buffer, size):
            #print hex(address)
            try:
                data = self.read_func(address, size)
            except:
                return 0
            if len(data) < size:
                size = len(data)
            lib.memcpy(buffer, data, size)
            return size

        @ffi.callback("void(void*, uint64_t, unsigned char)")
        def _mark_fake_jump(null, address, jump_taken):
            self.fake_jumps[address] = jump_taken

        self.read_func_ref = _read
        self.mark_fake_jump_ref = _mark_fake_jump
        self.cleaner = lib.create_cleaner(_read, mode, ffi.NULL)
        if self.cleaner == ffi.NULL:
            raise MemoryError()
        if self.trace:
            # The jumps the cleaner resolved are needed to retrace the original path
            self.mark_fake_jumps()

    def set_reg_unused(self, reg):
        if reg.upper() in REGISTERS:
            lib.set_reg_unused(self.cleaner, REGISTERS[reg.upper()])
        else:
            raise ValueError("Invalid register %s" % reg)

    def set_option(self, option, value):
        self.options[option] = value
        lib.set_option(self.cleaner, option, value)

    def mark_fake_jumps(self):
        lib.mark_fake_jumps(self.cleaner, self.mark_fake_jump_ref)

    def get_clean_instruction(self, address):
        buffer = ffi.new("unsigned char [20]")
        output_size = ffi.new("size_t*", 20)
        next_address = lib.clean_instruction(self.cleaner, address, buffer, output_size)
        if next_address == 0:
            return None, ""
        data = ffi.buffer(buffer, output_size[0])[:]
        if self.trace:
            self._trace_clean(address, next_address, data)
        return (next_address, data)

    def _disassemble(self, address):
        import pyx86utils
        try:
            return pyx86utils.Instruction(self.read_func(address, 20), address, self.mode)
        except Exception:
            return None

    def _original_path(self, address, end_address, max_instructions=300):
        """Rebuild the original instructions the cleaner consumed going from address to end_address.

        The run isn't contiguous: jmps are followed and opaque conditional jumps are taken or skipped,
        so walk the original code depth first and return the first path that lands on end_address,
        as a list of (instruction, note) pairs.
        """
        # Defaults as in the Cleaner constructor (Cleaner.cpp)
        follow_top_jumps = self.options.get("ignore_jumps", True)
        follow_jumps = follow_top_jumps or self.options.get("ignore_nontop_jumps", False)
        follow_calls = self.options.get("ignore_calls", False)

        def successors(inst, top):
            if inst.opcode == "jmp" and inst.operands[0].is_immediate():
                if follow_top_jumps if top else follow_jumps:
                    return [(inst.operands[0].value, "followed")]
                return [(inst.next, None)]
            if inst.opcode == "call" and inst.operands[0].is_immediate() and follow_calls:
                return [(inst.operands[0].value, "followed")]
            if inst.opcode in ("ja", "jae", "jb", "jbe", "jz", "jg", "jge", "jl", "jle", "jnz", "jno", "jnp", "jns", "jo", "jp", "js") \
                    and inst.operands[0].is_immediate():
                # The cleaner marks the jump by the address right after it minus 6 (Cleaner::clearMovConstant)
                taken = self.fake_jumps.get(inst.next - 6)
                if taken is not None:
                    if taken:
                        return [(inst.operands[0].value, "taken")]
                    return [(inst.next, "not taken")]
                return [(inst.next, "not taken?"), (inst.operands[0].value, "taken?")]
            return [(inst.next, None)]

        def is_terminal(inst):
            # ret / jmp reg / jmp [mem]: the run can only end right after it
            return inst.opcode == "ret" or (inst.opcode == "jmp" and not inst.operands[0].is_immediate())

        def walk(current, path, visited):
            if current == end_address and path:
                return path
            if len(path) >= max_instructions or current in visited:
                return None
            inst = self._disassemble(current)
            if inst is None:
                return None
            if is_terminal(inst):
                if inst.next == end_address:
                    return path + [(inst, None)]
                return None
            for next_address, note in successors(inst, not path):
                res = walk(next_address, path + [(inst, note)], visited | set([current]))
                if res is not None:
                    return res
            return None

        return walk(address, [], set())

    def _trace_clean(self, address, next_address, data):
        import pyx86utils
        width = self.mode / 4
        out = self.trace_file
        try:
            cleaned = str(pyx86utils.Instruction(data, address, self.mode))
        except Exception:
            cleaned = "<%s>" % data.encode("hex")
        path = self._original_path(address, next_address)

        if path is not None and len(path) == 1 and str(path[0][0]) == cleaned:
            out.write("%0*x  %s\n" % (width, address, cleaned))
            return

        if path is None:
            out.write("%0*x  ? -> 1  (original path to %0*x not recovered)\n" % (width, address, width, next_address))
        else:
            out.write("%0*x  %d -> 1\n" % (width, address, len(path)))
            for inst, note in path:
                line = "    %0*x  %-24s %s" % (width, inst.address, self.read_func(inst.address, inst.size).encode("hex"), inst)
                if note:
                    line = "%-72s ; %s" % (line, note)
                out.write(line + "\n")
        out.write("    %s=> %s\n" % (" " * width, cleaned))

    def __del__(self):
        if self.cleaner != ffi.NULL:
            lib.destroy_cleaner(self.cleaner)
