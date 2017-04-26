# Roll Back
## 简介
这是一个回退程序，根据 diff 的信息将新版的文件回退到旧版

## Usage

首先将 diff 的信息重定向到文件中

```bash
 diff hmmlearn-0.2.0/hmm.py  hmmlearn-0.1.1/hmm.py > diffInfo
```

调用 roll_back.py

```python
python roll_back.py diffInfo hmmlearn-0.2.0/hmm.py 
```

此时当前路径下的 `target.py` 就是原版本的文件

同时可以自定义文件路径，文件名

```python
python roll_back.py diffInfo hmmlearn-0.2.0/hmm.py yourname.py
```

## Requirement
* Python 2.7