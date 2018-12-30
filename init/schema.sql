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

insert into sat (h,m,s,t,c,a,r,sz,oc,d,name,aud,msg) values ('2','40','36','0','1','1','0','32','99','Mon, Tue, Wed, Thu','Alarm!','F:/dev/python/exe/alarm-2/sounds/tada.wav','');
insert into sat (h,m,s,t,c,a,r,sz,oc,d,name,aud,msg) values ('10','41','9','0','1','0','0','32','99','','Hello world!','','foo bar!');
insert into sat (h,m,s,t,c,a,r,sz,oc,d,name,aud,msg) values ('2','40','36','1','0','1','1','32','99','','Message alarm!','F:/dev/python/exe/alarm-2/sounds/ringout.wav','');
insert into sat (h,m,s,t,c,a,r,sz,oc,d,name,aud,msg) values ('16','25','0','0','0','0','0','32','99','Fri','foo bar!','','hello world');


UPDATE SQLITE_SEQUENCE SET seq = <n> WHERE name = '<table>'

-- schedule alarm table
CREATE TABLE IF NOT EXISTS sat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT,
    h           INT,
    m           INT,
    s           INT,
    t           INT(1),         -- timer or alarm
    d           TEXT,
    c           INT(1),         -- checked
    a		INT(1),		-- audio / message
    aud         TEXT,
    msg         TEXT,
    created     DATETIME DEFAULT CURRENT_TIMESTAMP
);

    {'id':1,'h':2,'m':40,'s':36,'t':0,'d':'Mon, Tue, Wed, Thu','n':'Alarm!','c':True,'a':0},
    {'id':2,'h':10,'m':41,'s':9,'t':0,'d':'','n':'Hello world!','c':True,'a':0},
    {'id':3,'h':2,'m':40,'s':36,'t':1,'d':'','n':'Message alarm!','c':False,'a':0},
    {'id':4,'h':16,'m':25,'s':0,'t':0,'d':'Fri','n':'foo bar!','c':False,'a':1},

