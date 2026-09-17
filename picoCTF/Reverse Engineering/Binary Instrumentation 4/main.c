
int __cdecl main(int _Argc,char **_Argv,char **_Env)

{
  int iVar1;
  undefined8 uVar2;
  char *pcVar3;
  LPCSTR lpString2;
  LPCSTR lpString1;
  string local_498 [32];
  string local_478 [32];
  char local_458 [512];
  sockaddr local_258;
  WSADATA local_248;
  string local_a8 [32];
  string local_88 [48];
  int *local_58;
  int *local_50;
  undefined1 *local_48;
  int local_3c;
  SOCKET local_38;
  undefined4 local_2c;
  char *local_28;
  int *local_20;
  
  __main();
  local_28 = "192.168.29.25";
  local_2c = 0x268b;
  std::allocator<char>::allocator();
  std::__cxx11::string::string(local_88,"key68555664");
  std::allocator<char>::~allocator();
  std::allocator<char>::allocator();
  std::__cxx11::string::string(local_a8,"Enter the key:");
  std::allocator<char>::~allocator();
  local_38 = 0xffffffffffffffff;
  iVar1 = WSAStartup(0x202,&local_248);
  if (iVar1 == 0) {
    local_38 = socket(2,1,6);
    if (local_38 == 0xffffffffffffffff) {
      std::operator<<(&std::cerr,"Socket creation failed.\n");
      WSACleanup();
      iVar1 = 1;
    }
    else {
      local_258.sa_family = 2;
      local_258.sa_data._0_2_ = htons(0x268b);
      inet_pton(2,local_28,local_258.sa_data + 2);
      iVar1 = connect(local_38,&local_258,0x10);
      if (iVar1 == -1) {
        std::operator<<(&std::cerr,"Connection failed.\n");
        closesocket(local_38);
        WSACleanup();
        iVar1 = 1;
      }
      else {
        uVar2 = std::__cxx11::string::length(local_a8);
        pcVar3 = (char *)std::__cxx11::string::c_str(local_a8);
        send(local_38,pcVar3,(int)uVar2,0);
        local_3c = recv(local_38,local_458,0x1ff,0);
        if (local_3c < 1) {
          std::operator<<(&std::cerr,"No response from server.\n");
          closesocket(local_38);
          WSACleanup();
          iVar1 = 1;
        }
        else {
          local_458[local_3c + -1] = '\0';
          std::allocator<char>::allocator();
          std::__cxx11::string::string(local_478,local_458);
          std::allocator<char>::~allocator();
          lpString2 = (LPCSTR)std::__cxx11::string::c_str(local_88);
          lpString1 = (LPCSTR)std::__cxx11::string::c_str(local_478);
          iVar1 = lstrcmpA(lpString1,lpString2);
          if (iVar1 == 0) {
            std::allocator<char>::allocator();
            std::__cxx11::string::string(local_498,"Congratulations! Here\'s your flag:\n");
            std::allocator<char>::~allocator();
            local_48 = &flagParts;
            local_50 = &initialized;
            for (local_20 = (int *)&flagParts; local_20 != local_50; local_20 = local_20 + 8) {
              local_58 = local_20;
              std::__cxx11::string::operator+=(local_498,(undefined8 *)local_20);
            }
            uVar2 = std::__cxx11::string::length(local_498);
            pcVar3 = (char *)std::__cxx11::string::c_str(local_498);
            send(local_38,pcVar3,(int)uVar2,0);
            std::__cxx11::string::~string(local_498);
          }
          else {
            std::allocator<char>::allocator();
            std::__cxx11::string::string(local_498,"Wrong key");
            std::allocator<char>::~allocator();
            uVar2 = std::__cxx11::string::length(local_498);
            pcVar3 = (char *)std::__cxx11::string::c_str(local_498);
            send(local_38,pcVar3,(int)uVar2,0);
            std::__cxx11::string::~string(local_498);
          }
          closesocket(local_38);
          WSACleanup();
          iVar1 = 0;
          std::__cxx11::string::~string(local_478);
        }
      }
    }
  }
  else {
    std::operator<<(&std::cerr,"WSAStartup failed.\n");
    iVar1 = 1;
  }
  std::__cxx11::string::~string(local_a8);
  std::__cxx11::string::~string(local_88);
  return iVar1;
}

