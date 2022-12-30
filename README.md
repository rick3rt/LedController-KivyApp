## Deploy on android

```
buildozer android debug deploy run
```

https://buildozer.readthedocs.io/en/latest/quickstart.html#init-and-build-for-android

```
buildozer -v android deploy run logcat | grep python
```

```
~/.buildozer/android/platform/android-sdk/platform-tools/adb logcat | grep python
```
