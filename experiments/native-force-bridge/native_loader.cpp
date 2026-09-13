// SPDX-License-Identifier: MIT
// Compatibility proof only: forward native calls without changing any forces.
// No native patches, injected code, import-table edits, or memory hooks.
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <array>
#include <atomic>
#include <filesystem>
#include <fstream>
#include <mutex>
#include <stdexcept>
#include <string>
#include "names.hpp"

namespace {
constexpr auto count = std::size(names);
std::array<FARPROC, count> callbacks{};
std::array<std::atomic<unsigned long long>, count> calls{};
std::once_flag initialized;
std::mutex log_mutex;

void note(const std::string& text) {
    wchar_t path[2048]{};
    if (GetEnvironmentVariableW(L"F23B_NATIVE_FORWARD_TRACE", path, 2048) == 0) return;
    std::lock_guard<std::mutex> lock(log_mutex);
    std::ofstream(std::filesystem::path(path), std::ios::app) << text << '\n';
}

void initialize() {
    wchar_t executable[2048]{};
    if (!GetModuleFileNameW(nullptr, executable, 2048)) throw std::runtime_error("DCS path unavailable");
    auto root = std::filesystem::path(executable).parent_path().parent_path();
    auto path = root / L"Mods/aircraft/FA-18C/bin/FA18C.dll";
    auto native = GetModuleHandleW(L"FA18C.dll");
    if (native) {
        wchar_t loaded[2048]{};
        GetModuleFileNameW(native, loaded, 2048);
        if (_wcsicmp(std::filesystem::weakly_canonical(path).c_str(),
                     std::filesystem::weakly_canonical(loaded).c_str()) != 0)
            throw std::runtime_error("Native Hornet module is not the installed reference");
    } else native = LoadLibraryExW(path.c_str(), nullptr, LOAD_WITH_ALTERED_SEARCH_PATH);
    if (!native) {
        note("native load failed: " + std::to_string(GetLastError()));
        throw std::runtime_error("Installed Hornet callback library unavailable");
    }
    for (std::size_t i = 0; i < count; ++i) {
        callbacks[i] = GetProcAddress(native, names[i]);
        if (!callbacks[i]) {
            note(std::string("missing native callback: ") + names[i]);
            throw std::runtime_error("Native callback contract mismatch");
        }
    }
    note("resolved all " + std::to_string(count) + " installed native callbacks; zero force modification");
}
}

extern "C" FARPROC* f23b_resolve(unsigned index) noexcept {
  try {
    std::call_once(initialized, initialize);
    if (index >= count) throw std::runtime_error("Invalid callback index");
    const auto n = ++calls[index];
    if (n <= 2 || (std::string(names[index]) == "ed_fm_simulate" && n % 1024 == 0))
        note(std::string(names[index]) + " " + std::to_string(n));
    return &callbacks[index];
  } catch (const std::exception& error) {
    note(std::string("forwarding initialization failed: ") + error.what());
    RaiseException(0xE023B001, EXCEPTION_NONCONTINUABLE, 0, nullptr);
    return nullptr;
  }
}
