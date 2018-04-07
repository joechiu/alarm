-- pyqt-alarm.db

sqlite> SELECT sql FROM sqlite_master WHERE name = 'sat';
CREATE TABLE sat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT,
    h           INT,
    m           INT,
    s           INT,
    t           INT(1),         -- timer or alarm
    a           INT(1),         -- audio/message
    r           INT(1),         -- repeat audio
    d           TEXT,
    c           INT(1),         -- checked
    aud         TEXT,
    msg         TEXT,
    rgb		TEXT DEFAULT '255,0,0',    -- text color
    sz          INT(2) DEFAULT 24,  -- text size
    oc          INT(3) DEFAULT 100, -- text opacity
    created     DATETIME
);
