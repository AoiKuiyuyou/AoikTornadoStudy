# AoikTornadoStudy
Python **Tornado** library study.

Tested working with:
- Python 2.7 and 3.5
- Tornado 4.4.2

Trace call using [AoikTraceCall](https://github.com/AoiKuiyuyou/AoikTraceCall):
- [RequestHandlerIOLoopTraceCall.py](/src/RequestHandlerIOLoopTraceCall.py)
- [RequestHandlerIOLoopTraceCallLogPy2.txt](/src/RequestHandlerIOLoopTraceCallLogPy2.txt?raw=True)
- [RequestHandlerIOLoopTraceCallLogPy3.txt](/src/RequestHandlerIOLoopTraceCallLogPy3.txt?raw=True)
- [RequestHandlerIOLoopTraceCallNotesPy2.txt](/src/RequestHandlerIOLoopTraceCallNotesPy2.txt?raw=True)
- [RequestHandlerIOLoopTraceCallNotesPy3.txt](/src/RequestHandlerIOLoopTraceCallNotesPy3.txt?raw=True)

## Table of Contents
- [Set up AoikTraceCall](#set-up-aoiktracecall)
  - [Setup via pip](#setup-via-pip)
  - [Setup via git](#setup-via-git)
- [Usage](#usage)
  - [Start server](#start-server)
  - [Send request](#send-request)

## Set up AoikTraceCall
- [Setup via pip](#setup-via-pip)
- [Setup via git](#setup-via-git)

### Setup via pip
Run:
```
pip install git+https://github.com/AoiKuiyuyou/AoikTraceCall
```

### Setup via git
Run:
```
git clone https://github.com/AoiKuiyuyou/AoikTraceCall

cd AoikTraceCall

python setup.py install
```

## Usage
- [Start server](#start-server)
- [Send request](#send-request)

### Start server
Run:
```
python "AoikTornadoStudy/src/RequestHandlerIOLoopTraceCall.py" > Log.txt 2>&1
```

### Send request
Run:
```
curl -X POST -d hello http://127.0.0.1:8000/
```
