#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds data/aircraft.json from the compact tables below.

Two tables, because a fighter and an airliner do not describe themselves with
the same numbers. CIVIL_ROWS carries seat counts; MIL_ROWS carries crew,
service ceiling and armament. Both merge into one record shape at build time,
with the fields the other side does not use left as null.

CIVIL_COLS:
 id, mfr, model, family, type, country, firstFlight, introduced, status,
 seatsTypical, seatsMax, rangeKm, speedKmh, mtowKg, lengthM, spanM, heightM,
 engineCount, engineKind, engineModel, built, iran, wiki, notes

MIL_COLS:
 id, mfr, model, family, type, role, country, firstFlight, introduced, status,
 crew, rangeKm, speedKmh, mtowKg, lengthM, spanM, heightM,
 engineCount, engineKind, engineModel, ceilingM, armament, built, iran, wiki, notes
"""
import importlib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "parts"))

CIVIL_COLS = ["id","mfr","model","family","type","country","firstFlight","introduced","status",
              "seatsTypical","seatsMax","rangeKm","speedKmh","mtowKg","lengthM","spanM","heightM",
              "engineCount","engineKind","engineModel","built","iran","wiki","notes"]

MIL_COLS = ["id","mfr","model","family","type","role","country","firstFlight","introduced","status",
            "crew","rangeKm","speedKmh","mtowKg","lengthM","spanM","heightM",
            "engineCount","engineKind","engineModel","ceilingM","armament","built","iran","wiki","notes"]

CIVIL_TYPES = {"narrowbody", "widebody", "regional", "turboprop", "freighter",
               "piston", "helicopter"}
MIL_TYPES = {"fighter", "bomber", "attack", "transport", "trainer",
             "recon", "maritime", "tanker", "awacs", "utility",
             "helicopter", "uav"}
ENGINE_KINDS = {"jet", "turboprop", "turboshaft", "piston", "rocket", "electric"}
STATUSES = {"production", "active", "retired", "development"}

N = None

CIVIL_ROWS = [
# ---------------- Boeing ----------------
("boeing-707-320b","Boeing","707-320B","707","narrowbody","آمریکا",1957,1959,"retired",141,189,9265,977,151315,46.6,44.4,12.9,4,"jet","Pratt & Whitney JT3D",1010,True,"Boeing 707","نخستین جت مسافربری پرفروش جهان؛ ایران‌ایر و ساها ایر سال‌ها از آن استفاده کردند."),
("boeing-727-200","Boeing","727-200 Advanced","727","narrowbody","آمریکا",1963,1967,"retired",149,189,4020,953,95028,46.7,32.9,10.4,3,"jet","Pratt & Whitney JT8D",1832,True,"Boeing 727","سه‌موتوره با موتورهای دم؛ تا اواخر دهه ۲۰۱۰ در ناوگان ایران‌ایر پرواز می‌کرد."),
("boeing-737-100","Boeing","737-100","737 Original","narrowbody","آمریکا",1967,1968,"retired",85,124,2775,780,50300,28.6,28.35,11.3,2,"jet","Pratt & Whitney JT8D",30,False,"Boeing 737","کوتاه‌ترین عضو خانواده ۷۳۷؛ تنها ۳۰ فروند ساخته شد."),
("boeing-737-200","Boeing","737-200 Advanced","737 Original","narrowbody","آمریکا",1967,1968,"retired",115,136,4260,780,58100,30.5,28.35,11.3,2,"jet","Pratt & Whitney JT8D",1114,True,"Boeing 737","نسخه‌ای که ۷۳۷ را جهانی کرد؛ قابلیت نشستن روی باندهای خاکی."),
("boeing-737-300","Boeing","737-300","737 Classic","narrowbody","آمریکا",1984,1984,"retired",126,149,4400,795,62820,33.4,28.9,11.1,2,"jet","CFM56-3",1113,True,"Boeing 737 Classic","آغاز نسل کلاسیک با موتورهای فن‌بالا و ورودی هوای بیضی‌شکل."),
("boeing-737-400","Boeing","737-400","737 Classic","narrowbody","آمریکا",1988,1988,"retired",147,188,3815,795,68050,36.4,28.9,11.1,2,"jet","CFM56-3",486,True,"Boeing 737 Classic","نسخه کشیده‌شده کلاسیک؛ در ایران هم مسافری و هم باری استفاده شده است."),
("boeing-737-500","Boeing","737-500","737 Classic","narrowbody","آمریکا",1989,1990,"retired",110,132,4440,795,60550,31.0,28.9,11.1,2,"jet","CFM56-3",389,True,"Boeing 737 Classic","جایگزین مستقیم ۷۳۷-۲۰۰ با برد بیشتر."),
("boeing-737-600","Boeing","737-600","737 NG","narrowbody","آمریکا",1998,1998,"retired",110,132,5648,839,65090,31.2,34.3,12.6,2,"jet","CFM56-7B",69,False,"Boeing 737 Next Generation","کم‌فروش‌ترین عضو نسل NG."),
("boeing-737-700","Boeing","737-700","737 NG","narrowbody","آمریکا",1997,1998,"retired",126,149,6230,839,70080,33.6,34.3,12.6,2,"jet","CFM56-7B",1128,False,"Boeing 737 Next Generation","پایه‌ی نسل NG و پرکاربرد در ساوت‌وست."),
("boeing-737-800","Boeing","737-800","737 NG","narrowbody","آمریکا",1997,1998,"retired",162,189,5436,839,79010,39.5,34.3,12.5,2,"jet","CFM56-7B",4991,True,"Boeing 737 Next Generation","پرفروش‌ترین باریک‌پیکر تاریخ تا پیش از مکس؛ در ناوگان چند شرکت ایرانی."),
("boeing-737-900er","Boeing","737-900ER","737 NG","narrowbody","آمریکا",2006,2007,"retired",178,220,5925,839,85130,42.1,34.3,12.5,2,"jet","CFM56-7B",505,False,"Boeing 737 Next Generation","بلندترین ۷۳۷ نسل NG با درهای اضطراری اضافی."),
("boeing-737-max-7","Boeing","737 MAX 7","737 MAX","narrowbody","آمریکا",2018,N,"development",138,172,7130,839,80290,35.6,35.9,12.3,2,"jet","CFM LEAP-1B",N,False,"Boeing 737 MAX","کوتاه‌ترین مکس با بیشترین برد خانواده."),
("boeing-737-max-8","Boeing","737 MAX 8","737 MAX","narrowbody","آمریکا",2016,2017,"production",162,210,6570,839,82190,39.5,35.9,12.3,2,"jet","CFM LEAP-1B",N,False,"Boeing 737 MAX","پرفروش‌ترین عضو خانواده مکس؛ پس از دو سانحه ۲۰ ماه زمین‌گیر شد."),
("boeing-737-max-9","Boeing","737 MAX 9","737 MAX","narrowbody","آمریکا",2017,2018,"production",178,220,6570,839,88314,42.2,35.9,12.3,2,"jet","CFM LEAP-1B",N,False,"Boeing 737 MAX","جایگزین ۷۳۷-۹۰۰ER."),
("boeing-737-max-10","Boeing","737 MAX 10","737 MAX","narrowbody","آمریکا",2021,N,"development",188,230,6110,839,89765,43.8,35.9,12.3,2,"jet","CFM LEAP-1B",N,False,"Boeing 737 MAX","بلندترین ۷۳۷ با ارابه فرود تلسکوپی."),
("boeing-747-100","Boeing","747-100","747","widebody","آمریکا",1969,1970,"retired",366,550,8560,895,333390,70.6,59.6,19.3,4,"jet","Pratt & Whitney JT9D",205,False,"Boeing 747","نخستین پهن‌پیکر جهان و آغاز عصر جامبوجت."),
("boeing-747-200b","Boeing","747-200B","747","widebody","آمریکا",1970,1971,"retired",366,550,12700,907,377842,70.6,59.6,19.3,4,"jet","JT9D / CF6-50 / RB211-524",393,True,"Boeing 747","ستون فقرات پروازهای دوربرد ایران‌ایر در دهه‌های ۷۰ و ۸۰ میلادی."),
("boeing-747sp","Boeing","747SP","747","widebody","آمریکا",1975,1976,"retired",276,400,12320,994,318000,56.3,59.6,20.1,4,"jet","Pratt & Whitney JT9D",45,True,"Boeing 747SP","نسخه کوتاه و فوق‌دوربرد؛ ایران‌ایر یکی از مشهورترین کاربران آن بود."),
("boeing-747-300","Boeing","747-300","747","widebody","آمریکا",1982,1983,"retired",400,565,12400,907,377842,70.6,59.6,19.3,4,"jet","JT9D / CF6-80 / RB211-524",81,False,"Boeing 747","نخستین ۷۴۷ با طبقه بالای کشیده."),
("boeing-747-400","Boeing","747-400","747","widebody","آمریکا",1988,1989,"retired",416,660,13450,916,396890,70.7,64.4,19.4,4,"jet","PW4000 / CF6-80C2 / RB211-524",694,False,"Boeing 747-400","پرفروش‌ترین نسخه ۷۴۷ با وینگ‌لت و کابین دو خلبانه."),
("boeing-747-8i","Boeing","747-8 Intercontinental","747","widebody","آمریکا",2011,2012,"retired",410,605,14320,917,447700,76.3,68.4,19.4,4,"jet","GEnx-2B67",155,False,"Boeing 747-8","بلندترین هواپیمای مسافربری جهان؛ تولید در ۲۰۲۳ پایان یافت."),
("boeing-757-200","Boeing","757-200","757","narrowbody","آمریکا",1982,1983,"retired",200,239,7250,850,115680,47.3,38.0,13.6,2,"jet","RB211-535 / PW2000",913,False,"Boeing 757","باریک‌پیکری با توان صعود استثنایی؛ محبوب پروازهای فرااقیانوسی."),
("boeing-757-300","Boeing","757-300","757","narrowbody","آمریکا",1998,1999,"retired",243,295,6295,850,123600,54.4,38.0,13.6,2,"jet","RB211-535 / PW2000",55,False,"Boeing 757","بلندترین باریک‌پیکر بوئینگ."),
("boeing-767-200er","Boeing","767-200ER","767","widebody","آمریکا",1981,1984,"retired",181,255,12200,851,179170,48.5,47.6,15.8,2,"jet","CF6-80 / PW4000 / RB211-524",121,False,"Boeing 767","نخستین دو موتوره‌ای که پروازهای ETOPS اقیانوس اطلس را عادی کرد."),
("boeing-767-300er","Boeing","767-300ER","767","widebody","آمریکا",1986,1988,"production",218,290,11070,851,186880,54.9,47.6,15.8,2,"jet","CF6-80C2 / PW4000",583,False,"Boeing 767","پرفروش‌ترین نسخه ۷۶۷؛ خط تولید باری آن هنوز فعال است."),
("boeing-767-400er","Boeing","767-400ER","767","widebody","آمریکا",1999,2000,"retired",245,375,10415,851,204120,61.4,51.9,16.8,2,"jet","CF6-80C2",37,False,"Boeing 767","بلندترین ۷۶۷ با وینگ‌تیپ کشیده."),
("boeing-777-200er","Boeing","777-200ER","777","widebody","آمریکا",1994,1997,"retired",313,440,13080,905,297550,63.7,60.9,18.5,2,"jet","GE90 / PW4000 / Trent 800",422,False,"Boeing 777","نخستین هواپیمای کاملاً طراحی‌شده با رایانه."),
("boeing-777-200lr","Boeing","777-200LR","777","widebody","آمریکا",2005,2006,"retired",317,440,15843,905,347450,63.7,64.8,18.6,2,"jet","GE90-110B/115B",61,False,"Boeing 777","رکورددار طولانی‌ترین پرواز بدون توقف یک هواپیمای مسافربری."),
("boeing-777-300er","Boeing","777-300ER","777","widebody","آمریکا",2003,2004,"production",396,550,13650,905,351530,73.9,64.8,18.5,2,"jet","GE90-115B",N,False,"Boeing 777","پرفروش‌ترین پهن‌پیکر دوموتوره؛ ستون ناوگان امارات."),
("boeing-777-9","Boeing","777-9","777X","widebody","آمریکا",2020,N,"development",426,475,13500,905,351500,76.7,71.8,19.7,2,"jet","GE9X",N,False,"Boeing 777X","بلندترین مسافربری جهان با نوک بال تاشو."),
("boeing-787-8","Boeing","787-8 Dreamliner","787","widebody","آمریکا",2009,2011,"production",248,359,13530,903,227930,56.7,60.1,17.0,2,"jet","Trent 1000 / GEnx-1B",N,False,"Boeing 787 Dreamliner","نخستین مسافربری با بدنه عمدتاً کامپوزیتی."),
("boeing-787-9","Boeing","787-9 Dreamliner","787","widebody","آمریکا",2013,2014,"production",296,406,14010,903,254010,62.8,60.1,17.0,2,"jet","Trent 1000 / GEnx-1B",N,False,"Boeing 787 Dreamliner","پرفروش‌ترین نسخه دریم‌لاینر."),
("boeing-787-10","Boeing","787-10 Dreamliner","787","widebody","آمریکا",2017,2018,"production",336,440,11730,903,254010,68.3,60.1,17.0,2,"jet","Trent 1000 / GEnx-1B",N,False,"Boeing 787 Dreamliner","بلندترین دریم‌لاینر با برد کمتر."),
("boeing-717-200","Boeing","717-200","717","regional","آمریکا",1998,1999,"retired",106,134,3815,811,54885,37.8,28.4,8.9,2,"jet","BR715",156,False,"Boeing 717","آخرین بازمانده خط DC-9؛ تولید در ۲۰۰۶ پایان یافت."),
# ---------------- McDonnell Douglas / Douglas ----------------
("douglas-dc-9-30","McDonnell Douglas","DC-9-30","DC-9","narrowbody","آمریکا",1965,1967,"retired",105,115,2780,796,49090,36.4,28.5,8.4,2,"jet","Pratt & Whitney JT8D",976,False,"McDonnell Douglas DC-9","پایه‌ی خانواده‌ای که تا بوئینگ ۷۱۷ ادامه یافت."),
("douglas-dc-10-30","McDonnell Douglas","DC-10-30","DC-10","widebody","آمریکا",1970,1972,"retired",250,380,9600,908,259450,55.5,50.4,17.7,3,"jet","General Electric CF6-50",386,False,"McDonnell Douglas DC-10","سه‌موتوره پهن‌پیکر با موتور روی سکان عمودی."),
("mcdonnell-md-11","McDonnell Douglas","MD-11","MD-11","widebody","آمریکا",1990,1990,"retired",293,410,12670,876,285990,61.6,51.7,17.6,3,"jet","PW4000 / CF6-80C2",200,False,"McDonnell Douglas MD-11","جانشین DC-10؛ امروز عمدتاً باری."),
("mcdonnell-md-82","McDonnell Douglas","MD-82","MD-80","narrowbody","آمریکا",1979,1981,"retired",155,172,3800,811,67812,45.1,32.9,9.0,2,"jet","Pratt & Whitney JT8D-217",1191,True,"McDonnell Douglas MD-80","سال‌ها ستون ناوگان داخلی ایران؛ مشهور به «مادودی»."),
("mcdonnell-md-83","McDonnell Douglas","MD-83","MD-80","narrowbody","آمریکا",1984,1985,"retired",155,172,4635,811,72575,45.1,32.9,9.0,2,"jet","Pratt & Whitney JT8D-219",265,True,"McDonnell Douglas MD-80","نسخه دوربردتر MD-80 با مخزن سوخت اضافی."),
("mcdonnell-md-90-30","McDonnell Douglas","MD-90-30","MD-90","narrowbody","آمریکا",1993,1995,"retired",153,172,3860,811,70760,46.5,32.9,9.3,2,"jet","IAE V2525-D5",116,False,"McDonnell Douglas MD-90","MD-80 موتور تازه؛ آخرین طرح مستقل مک‌دانل داگلاس."),
# ---------------- Airbus ----------------
("airbus-a300b4","Airbus","A300B4-200","A300","widebody","اروپا",1972,1974,"retired",247,345,5375,847,165000,53.6,44.8,16.5,2,"jet","General Electric CF6-50",561,True,"Airbus A300","نخستین پهن‌پیکر دوموتوره جهان و نخستین محصول ایرباس."),
("airbus-a300-600r","Airbus","A300-600R","A300","widebody","اروپا",1987,1988,"retired",266,361,7500,860,171700,54.1,44.8,16.5,2,"jet","CF6-80C2 / PW4000",N,True,"Airbus A300","در ایران‌ایر و ماهان پرکاربرد بوده است."),
("airbus-a310-300","Airbus","A310-300","A310","widebody","اروپا",1982,1983,"retired",187,280,9600,850,164000,46.7,43.9,15.8,2,"jet","CF6-80C2 / PW4000",255,True,"Airbus A310","نخستین ایرباس با کابین دو خلبانه؛ در ناوگان ایران‌ایر و ماهان."),
("airbus-a318","Airbus","A318","A320ceo","narrowbody","اروپا",2002,2003,"retired",107,132,5750,828,68000,31.4,34.1,12.6,2,"jet","CFM56-5B / PW6000",80,False,"Airbus A318","کوچک‌ترین عضو خانواده A320 با گواهی فرود در باندهای شیب‌دار."),
("airbus-a319","Airbus","A319","A320ceo","narrowbody","اروپا",1995,1996,"retired",124,156,6950,828,75500,33.8,35.8,11.8,2,"jet","CFM56-5B / V2500",N,True,"Airbus A319","نسخه کوتاه A320 با برد زیاد."),
("airbus-a320-200","Airbus","A320-200","A320ceo","narrowbody","اروپا",1987,1988,"retired",150,180,6150,828,78000,37.6,35.8,11.8,2,"jet","CFM56-5 / IAE V2500",N,True,"Airbus A320","نخستین مسافربری با سیستم فلای‌بای‌وایر و ساید‌استیک."),
("airbus-a320neo","Airbus","A320neo","A320neo","narrowbody","اروپا",2014,2016,"production",165,194,6300,828,79000,37.6,35.8,11.8,2,"jet","LEAP-1A / PW1100G",N,False,"Airbus A320neo family","کاهش حدود ۱۵ درصدی مصرف سوخت نسبت به نسل ceo."),
("airbus-a321-200","Airbus","A321-200","A320ceo","narrowbody","اروپا",1993,1994,"retired",185,220,5950,828,93500,44.5,35.8,11.8,2,"jet","CFM56-5B / V2500",N,True,"Airbus A321","بلندترین عضو نسل ceo."),
("airbus-a321neo","Airbus","A321neo","A320neo","narrowbody","اروپا",2016,2017,"production",206,244,7400,828,97000,44.5,35.8,11.8,2,"jet","LEAP-1A / PW1100G",N,False,"Airbus A321neo","نسخه‌های LR و XLR برد را تا ۸٬۷۰۰ کیلومتر می‌رسانند."),
("airbus-a330-200","Airbus","A330-200","A330ceo","widebody","اروپا",1997,1998,"retired",247,406,13450,871,242000,58.8,60.3,17.4,2,"jet","Trent 700 / CF6-80E1 / PW4000",N,True,"Airbus A330","در ناوگان ماهان و ایران‌ایر."),
("airbus-a330-300","Airbus","A330-300","A330ceo","widebody","اروپا",1992,1994,"retired",277,440,11750,871,242000,63.7,60.3,16.8,2,"jet","Trent 700 / CF6-80E1 / PW4000",N,True,"Airbus A330","نسخه کشیده و پرظرفیت‌تر A330."),
("airbus-a330-800neo","Airbus","A330-800neo","A330neo","widebody","اروپا",2018,2020,"production",257,406,15094,871,251000,58.8,64.0,17.4,2,"jet","Rolls-Royce Trent 7000",N,False,"Airbus A330neo","کم‌فروش‌ترین نسخه نئو اما با بیشترین برد خانواده."),
("airbus-a330-900neo","Airbus","A330-900neo","A330neo","widebody","اروپا",2017,2018,"production",287,460,13334,871,251000,63.7,64.0,16.8,2,"jet","Rolls-Royce Trent 7000",N,False,"Airbus A330neo","بال جدید با شارک‌لت و کابین Airspace."),
("airbus-a340-300","Airbus","A340-300","A340","widebody","اروپا",1991,1993,"retired",277,440,13500,871,276500,63.7,60.3,16.9,4,"jet","CFM56-5C",218,True,"Airbus A340","چهارموتوره‌ای برای مسیرهایی که ETOPS نداشتند."),
("airbus-a340-600","Airbus","A340-600","A340","widebody","اروپا",2001,2002,"retired",320,475,14450,881,380000,75.4,63.5,17.3,4,"jet","Rolls-Royce Trent 556",97,True,"Airbus A340","تا آمدن ۷۴۷-۸ بلندترین مسافربری جهان بود؛ ماهان از آن استفاده می‌کند."),
("airbus-a350-900","Airbus","A350-900","A350","widebody","اروپا",2013,2015,"production",300,440,15000,903,283000,66.8,64.75,17.1,2,"jet","Rolls-Royce Trent XWB-84",N,False,"Airbus A350","بدنه و بال کامپوزیتی؛ رقیب مستقیم ۷۸۷ و ۷۷۷."),
("airbus-a350-1000","Airbus","A350-1000","A350","widebody","اروپا",2016,2018,"production",350,480,16100,903,319000,73.8,64.75,17.1,2,"jet","Rolls-Royce Trent XWB-97",N,False,"Airbus A350","ارابه فرود اصلی شش‌چرخ برای وزن بیشتر."),
("airbus-a380-800","Airbus","A380-800","A380","widebody","اروپا",2005,2007,"retired",525,853,14800,903,575000,72.7,79.8,24.1,4,"jet","Trent 900 / GP7200",251,False,"Airbus A380","بزرگ‌ترین مسافربری جهان با دو طبقه کامل."),
("airbus-a220-100","Airbus","A220-100","A220","regional","کانادا/اروپا",2013,2016,"production",108,135,6300,828,63100,35.0,35.1,11.5,2,"jet","Pratt & Whitney PW1500G",N,False,"Airbus A220","طراحی بمباردیه CSeries که ایرباس آن را خرید."),
("airbus-a220-300","Airbus","A220-300","A220","regional","کانادا/اروپا",2015,2016,"production",130,160,6300,828,70900,38.7,35.1,11.5,2,"jet","Pratt & Whitney PW1500G",N,False,"Airbus A220","بازده سوخت در کلاس ۱۳۰ صندلی بی‌رقیب است."),
# ---------------- Embraer ----------------
("embraer-erj-145","Embraer","ERJ 145","ERJ","regional","برزیل",1995,1996,"retired",50,50,2800,833,22000,29.9,20.0,6.8,2,"jet","Rolls-Royce AE 3007",N,False,"Embraer ERJ family","جت منطقه‌ای باریک با آرایش ۱+۲."),
("embraer-e170","Embraer","E170","E-Jet","regional","برزیل",2002,2004,"retired",72,80,3982,870,38600,29.9,26.0,9.8,2,"jet","General Electric CF34-8E",N,False,"Embraer E-Jet family","کابین ۲+۲ بدون صندلی وسط."),
("embraer-e175","Embraer","E175","E-Jet","regional","برزیل",2003,2005,"production",78,88,3889,870,40370,31.7,26.0,9.9,2,"jet","General Electric CF34-8E",N,False,"Embraer E-Jet family","پرکاربردترین جت منطقه‌ای در آمریکای شمالی."),
("embraer-e190","Embraer","E190","E-Jet","regional","برزیل",2004,2005,"retired",100,114,4537,870,51800,36.2,28.7,10.6,2,"jet","General Electric CF34-10E",N,True,"Embraer E-Jet family","در ایران هم پرواز کرده است."),
("embraer-e195","Embraer","E195","E-Jet","regional","برزیل",2004,2006,"retired",108,124,4077,870,52290,38.7,28.7,10.6,2,"jet","General Electric CF34-10E",N,False,"Embraer E-Jet family","بلندترین E-Jet نسل اول."),
("embraer-e190-e2","Embraer","E190-E2","E-Jet E2","regional","برزیل",2016,2018,"production",97,114,5278,870,56400,36.2,33.7,10.9,2,"jet","Pratt & Whitney PW1900G",N,False,"Embraer E-Jet E2 family","بال جدید و موتور گیرباکس‌دار."),
("embraer-e195-e2","Embraer","E195-E2","E-Jet E2","regional","برزیل",2017,2019,"production",120,146,4815,870,61500,41.5,35.1,10.9,2,"jet","Pratt & Whitney PW1900G",N,False,"Embraer E-Jet E2 family","بزرگ‌ترین محصول مسافربری امبرائر."),
# ---------------- Bombardier / De Havilland ----------------
("bombardier-crj200","Bombardier","CRJ200","CRJ","regional","کانادا",1991,1992,"retired",50,50,3148,860,23133,26.8,21.2,6.2,2,"jet","General Electric CF34-3B",N,True,"Bombardier CRJ100/200","بر پایه جت تجاری چلنجر؛ در ایران هم استفاده شده است."),
("bombardier-crj700","Bombardier","CRJ700","CRJ","regional","کانادا",1999,2001,"retired",68,78,3620,876,34019,32.3,23.2,7.6,2,"jet","General Electric CF34-8C",N,False,"Bombardier CRJ700 series","بال بازطراحی‌شده و کابین بلندتر."),
("bombardier-crj900","Bombardier","CRJ900","CRJ","regional","کانادا",2001,2003,"retired",76,90,2876,876,38330,36.4,24.9,7.5,2,"jet","General Electric CF34-8C5",N,False,"Bombardier CRJ700 series","محبوب‌ترین CRJ نسل دوم."),
("bombardier-crj1000","Bombardier","CRJ1000","CRJ","regional","کانادا",2008,2010,"retired",97,104,3004,870,41640,39.1,26.2,7.5,2,"jet","General Electric CF34-8C5",N,False,"Bombardier CRJ700 series","بلندترین CRJ ساخته‌شده."),
("dehavilland-dash8-q400","De Havilland Canada","Dash 8 Q400","Dash 8","turboprop","کانادا",1998,2000,"production",78,90,2040,667,29574,32.8,28.4,8.3,2,"turboprop","Pratt & Whitney PW150A",N,False,"De Havilland Canada Dash 8","سریع‌ترین توربوپراپ مسافربری رایج جهان."),
("dehavilland-dash8-300","De Havilland Canada","Dash 8-300","Dash 8","turboprop","کانادا",1987,1989,"retired",50,56,1711,528,19505,25.7,27.4,7.5,2,"turboprop","Pratt & Whitney PW123",N,False,"De Havilland Canada Dash 8","نسخه میانی خانواده دش-۸."),
# ---------------- ATR / Fokker / Saab / BAe ----------------
("atr-42-500","ATR","ATR 42-500","ATR 42","turboprop","اروپا",1994,1995,"production",48,50,1555,556,18600,22.7,24.6,7.6,2,"turboprop","Pratt & Whitney PW127E",N,True,"ATR 42","توربوپراپ کوتاه‌برد با هزینه عملیاتی پایین."),
("atr-72-500","ATR","ATR 72-500","ATR 72","turboprop","اروپا",1997,1997,"retired",70,74,1528,510,22500,27.2,27.05,7.65,2,"turboprop","Pratt & Whitney PW127F",N,True,"ATR 72","نسخه پیش از -۶۰۰ با آویونیک قدیمی‌تر."),
("atr-72-600","ATR","ATR 72-600","ATR 72","turboprop","اروپا",2009,2011,"production",70,78,1528,510,23000,27.2,27.05,7.65,2,"turboprop","Pratt & Whitney PW127M",N,True,"ATR 72","ایران‌ایر پس از برجام چند فروند تحویل گرفت."),
("fokker-100","Fokker","Fokker 100","Fokker 100","regional","هلند",1986,1988,"retired",100,119,3170,845,45810,35.5,28.1,8.5,2,"jet","Rolls-Royce Tay 650",283,True,"Fokker 100","سال‌ها ستون پروازهای داخلی ایران‌ایر."),
("fokker-50","Fokker","Fokker 50","Fokker 50","turboprop","هلند",1985,1987,"retired",50,58,2055,532,20820,25.25,29.0,8.3,2,"turboprop","Pratt & Whitney PW125B",213,True,"Fokker 50","نوسازی F27 با موتور توربوپراپ مدرن."),
("fokker-f28","Fokker","F28 Fellowship","F28","regional","هلند",1967,1969,"retired",65,85,2743,843,33110,29.6,25.1,8.5,2,"jet","Rolls-Royce Spey",241,True,"Fokker F28 Fellowship","پیشِ Fokker 100 و کاربردی در باندهای کوتاه."),
("bae-146-300","British Aerospace","BAe 146-300 / Avro RJ100","BAe 146","regional","بریتانیا",1987,1988,"retired",100,112,2900,801,44225,31.0,26.3,8.6,4,"jet","Lycoming ALF 502 / LF 507",387,False,"British Aerospace 146","چهارموتوره کم‌صدا؛ مناسب فرودگاه‌های شهری."),
("saab-340b","Saab","Saab 340B","Saab 340","turboprop","سوئد",1983,1989,"retired",33,37,1730,522,13155,19.7,21.4,7.0,2,"turboprop","General Electric CT7-9B",459,False,"Saab 340","توربوپراپ سبک منطقه‌ای."),
("concorde","Aérospatiale/BAC","Concorde","Concorde","widebody","اروپا",1969,1976,"retired",100,128,7222,2180,185070,61.7,25.6,12.2,4,"jet","Rolls-Royce/Snecma Olympus 593",20,False,"Concorde","تنها مسافربری مافوق صوت موفق تاریخ؛ ماخ ۲٫۰۴."),
# ---------------- Russia / Ukraine / China ----------------
("tupolev-tu-154m","Tupolev","Tu-154M","Tu-154","narrowbody","شوروی/روسیه",1982,1984,"retired",164,180,3900,900,100000,47.9,37.55,11.4,3,"jet","Soloviev D-30KU-154",N,True,"Tupolev Tu-154","سه‌موتوره روسی که سال‌ها در ناوگان ایران پرواز کرد."),
("tupolev-tu-134","Tupolev","Tu-134","Tu-134","narrowbody","شوروی",1963,1967,"retired",76,84,3200,850,49000,37.1,29.0,9.1,2,"jet","Soloviev D-30",854,False,"Tupolev Tu-134","با دماغه شیشه‌ای در نسخه‌های اولیه."),
("tupolev-tu-204-100","Tupolev","Tu-204-100","Tu-204","narrowbody","روسیه",1989,1996,"retired",164,210,4600,850,103000,46.1,41.8,13.9,2,"jet","Aviadvigatel PS-90A",N,False,"Tupolev Tu-204","پاسخ روسی به بوئینگ ۷۵۷."),
("ilyushin-il-62m","Ilyushin","Il-62M","Il-62","narrowbody","شوروی",1963,1967,"retired",174,198,10000,900,167000,53.1,43.2,12.35,4,"jet","Soloviev D-30KU",292,False,"Ilyushin Il-62","بزرگ‌ترین مسافربری با چهار موتور در دم."),
("ilyushin-il-76td","Ilyushin","Il-76TD","Il-76","freighter","شوروی/روسیه",1971,1976,"production",N,N,4000,850,190000,46.6,50.5,14.8,4,"jet","Soloviev D-30KP",N,True,"Ilyushin Il-76","باربر سنگین با قابلیت فرود در باند خاکی؛ در ایران کاربرد فراوان دارد."),
("ilyushin-il-96-300","Ilyushin","Il-96-300","Il-96","widebody","روسیه",1988,1993,"production",262,300,11000,850,250000,55.3,60.1,17.6,4,"jet","Aviadvigatel PS-90A",N,False,"Ilyushin Il-96","پهن‌پیکر چهارموتوره روسی؛ تولید بسیار محدود."),
("antonov-an-140","Antonov","An-140 / IrAn-140","An-140","turboprop","اوکراین/ایران",1997,2002,"retired",52,52,2320,575,21500,22.6,24.5,8.2,2,"turboprop","Motor Sich TV3-117VMA",N,True,"Antonov An-140","با نام ایران-۱۴۰ در هسا مونتاژ می‌شد؛ پروازش متوقف شده است."),
("antonov-an-148","Antonov","An-148","An-148","regional","اوکراین",2004,2009,"retired",68,85,3500,820,43700,29.1,28.9,8.2,2,"jet","Progress D-436","N",False,"Antonov An-148","جت منطقه‌ای بال-بالا برای باندهای ناهموار."),
("sukhoi-ssj100","Sukhoi","Superjet 100","SSJ","regional","روسیه",2008,2011,"production",98,108,3048,828,45880,29.9,27.8,10.3,2,"jet","PowerJet SaM146",N,False,"Sukhoi Superjet 100","نخستین مسافربری غیرنظامی مدرن روسیه با همکاری غرب."),
("yakovlev-yak-42d","Yakovlev","Yak-42D","Yak-42","narrowbody","شوروی/روسیه",1975,1980,"retired",104,120,2200,810,57000,36.4,34.9,9.8,3,"jet","Lotarev D-36",187,True,"Yakovlev Yak-42","سه‌موتوره میان‌برد؛ در ایران استفاده شده است."),
("comac-arj21-700","COMAC","ARJ21-700 / C909","ARJ21","regional","چین",2008,2016,"production",78,90,3700,828,43500,33.5,27.3,8.4,2,"jet","General Electric CF34-10A",N,False,"Comac ARJ21","نخستین جت مسافربری چین."),
("comac-c919","COMAC","C919","C919","narrowbody","چین",2017,2023,"production",164,192,5555,834,72500,38.9,35.8,11.95,2,"jet","CFM LEAP-1C",N,False,"Comac C919","رقیب چینی A320neo و ۷۳۷ مکس."),
]

# the hand-written table on its own, before the generated parts are folded in —
# scripts/merge_parts.py dedupes against this, not against the merged result
BASE_CIVIL_ROWS = list(CIVIL_ROWS)

MIL_ROWS = []

try:
    from military_data import MIL_ROWS as _MIL
    MIL_ROWS = _MIL
except ImportError:
    pass

try:
    from civil_extra import CIVIL_ROWS_EXTRA as _CIVX
    CIVIL_ROWS = CIVIL_ROWS + _CIVX
except ImportError:
    pass


# Same airframe reached the table twice from different part files; keep the
# richer record and drop the thinner one.
EXCLUDE = {
    "aermacchi-mb-339a",   # duplicate of aermacchi-mb-339
    "ilyushin-il-76td",    # the military Il-76 record carries crew and build count
}

BLANK = {"seatsTypical": N, "seatsMax": N, "crew": N,
         "ceilingM": N, "armament": N, "role": N, "builtFamily": False}


def to_obj(row, cols, category):
    obj = dict(BLANK)
    obj.update(dict(zip(cols, row)))
    obj["category"] = category
    obj["iran"] = bool(obj["iran"])
    return obj


EN_PARTS = ["en_0", "en_1", "en_2", "en_3", "en_4", "en_5"]


def apply_corrections(data):
    """Fold scripts/fixes/*.py over the generated records.

    Audits are recorded as corrections rather than edited into the source
    tables, so the provenance of every changed figure stays readable:
    fixes/<name>.py exports FIXES = {id: {field: value}} and, optionally,
    DROP = [id, ...] for records that should not be in the database at all.
    """
    import glob
    fixes, drop, family, verified = {}, set(), set(), set()
    checked_on = None
    here = os.path.dirname(os.path.abspath(__file__))
    for path in sorted(glob.glob(os.path.join(here, "fixes", "*.py"))):
        name = os.path.splitext(os.path.basename(path))[0]
        if name.startswith("_"):
            continue
        mod = importlib.import_module("fixes." + name)
        for k, v in getattr(mod, "FIXES", {}).items():
            fixes.setdefault(k, {}).update(v)
        drop.update(getattr(mod, "DROP", []))
        family.update(getattr(mod, "FAMILY_COUNT", []))
        # VERIFIED lists records that were read against their cited source,
        # field by field. The interface says so on the record, and says
        # nothing on the ones that were not — the absence is the honest part.
        verified.update(getattr(mod, "VERIFIED", []))
        # the month the reading was done — a mark means "agreed with the
        # article then", and an article can change afterwards
        checked_on = getattr(mod, "CHECKED_ON", None) or checked_on

    by_id = {d["id"]: d for d in data}
    for k in verified:
        if k in by_id:
            by_id[k]["checked"] = True
    for k in family:
        if k in by_id:
            # the interface marks these so a reader does not read a family
            # total as this one variant's output
            by_id[k]["builtFamily"] = True
    applied = 0
    for k, patch in fixes.items():
        rec = by_id.get(k)
        if not rec:
            continue
        for field, val in patch.items():
            if rec.get(field) != val:
                rec[field] = val
                applied += 1
    return applied, drop, len(verified), checked_on


def attach_english(data):
    """Fold scripts/parts/en_*.py into the records as role_en / armament_en /
    notes_en. A record with no translation keeps only its Persian text; the
    interface falls back to that."""
    en = {}
    for m in EN_PARTS:
        try:
            en.update(importlib.import_module(m).EN)
        except ImportError:
            pass
    hit = 0
    for d in data:
        v = en.get(d["id"])
        if not v:
            continue
        hit += 1
        for key, val in zip(("role_en", "armament_en", "notes_en"), v):
            d[key] = val.strip() or N
    return hit


def check(data):
    ids = [d["id"] for d in data]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    assert not dupes, "duplicate ids: " + str(dupes)
    for d in data:
        allowed = CIVIL_TYPES if d["category"] == "civil" else MIL_TYPES
        assert d["type"] in allowed, ("bad type", d["id"], d["type"])
        assert d["status"] in STATUSES, ("bad status", d["id"], d["status"])
        assert d["engineKind"] in ENGINE_KINDS, ("bad engineKind", d["id"], d["engineKind"])
        for k in ("rangeKm", "speedKmh", "mtowKg", "lengthM", "spanM"):
            v = d.get(k)
            assert v is None or (isinstance(v, (int, float)) and v > 0), ("bad " + k, d["id"], v)
        if d["firstFlight"]:
            assert 1900 < d["firstFlight"] < 2035, ("bad firstFlight", d["id"])


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(here, "data", "aircraft.json")
    data = ([to_obj(r, CIVIL_COLS, "civil") for r in CIVIL_ROWS] +
            [to_obj(r, MIL_COLS, "military") for r in MIL_ROWS])
    data = [d for d in data if d["id"] not in EXCLUDE]
    translated = attach_english(data)
    applied, drop, checked, checked_on = apply_corrections(data)
    data = [d for d in data if d["id"] not in drop]
    check(data)
    data.sort(key=lambda d: (d["category"], d["mfr"], d["model"]))
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"version": 3, "count": len(data),
                   "checkedAgainst": "en.wikipedia.org", "checkedCount": checked,
                   "checkedOn": checked_on,
                   "aircraft": data},
                  f, ensure_ascii=False, separators=(",", ":"))
    civ = sum(1 for d in data if d["category"] == "civil")
    print(f"wrote {len(data)} aircraft ({civ} civil, {len(data)-civ} military, "
          f"{translated} with English text, {applied} audited corrections, "
          f"{checked} source-checked, {len(drop)} dropped) -> {out}")


if __name__ == "__main__":
    main()
