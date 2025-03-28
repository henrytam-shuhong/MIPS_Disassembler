


# extract bits from start to end (inclusive) from an instruction
def parse_bits(instruction, start, end):

    mask = (1 << (end - start + 1)) - 1
    return (instruction >> start) & mask

# convert a value to its two's complement representation
def twos_comp(val, bits=16):

    if val & (1 << (bits - 1)): #  checks if the most significant bit (MSB), also known as the sign bit, is set.
        return val - (1 << bits)
    return val


def main():

    # input
    instructions = [
        0x032BA020, 0x8CE90014, 0x12A90003, 0x022DA822, 0xADB30020, 0x02697824, 0xAE8FFFF4,
        0x018C6020, 0x02A4A825, 0x158FFFF7, 0x8ECDFFF0]


    current_address = 0x9A040  # start address

    for instruction in instructions:
        assy_instruction = f"{hex(current_address)} "
        opcode = parse_bits(instruction, 26, 31)

        if opcode == 0:  # R-format instruction
            src1 = parse_bits(instruction, 21, 25)
            src2 = parse_bits(instruction, 16, 20)
            dest = parse_bits(instruction, 11, 15)
            func = parse_bits(instruction, 0, 5)

            func_map = {32: "add", 34: "sub", 36: "and", 37: "or", 42: "slt"}

            assy_instruction += func_map.get(func, "ERROR NOT FOUND")
            assy_instruction += f" ${dest}, ${src1}, ${src2}"

        else:  # I-format instruction
            src1 = parse_bits(instruction, 21, 25)
            dest = parse_bits(instruction, 16, 20)
            offset = twos_comp(parse_bits(instruction, 0, 15))

            opcode_map = {4: "beq", 5: "bne", 35: "lw", 43: "sw"}

            assy_instruction += opcode_map.get(opcode, "ERROR NOT FOUND")

            if opcode in {35, 43}:  # lw/sw
                assy_instruction += f" ${dest}, {offset}(${src1})"
            elif opcode in {4, 5}:  # beq/bne
                target_address = current_address + 4 * (offset + 1)
                assy_instruction += f" ${src1}, ${dest}, address {hex(target_address)}"

        current_address += 4
        print(assy_instruction)


if __name__ == "__main__":
    main()
