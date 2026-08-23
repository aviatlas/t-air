# -*- coding: utf-8 -*-
"""Civil helicopters. CIVIL_COLS order (24 fields).

seatsTypical / seatsMax count passengers excluding the crew, and spanM holds
the main rotor diameter so the size comparison bar has something to draw.
"""
N = None

ROWS = [
("bell-206b","Bell","206B JetRanger III","206","helicopter","آمریکا",1962,1967,"retired",4,4,693,214,1520,9.5,10.16,2.91,1,"turboshaft","Rolls-Royce 250-C20J",7300,True,"Bell 206","پرفروش‌ترین بالگرد توربینی سبک تاریخ؛ در ایران هم رایج است."),
("bell-407","Bell","407","206","helicopter","آمریکا",1995,1996,"production",6,6,611,246,2381,12.7,10.67,3.56,1,"turboshaft","Rolls-Royce 250-C47B",N,False,"Bell 407","جانشین جت‌رنجر با روتور چهارپره و کابین پهن‌تر."),
("bell-412","Bell","412EPI","212","helicopter","آمریکا",1979,1981,"production",13,14,656,259,5398,17.13,14.02,4.57,2,"turboshaft","Pratt & Whitney Canada PT6T-9",N,True,"Bell 412","دوموتوره‌ی چهارپره؛ در ایران برای امداد و انتقال بیمار کاربرد دارد."),
("robinson-r44","Robinson","R44 Raven II","R44","helicopter","آمریکا",1990,1993,"production",3,3,555,240,1134,9.07,10.06,3.28,1,"piston","Lycoming IO-540",7000,False,"Robinson R44","ارزان‌ترین راه ورود به پرواز بالگردی و پرشمارترین بالگرد پیستونی جهان."),
("robinson-r22","Robinson","R22 Beta II","R22","helicopter","آمریکا",1975,1979,"production",1,1,389,180,622,8.76,7.67,2.67,1,"piston","Lycoming O-360",4600,False,"Robinson R22","بالگرد دو نفره‌ی آموزشی که بیشتر خلبانان بالگرد با آن شروع می‌کنند."),
("robinson-r66","Robinson","R66 Turbine","R66","helicopter","آمریکا",2007,2010,"production",4,4,650,222,1225,10.67,10.06,3.5,1,"turboshaft","Rolls-Royce RR300",N,False,"Robinson R66","نخستین بالگرد توربینی رابینسون."),
("airbus-h125","Airbus Helicopters","H125 / AS350 B3","Écureuil","helicopter","فرانسه",1974,1975,"production",5,6,610,287,2250,10.93,10.69,3.14,1,"turboshaft","Safran Arriel 2D",N,False,"Eurocopter AS350 Écureuil","تنها بالگردی که روی قله‌ی اورست فرود آمده است."),
("airbus-h135","Airbus Helicopters","H135","EC135","helicopter","آلمان",1994,1996,"production",7,8,635,254,2980,12.16,10.2,3.51,2,"turboshaft","Safran Arrius 2B2",N,False,"Eurocopter EC135","با فنستران کم‌صدا؛ رایج‌ترین بالگرد اورژانس هوایی اروپا."),
("airbus-h145","Airbus Helicopters","H145","BK117","helicopter","آلمان",1999,2002,"production",9,10,662,268,3800,13.64,11.0,3.95,2,"turboshaft","Safran Arriel 2E",N,False,"Eurocopter EC145","کابین بزرگ با درهای کشویی و دو لنگه‌ی عقب."),
("leonardo-aw139","Leonardo","AW139","AW139","helicopter","ایتالیا",2001,2004,"production",15,15,1061,306,7000,16.66,13.8,4.98,2,"turboshaft","Pratt & Whitney Canada PT6C-67C",N,False,"AgustaWestland AW139","استاندارد جابه‌جایی کارکنان سکوهای نفتی دریایی."),
("sikorsky-s-76","Sikorsky","S-76D","S-76","helicopter","آمریکا",1977,1979,"production",12,12,761,287,5307,16.0,13.41,4.41,2,"turboshaft","Pratt & Whitney Canada PW210S",N,False,"Sikorsky S-76","طراحی‌شده برای بازار نفت دریایی و پرواز شخصی مدیران."),
("sikorsky-s-92","Sikorsky","S-92","S-92","helicopter","آمریکا",1998,2004,"production",19,19,999,306,12020,20.88,17.17,5.86,2,"turboshaft","General Electric CT7-8A",N,False,"Sikorsky S-92","بزرگ‌ترین بالگرد غیرنظامی سیکورسکی، رایج در دریای شمال."),
("kamov-ka-32","Kamov","Ka-32A11BC","Ka-27","helicopter","روسیه",1980,1985,"production",13,16,800,260,11000,11.3,15.9,5.4,2,"turboshaft","Klimov TV3-117VMA",N,False,"Kamov Ka-32","روتور هم‌محور دوگانه؛ برای آتش‌نشانی و بار زیرآویز کاربرد دارد."),
("mil-mi-8t-civil","Mil","Mi-8T (civil)","Mi-8","helicopter","شوروی",1961,1967,"production",24,28,465,250,12000,18.17,21.29,5.65,2,"turboshaft","Klimov TV2-117",N,True,"Mil Mi-8","نسخه‌ی غیرنظامی پرتولیدترین بالگرد جهان؛ در ایران هم پرواز می‌کند."),
("mdhelicopters-md-902","MD Helicopters","MD 902 Explorer","MD Explorer","helicopter","آمریکا",1992,1994,"production",7,8,555,258,2835,11.83,10.31,3.66,2,"turboshaft","Pratt & Whitney Canada PW207E",N,False,"MD Helicopters MD Explorer","بدون روتور دم؛ گشتاور را با دمش هوا از بوم کنترل می‌کند."),
]
