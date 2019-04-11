# pwnable.tw_seethefile
#file structure oriented programming 

sol: local에서 /dev/stdin 혹은 /dev/fd/0 을 이용!  
/dev/stdin 혹은 /dev/fd/0을 open하면 fread할 때 stdin으로 받는다.  
서버에서는 /dev/stdin 혹은 /dev/fd/0이 없어서 sol3으로 풀었다.  

sol2: 떠돌아 다니는 writeup (아직 이해못했음)  

sol3: 서버에서 /dev/stdin 혹은 /dev/fd/0이 안먹혀서 다른 방법으로 내가 한 풀이!  


fsop사용 

/proc/self/maps 파일을 통해 libc릭 및 힙주소 릭이 가능하다.  
5번 메뉴에서 name을 입력받는 부분에서 버퍼오버플로우가 나는데, fp를 덮을 수 있다.  
원래는 fp에 open한 file의버퍼포인터가 들어있는데 그 주소는 힙영역이다.   
그 주소로 가봤더니 조금 뒤에 IO_FILE_JUMPS라는 vtable이 있었다.  
IO_FILE_JUMPS에 안에는 여러개의 함수가 존재한다.  
이때, IO_file_close부분에 릭한 system함수의 주소를 넣어주면 쉘을 딸 수 있다.  
sh는 fake file structure구조 속에 넣는다.  

참고한 fsop내용-> https://s0ngsari.tistory.com/entry/File-Stream-Pointer%EC%97%90-%EA%B4%80%ED%95%9C-%EA%B8%80?category=553718
