// SPDX-License-Identifier: MIT
// DCS 2.9.29.27468 primary-cockpit connection. No weapon/flight binary is modified.
#include <windows.h>
#include <cstdint>
#include <cmath>
#include <bcrypt.h>
#include <string>
#include "supported.h"
struct lua_State;
using LuaFunction = int(*)(lua_State*);
static void* (*userData)(lua_State*, int);
static double (*number)(lua_State*, int);
static void (*pushNumber)(lua_State*, double);
static void (*pushFunction)(lua_State*, LuaFunction, int);
template<class T> T field(void* p, size_t offset) {
    return *reinterpret_cast<T*>(static_cast<char*>(p) + offset);
}
template<class T> T method(void* p, size_t offset) {
    return field<T>(*static_cast<void**>(p), offset);
}
// Check exact on-disk module versions once, before accessing version-specific layouts.
static bool matches(const wchar_t* name, const char* expected) {
    auto module = GetModuleHandleW(name);
    wchar_t path[32768]{};
    if (!module || !GetModuleFileNameW(module, path, 32768)) return false;
    HANDLE file = CreateFileW(path, GENERIC_READ, FILE_SHARE_READ, nullptr, OPEN_EXISTING, 0, nullptr);
    if (file == INVALID_HANDLE_VALUE) return false;
    BCRYPT_ALG_HANDLE algorithm{};
    BCRYPT_HASH_HANDLE hash{};
    bool ok = BCryptOpenAlgorithmProvider(&algorithm, BCRYPT_SHA256_ALGORITHM, nullptr, 0) >= 0;
    if (ok) ok = BCryptCreateHash(algorithm, &hash, nullptr, 0, nullptr, 0, 0) >= 0;
    unsigned char buffer[65536], digest[32]{};
    DWORD size{};
    while (ok) {
        if (!ReadFile(file, buffer, sizeof(buffer), &size, nullptr)) { ok = false; break; }
        if (!size) break;
        ok = BCryptHashData(hash, buffer, size, 0) >= 0;
    }
    if (ok) ok = BCryptFinishHash(hash, digest, sizeof(digest), 0) >= 0;
    if (hash) BCryptDestroyHash(hash);
    if (algorithm) BCryptCloseAlgorithmProvider(algorithm, 0);
    CloseHandle(file);
    std::string hex;
    for (auto byte : digest) { hex += "0123456789abcdef"[byte >> 4]; hex += "0123456789abcdef"[byte & 15]; }
    return ok && hex == expected;
}
static int prepare(lua_State* L) {
    auto link = static_cast<char*>(userData(L,1));
    auto module = GetModuleHandleW(L"CockpitBase.dll");
    if (!link || !module) { pushNumber(L,0); return 1; }
    const double requested = number(L,2);
    if (requested < 0 || requested > 8 || requested != std::floor(requested)) { pushNumber(L,-6); return 1; }
    auto device = link - 0x20;
    auto expected = GetProcAddress(module,"??_7avSimpleWeaponSystem@cockpit@@6BccContextRelatedObject@1@@");
    if (*reinterpret_cast<void**>(device) != reinterpret_cast<void*>(expected)) {
        pushNumber(L,-1); return 1;
    }
    auto seeker = field<void*>(device,0x158);
    auto context = field<void*>(device,0x18);
    if (!context) { pushNumber(L,-7); return 1; }
    auto human = field<void*>(context,0x10);
    if (!human) { pushNumber(L,-7); return 1; }
    auto armament = method<void*(*)(void*)>(human,0x120)(human);
    if (!armament) { pushNumber(L,-3); return 1; }
    auto type = method<const uint64_t*(*)(void*,int)>(armament,0xa0)(armament,int(number(L,2)));
    if (!type) { pushNumber(L,-5); return 1; }
    auto setType = reinterpret_cast<void(*)(void*,const uint64_t&)>(GetProcAddress(module,
        "?setParentType@avSidewinderSeeker@cockpit@@QEAAXAEBVwsType@@@Z"));
    if (!setType) { pushNumber(L,-4); return 1; }
    // Radar stores do not create an IR seeker. Target handoff is independent
    // of that optional device; an IR seeker initializes after station selection.
    if (seeker) setType(seeker,*type);
    pushNumber(L,double(*type));
    auto responder=field<void*>(context,0x100);
    auto target=responder ? method<unsigned(*)(void*)>(responder,0x10)(responder) : 0;
    pushNumber(L,target);
    auto objects=GetModuleHandleW(L"edObjects.dll");
    auto construct=reinterpret_cast<void*(*)(void*,unsigned)>(GetProcAddress(objects,"??0SceneObject@@QEAA@I@Z"));
    auto destroy=reinterpret_cast<void(*)(void*)>(GetProcAddress(objects,"??1SceneObject@@UEAA@XZ"));
    auto valid=reinterpret_cast<bool(*)(const void*)>(GetProcAddress(objects,"??BSceneObject@@QEBA_NXZ"));
    auto position=reinterpret_cast<double*(*)(const void*,double*)>(GetProcAddress(objects,"?getObjectPosition@SceneObject@@UEBA?AVMatrixd@osg@@XZ"));
    if (!target || !construct || !destroy || !valid || !position) return 2;
    alignas(16) unsigned char object[64]{};
    construct(object,target);
    if (!valid(object)) { destroy(object);return 2; }
    double matrix[16]{};
    position(object,matrix);
    destroy(object);
    // slaveToDirection already converts from aircraft to the mounting frame.
    // Supply aircraft-relative angles, without applying that rotation twice.
    auto planeLink=field<char*>(context,0x28);
    if (!planeLink) return 2;
    auto plane=planeLink-0x100;
    const float* frame=method<const float*(*)(void*)>(plane,0x148)(plane);
    double delta[3]={matrix[12]-frame[12],matrix[13]-frame[13],matrix[14]-frame[14]};
    double local[3]{};
    for(int row=0;row<3;row++) for(int axis=0;axis<3;axis++) local[row]+=frame[4*row+axis]*delta[axis];
    pushNumber(L,-std::atan2(local[2],local[0]));
    pushNumber(L,std::atan2(local[1],std::hypot(local[0],local[2])));
    pushNumber(L,std::sqrt(local[0]*local[0]+local[1]*local[1]+local[2]*local[2]));
    return 5;
}
extern "C" __declspec(dllexport) int luaopen_f23b_weapons(lua_State* L) {
    auto module=GetModuleHandleW(L"lua.dll");
    userData=reinterpret_cast<decltype(userData)>(GetProcAddress(module,"lua_touserdata"));
    number=reinterpret_cast<decltype(number)>(GetProcAddress(module,"lua_tonumber"));
    pushNumber=reinterpret_cast<decltype(pushNumber)>(GetProcAddress(module,"lua_pushnumber"));
    pushFunction=reinterpret_cast<decltype(pushFunction)>(GetProcAddress(module,"lua_pushcclosure"));
    if (!userData || !number || !pushNumber || !pushFunction) return 0;
    for (const auto& binary : supported) if (!matches(binary.name, binary.sha)) return 0;
    pushFunction(L,prepare,0);
    return 1;
}
