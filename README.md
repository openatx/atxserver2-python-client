# atxserver2 python client
Make it easy to use atxserver2

## Requirements
- Python 3.6+

## Install
```
pip install --upgrade atxserver2-python-client
```

## Usage
```python
import atxserver2

client = atxserver2.Client("http://localhost:4000", "xxxx-your-token-here-xxxxx")
for device in client.list_device():
    print("Device", device)
    device.acquire() # 占用设备
    device.acquire(email="tt@example.com", idle_timeout=6000) # 指定用户占用设备, 时长6000秒
    device.release() # 释放设备

    print(device.atx_agent_address) # 获取设备信息
