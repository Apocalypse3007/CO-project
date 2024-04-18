import sys
import os
class Simulator(object):
    def __init__(self):
        self.registers = [['zero', 0], ['ra', 0], ['sp', 2**(8)], ['gp', 0], ['tp', 0], ['t0', 0], ['t1', 0], ['t2', 0], ['s0', 0], ['s1', 0], ['a0', 0], ['a1', 0], ['a2', 0], ['a3', 0], ['a4', 0], ['a5', 0], ['a6', 0], ['a7', 0], ['s2', 0], ['s3', 0], ['s4', 0], ['s5', 0], ['s6', 0], ['s7', 0], ['s8', 0], ['s9', 0], ['s10', 0], ['s11', 0], ['t3', 0], ['t4', 0], ['t5', 0], ['t6', 0]]
        self.program_counter = 0
        self.memory = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.instructions = [
            ["0000000","001","","rvrs","bonus"], ["0000000","011","","mul","bonus"], ["0110011","000","0000000","add","r"], ["0110011","000","0100000","sub","r"],
            ["0110011","001","","sll","r"],["0110011","010","","slt","r"],["0110011","011","","sltu","r"],["0110011","100","","xor","r"],
            ["0110011","101","","srl","r"],["0110011","110","","or","r"],["0110011","111","","and","r"],["0000011","","","lw","i"],
            ["0010011","000","","addi","i"],["0010011","011","","sltiu","i"],["1100111","","","jalr","i"],["0100011","","","sw","s"],
            ["1100011","000","","beq","b"],["1100011","001","","bne","b"],["1100011","100","","blt","b"],["1100011","101","","bge","b"],
            ["1100011","110","","bltu","b"],["1100011","111","","bgeu","b"],["0110111","","","lui","u"],["0010111","","","auipc","u"],
            ["1101111","","","jal","j"]
            ]
    
    def bin_to_int(self, binary):
        if binary[0] == "-":
            binary = binary[3:]
        elif binary[1] == "b":
            binary = binary[2:]
        if binary[0] == "1":
            return -(2**(len(binary)) - int(binary, 2))
        return int(binary, 2)
    def bin_to_unsigned(self, binary):
        return int(binary, 2)
    def binary_2s(self, m, bit=32):
        binary=''
        if (m<0):
            m=2**bit+m
        if (m==0):
            binary=binary+str(0)
        else:
            while (m!=0):
                r=m%2
                binary=str(r)+binary
                m=int(m/2)
        if(len(binary)==bit):
            return (binary)
        else:
            binary='0'*(bit-len(binary))+binary
            return binary
    def sign_extend(binary, size = 32, type_of_bit = "2s"):
        if type_of_bit == "unsigned":
            return "0"*(size-len(binary)) + binary
        elif type_of_bit in ("signed", "1s"):
            return binary[0]*(size-len(binary)) + binary
        elif type_of_bit == "2s":
            return binary[0]*(size-len(binary)) + binary
        return binary
    def binary_uns(self, m, bit = 32):
        binary=''
        if (m==0):
            binary=binary+str(0)
        else:
            while (m!=0):
                r=m%2
                binary=str(r)+binary
                m=int(m/2)
        return self.sign_extend(binary, bit, "unsigned")
    
    def Find_Instruction(self, line):
        if line == "00000000000000000000000001100011":
            return ["halt","bonus"]
        elif line=="00000000000000000000000000000000":
            return ["rvrs", "bonus"]
        opcode = line[25:]
        func3 = line[17:20]
        func7 = line[:7]
        for i in self.instructions:
            if i[0] == opcode:
                if i[1] == "":
                    return [i[3], i[4]]
                if i[1] == func3:
                    if i[2] == "":
                        return [i[3], i[4]]
                    if i[2] == func7:
                        return [i[3], i[4]]
        return ["Invalid Instruction", "Invalid Instruction"]
    
    def Find_Register(self, bin):
        return int(bin, 2)
    def readfile(self, file):
        with open(file, 'r') as file:
            instructions = file.read()
            file.close()
        return instructions
    def mem_hex(sefl, val):
        out = "0x0001"+ "0"*(4-len(hex(val*4)[2:]))+ hex(val*4)[2:]
        return out
    def memory_string(self):
        string = ""
        for i in range(len(self.memory)):
            string += str(self.mem_hex(i)) + ":" + str("0b" + self.binary_2s(self.memory[i],32)) + "\n"
        return string
    def outfile(self, string ,file = sys.argv[-1]):
        with open(file, 'w') as file:
            file.write(string)
            file.write(self.memory_string())
            file.close()
    def R_Type(self, line , instruction):
        rd = line[-12:-7]
        rs1 = line[-20:-15]
        rs2 = line[-25:-20]
        if instruction == "add":
            self.registers[self.Find_Register(rd)][1] = self.registers[self.Find_Register(rs1)][1] + self.registers[self.Find_Register(rs2)][1] #sext
        if instruction == "sub":
            self.registers[self.Find_Register(rd)][1] = self.registers[self.Find_Register(rs1)][1] - self.registers[self.Find_Register(rs2)][1]
        if instruction == "sll":
            value = self.registers[self.Find_Register(rs2)][1]
            if value < 0:
                binary_value = bin(value & 0xFFFFFFFF)[2:] 
            else:
                binary_value = bin(value)[2:].zfill(32)
            x = binary_value [-5:]
            y = int(x, 2)
            result = self.bin_to_int(self.binary_2s(self.registers[self.Find_Register(rs1)][1])[y:]+'0'*y)
            self.registers[self.Find_Register(rs1)][1] = result
        if instruction == "srl":
            value = self.registers[self.Find_Register(rs2)][1]
            if value < 0:
                binary_value = bin(value & 0xFFFFFFFF)[2:] 
            else:
                binary_value = bin(value)[2:].zfill(32)
            x = binary_value [-5:]
            y = int(x, 2)
            result = self.bin_to_int('0'*y+self.binary_2s(self.registers[self.Find_Register(rs1)][1])[:32-y])
            self.registers[self.Find_Register(rs1)][1] = result
        if instruction == "slt":
            if self.registers[self.Find_Register(rs1)][1] < self.registers[self.Find_Register(rs2)][1]: #sext
                self.registers[self.Find_Register(rd)][1] =1
        if instruction == "sltu":
            if self.binary_uns(self.registers[self.Find_Register(rs1)][1]) < self.binary_uns(self.registers[self.Find_Register(rs2)][1]):
                self.registers[self.Find_Register(rd)][1] =1
        if instruction == "xor" :
            self.registers[self.Find_Register(rd)][1] = self.registers[self.Find_Register(rs1)][1] ^ self.registers[self.Find_Register(rs2)][1]
        if instruction == "or" :
            self.registers[self.Find_Register(rd)][1] = self.registers[self.Find_Register(rs1)][1] | self.registers[self.Find_Register(rs2)][1]
        if instruction == "and" :
            self.registers[self.Find_Register(rd)][1] = self.registers[self.Find_Register(rs1)][1] & self.registers[self.Find_Register(rs2)][1]
        self.program_counter += 1
    def reverse(self, s):
        return s[::-1]
    def B_Type(self, line , instruction):
        rs2 = line[7:12]
        rs1 = line[12:17]
        immv1 = line[0:7]
        immv2 = line[20:25]
        imm = immv1+immv2
        imm = self.reverse(self.reverse(imm[0:12]) + "0")
        immval = int(self.bin_to_int(imm)/4)
        if (immval < -self.program_counter or immval > len(line)):
            imm = immv1+immv2
            imm = imm = self.reverse(self.reverse(imm[1:12]) + "1")
            immval = int(self.bin_to_int(imm)/4) - 1
            if (immval < -self.program_counter or immval > len(line)):
               immval = 1
        if instruction == "beq":
            if self.registers[self.Find_Register(rs1)][1] == self.registers[self.Find_Register(rs2)][1]:
                self.program_counter = self.program_counter + immval
            else:
                self.program_counter += 1
        if instruction == "bne":
            if self.registers[self.Find_Register(rs1)][1] != self.registers[self.Find_Register(rs2)][1]:
                self.program_counter = self.program_counter + immval
            else:
                self.program_counter += 1
        if instruction == "blt":
            if self.registers[self.Find_Register(rs1)][1] < self.registers[self.Find_Register(rs2)][1]:
                self.program_counter = self.program_counter + immval
            else:
                self.program_counter += 1
        if instruction == "bge":
            if self.registers[self.Find_Register(rs1)][1] >= self.registers[self.Find_Register(rs2)][1]:
                self.program_counter = self.program_counter + immval
            else:
                self.program_counter += 1
        if instruction == "bltu":
            if self.binary_uns(self.registers[self.Find_Register(rs1)][1]) < self.binary_uns(self.registers[self.Find_Register(rs2)][1]):
                self.program_counter = self.program_counter + immval
            else:
                self.program_counter += 1
        if instruction == "bgeu":
            if self.binary_uns(self.registers[self.Find_Register(rs1)][1]) >= self.binary_uns(self.registers[self.Find_Register(rs2)][1]):
                self.program_counter = self.program_counter + immval
            else:
                self.program_counter += 1
    def U_Type(self, line , instruction):
        rd = line[-12:-7]
        if instruction=="auipc":
            self.registers[self.Find_Register(rd)][1] = self.Find_Register(line[:-12]+'000000000000') + (self.program_counter)*4
        if instruction=="lui":
            self.registers[self.Find_Register(rd)][1] = self.Find_Register(line[:-12]+'000000000000')
        self.program_counter += 1
    def I_Type(self, line, instruction):
        imm = line[0:12]
        rs1 = line[12:17]
        rd = line[20:25]
        if instruction == "addi":
            self.registers[self.Find_Register(rd)][1] = self.registers[self.Find_Register(rs1)][1] + self.bin_to_int(imm)
            self.program_counter += 1
        elif instruction == "sltiu":
            if self.binary_uns(self.registers[self.Find_Register(rs1)][1]) < self.binary_uns(imm):
                self.registers[self.Find_Register(rd)][1] = 1
            else:
                self.registers[self.Find_Register(rd)][1] = 0
            self.program_counter += 1
        elif instruction == "lw":
            self.registers[self.Find_Register(rd)][1] = self.memory[int((((self.registers[self.Find_Register(rs1)][1]+self.bin_to_int(imm)))-65536)/4)]
            self.program_counter += 1
        elif instruction == "jalr":
            self.registers[self.Find_Register(rd)][1] = (self.program_counter+1)*4
            self.program_counter = int(self.registers[self.Find_Register(rs1)][1]/4) + int(self.bin_to_int(imm)/4)   
    def J_Type(self, line , instruction):
        rd = line[-12:-7]
        imm = self.reverse(str(line[1:11]))+str(line[11])+self.reverse(str(line[12:20]))+str(line[0])
        imm = self.reverse(imm)
        immval = int(self.bin_to_int(imm)/2)
        if instruction == "jal":
            self.registers[self.Find_Register(rd)][1] = (self.program_counter + 1)*4
            self.program_counter = self.program_counter + immval
    def S_Type(self, line , instruction):
        if instruction == "sw":
            rs2 = line[-25:-20]
            rs1 = line[-20:-15]
            imm = str(line[-32:-25])+str(line[-12:-7])
            self.memory[int((((self.registers[self.Find_Register(rs1)][1]+self.bin_to_int(imm)))-65536)/4)] = self.registers[self.Find_Register(rs2)][1]
            self.program_counter += 1
    def bonus(self, line, instruction):
        if instruction == "rst":
            for i in range(32):
                self.registers[i][1] = 0
            self.program_counter += 1
        if instruction == "halt":
            pass
        if instruction == "rvrs":
            rd = line[-12:-7]
            rs1 = line[-20:-15]
            self.registers[self.Find_Register(rd)][1] = self.bin_to_int(self.reverse(self.Find_Register(rs1)), 32)
            self.program_counter += 1
        if instruction == "mul":
            rs2 = line[7:12]
            rs1 = line[12:17]
            rd = line[20:25]
            if self.registers[self.Find_Register(rs1)][1]*self.registers[self.Find_Register(rs2)][1] < 2**(32):
                self.registers[self.Find_Register(rd)][1] = self.registers[self.Find_Register(rs1)][1]*self.registers[self.Find_Register(rs2)][1]
            self.program_counter += 1
    def regisout(self):
        out = ""
        for i in self.registers:
            out += f"0b{self.binary_2s(i[1])} "
        return out
    def output(self):
        out = ""
        for i in self.registers:
            out += f"{i[0]}: {i[1]}\n"
        return out
    def execute(self):
        outdata = ""
        line = self.readfile(sys.argv[-2])
        line=line.split("\n")
        self.program_counter = 0
        loop = 0
        while (self.program_counter <= len(line)):
            loop += 1
            if loop > 50:
                break
            self.program_counter = int(self.program_counter)
            i = self.program_counter
            i = int(i)
            print(self.Find_Instruction(line[i]))
            check_insta = self.Find_Instruction(line[int(i)])
            if check_insta[1]=='bonus':
                self.bonus(line[i],check_insta[0])
                if check_insta[0]=='rst':
                    pass
                elif check_insta[0]=='halt':
                    # print("0b" + decimal_to_binary(self.program_counter*4), end = " ")
                    self.registers[0][1] = 0
                    outdata += "0b" + self.binary_2s(self.program_counter*4) + " " + self.regisout() + "\n"
                    # print(output(registers))
                    break
            elif check_insta[1]=='r':
                self.R_Type(line[i],check_insta[0])
            elif check_insta[1]=='i':
                self.I_Type(line[i],check_insta[0])
            elif check_insta[1]=='s':
                self.S_Type(line[i],check_insta[0])
            elif check_insta[1]=='b':
                self.B_Type(line[i],check_insta[0])
            elif check_insta[1]=='u':
                self.U_Type(line[i],check_insta[0])
            elif check_insta[1]=='j':
                self.J_Type(line[i],check_insta[0])
            self.registers[0][1] = 0
            outdata += "0b" + self.binary_2s(self.program_counter*4) + " " + self.regisout() + "\n"
            # print(self.output())
        self.outfile(outdata)
    def execute1(self):
        outdata = ""
        # line = self.readfile(sys.argv[-2])
        # print(line)
        # line=line.split("\n")
        line = ""
        while (True):
            inp = input()
            if inp == "":
                break
            line += inp + "\n"
        line = line.split("\n")
        if line[-1] == "":
            line.pop(-1)
        self.program_counter = 0
        loop = 0
        while (self.program_counter <= len(line)):
            loop += 1
            if loop > 50:
                break
            self.program_counter = int(self.program_counter)
            i = self.program_counter
            i = int(i)
            check_insta = self.Find_Instruction(line[int(i)])
            print(check_insta)
            if check_insta[1]=='bonus':
                self.bonus(line[i],check_insta[0])
                if check_insta[0]=='rst':
                    pass
                elif check_insta[0]=='halt':
                    # print("0b" + decimal_to_binary(self.program_counter*4), end = " ")
                    self.registers[0][1] = 0
                    outdata += "0b" + self.binary_2s(self.program_counter*4) + " " + self.regisout() + "\n"
                    # print(output(registers))
                    break
            elif check_insta[1]=='r':
                self.R_Type(line[i],check_insta[0])
            elif check_insta[1]=='i':
                self.I_Type(line[i],check_insta[0])
            elif check_insta[1]=='s':
                self.S_Type(line[i],check_insta[0])
            elif check_insta[1]=='b':
                self.B_Type(line[i],check_insta[0])
            elif check_insta[1]=='u':
                self.U_Type(line[i],check_insta[0])
            elif check_insta[1]=='j':
                self.J_Type(line[i],check_insta[0])
            self.registers[0][1] = 0
            outdata += "0b" + self.binary_2s(self.program_counter*4) + " " + self.regisout() + "\n"
            # print(self.output())
        self.outfile(outdata, file = os.path.join(os.path.dirname(__file__) + "/output.txt"))
                    
if __name__ == "__main__":
    sim = Simulator()
    sim.execute()