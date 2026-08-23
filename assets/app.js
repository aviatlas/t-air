/* T-AIR — app logic
   Data: data/aircraft.json (or window.__AIRCRAFT__ in the single-file build).
   Strings: window.TAIR_I18N (assets/i18n.js).

   Two record shapes share one list: civil aircraft carry seat counts, military
   aircraft carry crew, service ceiling and armament. Everything that differs
   between them resolves through isMil() rather than being duplicated.

   Both languages are rendered from the same records: latin fields (model,
   manufacturer, engine) are shown as-is, and role / armament / notes carry an
   _en twin, falling back to the Persian text when a translation is missing. */

(function () {
  "use strict";

  var I18N = window.TAIR_I18N;

  /* ---------------------------------------------------------------- helpers */

  var FA_DIGITS = "۰۱۲۳۴۵۶۷۸۹";
  var AR_DIGITS = "٠١٢٣٤٥٦٧٨٩";

  function toLatinDigits(s) {
    return String(s).replace(/[۰-۹٠-٩]/g, function (d) {
      var i = FA_DIGITS.indexOf(d);
      return String(i > -1 ? i : AR_DIGITS.indexOf(d));
    });
  }

  function faDigits(s) {
    return String(s).replace(/[0-9]/g, function (d) { return FA_DIGITS[+d]; });
  }

  function norm(s) {
    return toLatinDigits(s)
      .toLowerCase()
      .replace(/[يى]/g, "ی")
      .replace(/[ك]/g, "ک")
      .replace(/[‌‏‎]/g, " ")
      .replace(/[ً-ْ]/g, "")
      .replace(/[^\p{L}\p{N}]+/gu, " ")
      .trim();
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function isMil(a) { return a.category === "military"; }

  /* ------------------------------------------------------------- language */

  function readStored(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }
  function store(key, val) {
    try { localStorage.setItem(key, val); } catch (e) { /* private mode */ }
  }

  var lang = readStored("tair-lang") === "en" ? "en" : "fa";

  function t(key) { return I18N.STR[lang][key]; }

  /* digits: Persian numerals in Persian, latin in English */
  function d(v) { return lang === "fa" ? faDigits(v) : String(v); }
  function num(v) {
    return v == null ? "—" : d(Number(v).toLocaleString("en-US"));
  }

  function typeLabel(k) { return I18N.TYPE[k] ? I18N.TYPE[k][lang] : k; }
  function engineLabel(k) { return I18N.ENGINE[k] ? I18N.ENGINE[k][lang] : k; }
  function statusOf(k) {
    var s = I18N.STATUS[k];
    return { label: s ? s[lang] : k, cls: s ? s.cls : "tag--dim" };
  }
  function countryLabel(c) {
    return lang === "en" ? (I18N.COUNTRY[c] || c) : c;
  }
  /* the _en twin when we have one, the Persian original when we do not */
  function field(a, key) {
    return lang === "en" ? (a[key + "_en"] || a[key]) : a[key];
  }

  /* Persian numerals for standalone numbers, leaving latin designations
     such as AIM-9 or R-73 alone */
  function faNumbersIn(text) {
    if (lang !== "fa") return String(text);
    return String(text).replace(/(^|[^A-Za-z0-9-])(\d+)(?![A-Za-z0-9-])/g,
      function (_, pre, n) { return pre + faDigits(n); });
  }

  /* ------------------------------------------------------------ vocabulary */

  /* Persian spellings people actually type, mapped onto the latin data. */
  var SYNONYMS = {
    "بوئینگ": "boeing", "بویینگ": "boeing", "بوينگ": "boeing",
    "ایرباس": "airbus", "ايرباس": "airbus", "اربس": "airbus",
    "امبرائر": "embraer", "امبراییر": "embraer",
    "بمباردیه": "bombardier", "بمباردیر": "bombardier",
    "فوکر": "fokker", "فوكر": "fokker",
    "توپولف": "tupolev", "توپولوف": "tupolev",
    "ایلیوشین": "ilyushin", "ایلوشین": "ilyushin",
    "آنتونوف": "antonov", "انتونوف": "antonov",
    "سوخو": "sukhoi", "سوخوی": "sukhoi", "سوپرجت": "superjet",
    "یاکولف": "yakovlev", "یاک": "yak",
    "میگ": "mig", "میکویان": "mikoyan",
    "مک‌دانل": "mcdonnell", "مکدانل": "mcdonnell", "داگلاس": "douglas",
    "لاکهید": "lockheed", "لاکهد": "lockheed",
    "نورثروپ": "northrop", "گرومن": "grumman", "گرامن": "grumman",
    "داسو": "dassault", "میراژ": "mirage", "میراج": "mirage",
    "ساب": "saab", "کنکورد": "concorde",
    "کومک": "comac", "کوماک": "comac",
    "سوپرمارین": "supermarine", "اسپیتفایر": "spitfire",
    "مسراشمیت": "messerschmitt", "مسرشمیت": "messerschmitt",
    "فوکه‌وولف": "focke wulf", "یونکرس": "junkers", "هاینکل": "heinkel",
    "میتسوبیشی": "mitsubishi", "زیرو": "zero",
    "موستانگ": "mustang", "تاندربولت": "thunderbolt", "لایتنینگ": "lightning",
    "فانتوم": "phantom", "تامکت": "tomcat", "تام‌کت": "tomcat",
    "شاهین جنگی": "fighting falcon", "هورنت": "hornet", "رپتور": "raptor",
    "ایگل": "eagle", "رافال": "rafale", "تایفون": "typhoon", "گریپن": "gripen",
    "هرکولس": "hercules", "هرکول": "hercules",
    "جامبو": "747", "دریملاینر": "787", "دریم‌لاینر": "787",
    "مافوق صوت": "concorde",
    "اف ۱۴": "f-14", "اف ۵": "f-5", "اف ۴": "f-4", "اف ۱۶": "f-16",
    "صاعقه": "saeqeh", "کوثر": "kowsar", "آذرخش": "azarakhsh"
  };

  var CIVIL_TYPES = ["narrowbody", "widebody", "regional", "turboprop", "piston",
                     "freighter", "helicopter"];
  var MIL_TYPES = ["fighter", "bomber", "attack", "transport", "helicopter", "uav",
                   "trainer", "recon", "maritime", "tanker", "awacs", "utility"];

  var PAGE = 96;

  /* ------------------------------------------------------------------ state */

  var DATA = [];
  var byId = {};
  /* photos.json is written by scripts/fetch_photos.py and is optional: with no
     local photo library the sheet still pulls a picture from Wikipedia live,
     and the cards fall back to a silhouette. */
  var PHOTOS = {};
  var INLINE = window.__PHOTOS_INLINE__ || {};
  /* the cards only grow a picture band once a photo library exists; until
     scripts/fetch_photos.py has run, the compact card is the better card */
  var HAS_PHOTOS = false;
  var MAX_SEATS = 1, MAX_SPEED = 1;
  var shown = PAGE;
  var state = { q: "", cat: "", type: "", engine: "", iran: false, prod: false,
                decade: null, sort: "relevance" };
  var compare = [];   /* ids, at most three */

  var $q = document.getElementById("q");
  var $grid = document.getElementById("grid");
  var $empty = document.getElementById("empty");
  var $count = document.getElementById("count");
  var $filters = document.getElementById("filters");
  var $types = document.getElementById("typeFilters");
  var $more = document.getElementById("more");
  var $timeline = document.getElementById("timeline");
  var $tray = document.getElementById("tray");
  var $scrim = document.getElementById("scrim");
  var $clear = document.getElementById("clearBtn");

  /* ------------------------------------------------------------------ theme */

  function applyTheme(mode) {
    if (mode === "light" || mode === "dark") {
      document.documentElement.setAttribute("data-theme", mode);
    } else {
      document.documentElement.removeAttribute("data-theme");
    }
    document.getElementById("themeLabel").textContent =
      mode === "light" ? t("themeLight") : mode === "dark" ? t("themeDark") : t("themeSystem");
  }

  var themeOrder = ["system", "light", "dark"];
  var theme = readStored("tair-theme") || "system";
  document.getElementById("themeBtn").addEventListener("click", function () {
    theme = themeOrder[(themeOrder.indexOf(theme) + 1) % themeOrder.length];
    store("tair-theme", theme);
    applyTheme(theme);
  });

  /* --------------------------------------------------- static text + langs */

  function applyLang() {
    var root = document.documentElement;
    root.lang = lang;
    root.dir = t("dir");

    Array.prototype.forEach.call(document.querySelectorAll("[data-i18n]"), function (n) {
      n.textContent = t(n.getAttribute("data-i18n"));
    });
    Array.prototype.forEach.call(document.querySelectorAll("[data-i18n-attr]"), function (n) {
      n.getAttribute("data-i18n-attr").split(",").forEach(function (pair) {
        var bits = pair.split(":");
        n.setAttribute(bits[0], t(bits[1]));
      });
    });

    $filters.setAttribute("aria-label", t("sortLabel"));
    $types.setAttribute("aria-label", t("allTypes"));
    $timeline.setAttribute("aria-label", t("timelineTitle"));
    $grid.setAttribute("aria-label", t("resultsLabel"));

    var lb = document.getElementById("langBtn");
    lb.querySelector("span").textContent = t("langBtn");
    lb.setAttribute("aria-label", t("langAria"));
    applyTheme(theme);
  }

  document.getElementById("langBtn").addEventListener("click", function () {
    lang = lang === "fa" ? "en" : "fa";
    store("tair-lang", lang);
    if (!$scrim.hidden) closeSheet();
    applyLang();
    DATA.forEach(function (a) { a._hay = haystack(a); });
    buildStats();
    buildTray();
    render();
  });

  /* ----------------------------------------------------------------- search */

  /* one index per record covering both languages, so a Persian query still
     finds a record while the interface is in English and vice versa */
  function haystack(a) {
    var prop = a.engineKind === "piston" || a.engineKind === "turboprop";
    return norm([a.model, a.mfr, a.family, a.wiki, a.engineModel,
                 a.role, a.role_en, a.notes, a.notes_en, a.armament, a.armament_en,
                 I18N.TYPE[a.type] ? I18N.TYPE[a.type].fa + " " + I18N.TYPE[a.type].en : a.type,
                 I18N.ENGINE[a.engineKind].fa + " " + I18N.ENGINE[a.engineKind].en,
                 a.country, I18N.COUNTRY[a.country] || "",
                 isMil(a) ? "نظامی جنگی military combat" : "غیرنظامی مسافربری civil airliner",
                 prop ? "ملخی پروانه‌ای propeller prop" : "جت jet"].join(" "));
  }

  /* Swap Persian spellings for the latin token the data stores, so
     "بویینگ ۷۳۷" searches as "boeing 737". Longest key first. */
  var SYN_KEYS = Object.keys(SYNONYMS)
    .map(function (k) { return { n: norm(k), v: SYNONYMS[k] }; })
    .sort(function (a, b) { return b.n.length - a.n.length; });

  function expand(query) {
    SYN_KEYS.forEach(function (s) {
      if (s.n && query.indexOf(s.n) > -1) query = query.split(s.n).join(" " + s.v + " ");
    });
    return query;
  }

  function score(a, terms) {
    var model = a._model, total = 0;
    for (var i = 0; i < terms.length; i++) {
      var term = terms[i];
      if (!term) continue;
      if (model === term) total += 100;
      else if (model.indexOf(term) === 0) total += 60;
      else if (model.indexOf(term) > -1) total += 40;
      else if (norm(a.mfr).indexOf(term) > -1) total += 25;
      else if (norm(a.family).indexOf(term) > -1) total += 20;
      else if (a._hay.indexOf(term) > -1) total += 8;
      else return -1;
    }
    return total;
  }

  function results() {
    var terms = norm(expand(norm(state.q))).split(" ").filter(Boolean);
    var list = DATA.filter(function (a) {
      if (state.cat && a.category !== state.cat) return false;
      if (state.type && a.type !== state.type) return false;
      if (state.engine === "prop" && a.engineKind !== "piston" && a.engineKind !== "turboprop") return false;
      if (state.engine === "jet" && a.engineKind !== "jet") return false;
      if (state.iran && !a.iran) return false;
      if (state.prod && a.status !== "production") return false;
      if (state.decade != null) {
        var y = a.introduced || a.firstFlight;
        if (!y || Math.floor(y / 10) * 10 !== state.decade) return false;
      }
      return true;
    });

    if (terms.length) {
      list = list.map(function (a) { return { a: a, s: score(a, terms) }; })
                 .filter(function (r) { return r.s >= 0; })
                 .sort(function (x, y) {
                   if (y.s !== x.s) return y.s - x.s;
                   /* equal relevance → chronological, so a family reads in order */
                   return (x.a.introduced || x.a.firstFlight || 9999) -
                          (y.a.introduced || y.a.firstFlight || 9999);
                 })
                 .map(function (r) { return r.a; });
    }

    var by = {
      seats: function (x, y) { return (y.seatsTypical || 0) - (x.seatsTypical || 0); },
      speed: function (x, y) { return (y.speedKmh || 0) - (x.speedKmh || 0); },
      range: function (x, y) { return (y.rangeKm || 0) - (x.rangeKm || 0); },
      newest: function (x, y) { return (y.introduced || y.firstFlight || 0) - (x.introduced || x.firstFlight || 0); },
      oldest: function (x, y) { return (x.introduced || x.firstFlight || 9999) - (y.introduced || y.firstFlight || 9999); },
      name: function (x, y) { return x.model.localeCompare(y.model); }
    }[state.sort];
    if (by) list = list.slice().sort(by);
    return list;
  }

  /* ---------------------------------------------------------------- filters */

  function chip(label, active, onclick, extra) {
    var b = el("button", "chip" + (extra ? " " + extra : ""), label);
    b.type = "button";
    b.setAttribute("aria-pressed", active ? "true" : "false");
    b.addEventListener("click", onclick);
    return b;
  }

  function buildFilters() {
    $filters.textContent = "";

    /* category comes first: it decides which type chips make sense below */
    var seg = el("div", "seg");
    [["", "catAll"], ["civil", "catCivil"], ["military", "catMil"]].forEach(function (c) {
      var b = el("button", "seg__btn", t(c[1]));
      b.type = "button";
      b.setAttribute("aria-pressed", state.cat === c[0] ? "true" : "false");
      b.addEventListener("click", function () {
        if (state.cat === c[0]) return;
        state.cat = c[0];
        state.type = "";
        render();
      });
      seg.appendChild(b);
    });
    $filters.appendChild(seg);

    $filters.appendChild(el("div", "filters__sep"));
    $filters.appendChild(chip(t("chipProp"), state.engine === "prop", function () {
      state.engine = state.engine === "prop" ? "" : "prop"; render();
    }));
    $filters.appendChild(chip(t("chipJet"), state.engine === "jet", function () {
      state.engine = state.engine === "jet" ? "" : "jet"; render();
    }));
    $filters.appendChild(el("div", "filters__sep"));
    $filters.appendChild(chip(t("chipIran"), state.iran, function () {
      state.iran = !state.iran; render();
    }, "chip--iran"));
    $filters.appendChild(chip(t("chipProd"), state.prod, function () {
      state.prod = !state.prod; render();
    }));

    var wrap = el("div", "sortwrap");
    var lab = el("label", null, t("sortLabel"));
    lab.setAttribute("for", "sort");
    var sel = el("select");
    sel.id = "sort";
    [["relevance", "sortRelevance"], ["newest", "sortNewest"], ["oldest", "sortOldest"],
     ["speed", "sortSpeed"], ["range", "sortRange"],
     ["seats", "sortSeats"], ["name", "sortName"]]
      .forEach(function (o) {
        var op = el("option", null, t(o[1]));
        op.value = o[0];
        if (state.sort === o[0]) op.selected = true;
        sel.appendChild(op);
      });
    sel.addEventListener("change", function () { state.sort = sel.value; render(); });
    wrap.appendChild(lab);
    wrap.appendChild(sel);
    $filters.appendChild(wrap);

    /* type chips, scoped to the chosen category */
    $types.textContent = "";
    /* helicopter sits in both pools, so the union has to be de-duplicated */
    var pool = state.cat === "civil" ? CIVIL_TYPES
             : state.cat === "military" ? MIL_TYPES
             : CIVIL_TYPES.concat(MIL_TYPES).filter(function (v, i, arr) {
                 return arr.indexOf(v) === i;
               });
    var counts = {};
    DATA.forEach(function (a) {
      if (state.cat && a.category !== state.cat) return;
      counts[a.type] = (counts[a.type] || 0) + 1;
    });
    $types.appendChild(chip(t("allTypes"), !state.type, function () {
      state.type = ""; render();
    }));
    pool.forEach(function (ty) {
      if (!counts[ty]) return;
      var b = chip(typeLabel(ty), state.type === ty, function () {
        state.type = state.type === ty ? "" : ty; render();
      }, "chip--type t-" + ty);
      b.appendChild(el("span", "chip__n", d(counts[ty])));
      $types.appendChild(b);
    });
  }

  /* --------------------------------------------------------------- timeline */

  /* A histogram of service-entry decades that doubles as a filter: the shape
     of the collection is itself information — the WWII spike, the jet-age
     climb — and each bar is the control for its own decade. */
  function buildTimeline() {
    var counts = {}, min = 9999, max = 0;
    DATA.forEach(function (a) {
      var y = a.introduced || a.firstFlight;
      if (!y) return;
      var dec = Math.floor(y / 10) * 10;
      counts[dec] = (counts[dec] || 0) + 1;
      if (dec < min) min = dec;
      if (dec > max) max = dec;
    });
    var peak = 1;
    for (var k in counts) peak = Math.max(peak, counts[k]);

    $timeline.textContent = "";
    var head = el("div", "timeline__head");
    head.appendChild(el("span", "timeline__title", t("timelineTitle")));
    if (state.decade != null) {
      var clear = el("button", "timeline__clear", t("timelineAll"));
      clear.type = "button";
      clear.addEventListener("click", function () { state.decade = null; render(); });
      head.appendChild(clear);
    }
    $timeline.appendChild(head);

    var bars = el("div", "timeline__bars");
    for (var dec = min; dec <= max; dec += 10) {
      var n = counts[dec] || 0;
      var b = el("button", "timeline__bar" + (state.decade === dec ? " is-on" : ""));
      b.type = "button";
      b.disabled = !n;
      b.title = d(dec) + "s — " + d(n);
      b.setAttribute("aria-label", d(dec) + "s: " + d(n));
      b.setAttribute("aria-pressed", state.decade === dec ? "true" : "false");
      var fill = el("span", "timeline__fill");
      fill.style.height = (n ? Math.max(6, n / peak * 100) : 0) + "%";
      b.appendChild(fill);
      /* label only the anchor decades — a tick under every bar is noise, and
         two-digit labels cannot tell 1910 from 2010 */
      var anchor = dec % 50 === 0 || dec === min || dec === max;
      b.appendChild(el("span", "timeline__tick", anchor ? d(dec) : ""));
      (function (value) {
        b.addEventListener("click", function () {
          state.decade = state.decade === value ? null : value;
          render();
        });
      })(dec);
      bars.appendChild(b);
    }
    $timeline.appendChild(bars);
  }

  /* -------------------------------------------------------------- comparison */

  function inCompare(id) { return compare.indexOf(id) > -1; }

  function toggleCompare(id) {
    var i = compare.indexOf(id);
    if (i > -1) compare.splice(i, 1);
    else if (compare.length < 3) compare.push(id);
    buildTray();
    render(true);
  }

  function buildTray() {
    $tray.textContent = "";
    $tray.hidden = compare.length === 0;
    if (!compare.length) return;

    var inner = el("div", "wrap tray__row");
    inner.appendChild(el("span", "tray__hint", t("compareHint")));
    var chips = el("div", "tray__chips");
    compare.forEach(function (id) {
      var a = byId[id];
      if (!a) return;
      var c = el("button", "tray__chip");
      c.type = "button";
      c.appendChild(el("span", null, a.model));
      c.appendChild(el("span", "tray__x", "×"));
      c.setAttribute("aria-label", t("compareRemove") + " — " + a.model);
      c.addEventListener("click", function () { toggleCompare(id); });
      chips.appendChild(c);
    });
    inner.appendChild(chips);

    var open = el("button", "tray__go", t("compareOpen"));
    open.type = "button";
    open.disabled = compare.length < 2;
    open.addEventListener("click", openCompare);
    inner.appendChild(open);

    var clear = el("button", "tray__clear", t("compareClear"));
    clear.type = "button";
    clear.addEventListener("click", function () { compare = []; buildTray(); render(true); });
    inner.appendChild(clear);

    $tray.appendChild(inner);
  }

  function compareRows(list) {
    var anyMil = list.some(isMil);
    var rows = [
      [t("lFirstFlight"), function (a) { return a.firstFlight ? d(a.firstFlight) : "—"; }],
      [t("lIntroduced"), function (a) { return a.introduced ? d(a.introduced) : "—"; }],
      [t("lMaxSpeed"), function (a) { return num(a.speedKmh) + " km/h"; }, "speedKmh"],
      [t("lRange"), function (a) { return num(a.rangeKm) + " km"; }, "rangeKm"],
      [t("lMtow"), function (a) { return num(a.mtowKg) + " kg"; }, "mtowKg"],
      [t("lLength"), function (a) { return (a.lengthM == null ? "—" : d(a.lengthM)) + " m"; }, "lengthM"],
      [t("lSpan"), function (a) { return (a.spanM == null ? "—" : d(a.spanM)) + " m"; }, "spanM"],
      [t("lEngines"), function (a) {
        return (a.engineCount == null ? "—" : d(a.engineCount)) + " × " + engineLabel(a.engineKind);
      }],
      [t("lEngineModel"), function (a) { return a.engineModel || "—"; }],
      [t("lBuilt"), function (a) {
        return a.built == null ? "—"
             : num(a.built) + (a.builtFamily ? " *" : "");
      }, "built"]
    ];
    if (anyMil) {
      rows.splice(2, 0, [t("lCrew"), function (a) {
        return a.crew == null ? "—" : a.crew === 0 ? t("uncrewed") : d(a.crew);
      }]);
      rows.splice(6, 0, [t("lCeiling"), function (a) { return num(a.ceilingM) + " m"; }, "ceilingM"]);
    }
    if (list.some(function (a) { return !isMil(a); })) {
      rows.splice(2, 0, [t("lSeatsTyp"), function (a) {
        return a.seatsTypical == null ? "—" : num(a.seatsTypical);
      }, "seatsTypical"]);
    }
    return rows;
  }

  function openCompare() {
    var list = compare.map(function (id) { return byId[id]; }).filter(Boolean);
    if (list.length < 2) return;
    lastFocus = document.activeElement;
    $scrim.textContent = "";

    var sheet = el("div", "sheet sheet--compare");

    var head = el("div", "sheet__head");
    var title = el("div", "sheet__title");
    title.appendChild(el("span", "card__mfr", "T-AIR"));
    var h2 = el("h2", null, t("compareTitle"));
    h2.id = "sheetTitle";
    h2.style.fontFamily = "var(--fa)";
    title.appendChild(h2);
    head.appendChild(title);
    var close = el("button", "close-btn");
    close.type = "button";
    close.setAttribute("aria-label", t("closeAria"));
    close.innerHTML = '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m6 6 12 12M18 6 6 18"/></svg>';
    close.addEventListener("click", closeSheet);
    head.appendChild(close);
    sheet.appendChild(head);

    var body = el("div", "sheet__body");
    var scroller = el("div", "cmp-scroll");
    var table = el("table", "cmp");

    var thead = el("thead");
    var hr = el("tr");
    hr.appendChild(el("th", "cmp__corner", t("field")));
    list.forEach(function (a) {
      var th = el("th", "t-" + a.type);
      th.appendChild(el("span", "card__mfr", a.mfr));
      th.appendChild(el("span", "cmp__model", a.model));
      hr.appendChild(th);
    });
    thead.appendChild(hr);
    table.appendChild(thead);

    var tbody = el("tbody");
    compareRows(list).forEach(function (row) {
      var tr = el("tr");
      tr.appendChild(el("th", "cmp__k", row[0]));
      /* mark the leader on any row that is a plain "bigger is more" number */
      var best = null;
      if (row[2]) {
        list.forEach(function (a) {
          if (a[row[2]] != null && (best == null || a[row[2]] > best)) best = a[row[2]];
        });
      }
      list.forEach(function (a) {
        var td = el("td", "cmp__v" + (row[2] && best != null && a[row[2]] === best ? " is-best" : ""));
        td.textContent = row[1](a);
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    scroller.appendChild(table);
    body.appendChild(scroller);
    sheet.appendChild(body);

    $scrim.appendChild(sheet);
    $scrim.hidden = false;
    document.body.style.overflow = "hidden";
    close.focus();
  }

  /* ------------------------------------------------------------------ cards */

  function card(a) {
    var mil = isMil(a);
    var wrap = el("div", "cardwrap" + (inCompare(a.id) ? " is-picked" : ""));
    wrap.setAttribute("role", "listitem");
    var pick = el("button", "card__pick", inCompare(a.id) ? "\u2713" : "+");
    pick.type = "button";
    pick.setAttribute("aria-pressed", inCompare(a.id) ? "true" : "false");
    pick.setAttribute("aria-label", (inCompare(a.id) ? t("compareRemove") : t("compareAdd")) +
      " — " + a.model);
    pick.addEventListener("click", function (e) {
      e.stopPropagation();
      toggleCompare(a.id);
    });

    var b = el("button", "card t-" + a.type);
    b.type = "button";
    b.dataset.id = a.id;

    if (HAS_PHOTOS) {
    var shot = el("figure", "card__shot");
    var src = photoSrc(a, "thumb");
    if (src) {
      var img = new Image();
      img.loading = "lazy";
      img.decoding = "async";
      img.alt = "";
      img.src = src;
      img.addEventListener("error", function () { shot.classList.add("is-empty"); });
      shot.appendChild(img);
    } else {
      shot.classList.add("is-empty");
      shot.appendChild(silhouette());
    }
    b.appendChild(shot);
    }

    var head = el("div", "card__head");
    var top = el("div");
    top.appendChild(el("span", "card__mfr", a.mfr));
    top.appendChild(el("span", "card__model", a.model));
    head.appendChild(top);
    if (a.iran) head.appendChild(el("span", "card__flag", "IRAN"));
    b.appendChild(head);

    var tags = el("div", "tags");
    tags.appendChild(el("span", "tag tag--type", typeLabel(a.type)));
    if (a.engineKind !== "jet" && engineLabel(a.engineKind) !== typeLabel(a.type)) {
      tags.appendChild(el("span", "tag", engineLabel(a.engineKind)));
    }
    var st = statusOf(a.status);
    tags.appendChild(el("span", "tag " + st.cls, st.label));
    b.appendChild(tags);

    var foot = el("div", "card__foot");

    /* one bar per card, scaled within its own category: cabin size for an
       airliner, top speed for a combat aircraft */
    var val = mil ? a.speedKmh : a.seatsTypical;
    var max = mil ? MAX_SPEED : MAX_SEATS;
    if (val) {
      var track = el("div", "seatbar");
      var fill = el("div", "seatbar__fill");
      fill.style.width = Math.max(3, val / max * 100).toFixed(1) + "%";
      track.appendChild(fill);
      track.title = mil ? t("barSpeed") : t("barSeats");
      foot.appendChild(track);
    }

    var specs = el("div", "card__specs");
    var rows = mil
      ? [[t("kCrew"), a.crew == null ? "—" : a.crew === 0 ? t("uncrewed") : d(a.crew),
          a.crew === 0 ? "" : t("uCrew")],
         [t("kSpeed"), num(a.speedKmh), t("uKmh")],
         [t("kIntro"), a.introduced ? d(a.introduced) : "—", t("uYear")]]
      : [[t("kSeats"), a.seatsTypical == null ? "—" : num(a.seatsTypical), t("uPax")],
         [t("kRange"), num(a.rangeKm), t("uKm")],
         [t("kIntro"), a.introduced ? d(a.introduced) : "—", t("uYear")]];
    rows.forEach(function (p) {
      var cell = el("div");
      cell.appendChild(el("span", "spec__k", p[0]));
      var v = el("span", "spec__v", p[1] + " ");
      if (p[2]) v.appendChild(el("small", null, p[2]));
      cell.appendChild(v);
      specs.appendChild(cell);
    });
    foot.appendChild(specs);
    b.appendChild(foot);

    b.addEventListener("click", function () { openSheet(a); });
    wrap.appendChild(b);
    wrap.appendChild(pick);
    return wrap;
  }

  function render(keepPage) {
    if (!keepPage) shown = PAGE;
    buildFilters();
    buildTimeline();
    var list = results();
    var slice = list.slice(0, shown);

    var frag = document.createDocumentFragment();
    slice.forEach(function (a) { frag.appendChild(card(a)); });
    $grid.textContent = "";
    $grid.appendChild(frag);

    $count.textContent = d(list.length);
    $empty.hidden = list.length > 0;
    $clear.classList.toggle("on", !!state.q);

    $more.hidden = list.length <= shown;
    if (!$more.hidden) {
      var next = Math.min(PAGE, list.length - shown);
      var rest = list.length - shown;
      $more.querySelector("span").textContent = lang === "fa"
        ? "نمایش " + d(next) + " مورد دیگر — " + d(rest) + " باقی‌مانده"
        : "Show " + next + " more — " + rest + " remaining";
    }
  }

  $more.addEventListener("click", function () { shown += PAGE; render(true); });
  document.getElementById("csvBtn").addEventListener("click", exportCsv);
  document.getElementById("jsonBtn").addEventListener("click", exportJson);
  document.getElementById("aboutBtn").addEventListener("click", openAbout);

  /* ------------------------------------------------------------ detail sheet */

  /* a size reference the reader already has a feel for, one per category */
  var REF_CIVIL = { label: "Airbus A320", lengthM: 37.6, spanM: 35.8, heightM: 11.8 };
  var REF_MIL   = { label: "F-16C", lengthM: 15.0, spanM: 9.96, heightM: 4.88 };

  function silhouette() {
    var ns = "http://www.w3.org/2000/svg";
    var svg = document.createElementNS(ns, "svg");
    svg.setAttribute("viewBox", "0 0 120 60");
    svg.setAttribute("fill", "currentColor");
    var p = document.createElementNS(ns, "path");
    p.setAttribute("d", "M60 4c2.6 0 4.4 4.6 4.8 12.4L110 32v4.4l-45 -8.6v14l10.5 7.4V52L60 48.4 44.5 52v-2.8L55 41.8v-14L10 36.4V32l45.2 -15.6C55.6 8.6 57.4 4 60 4Z");
    svg.appendChild(p);
    return svg;
  }

  function specRow(k, v, isFa) {
    var row = el("div");
    row.appendChild(el("dt", null, k));
    row.appendChild(el("dd", isFa && lang === "fa" ? "fa-val" : null, v));
    return row;
  }

  function scaleRow(label, value, ref, unit, refLabel) {
    var row = el("div", "scale__row");
    row.appendChild(el("div", "scale__label", label));
    var track = el("div", "scale__track");
    var max = Math.max(value || 0, ref) * 1.06;
    var bar = el("div", "scale__bar");
    bar.style.width = ((value || 0) / max * 100).toFixed(1) + "%";
    track.appendChild(bar);
    var tick = el("div", "scale__tick");
    tick.style.insetInlineStart = (ref / max * 100).toFixed(1) + "%";
    tick.title = refLabel + ": " + ref + " m";
    track.appendChild(tick);
    row.appendChild(track);
    row.appendChild(el("div", "scale__num", (value == null ? "—" : d(value)) + " " + unit));
    return row;
  }

  function loadPhoto(a, figure) {
    var local = photoSrc(a, "");
    if (local) {
      var big = new Image();
      big.alt = a.model;
      big.onload = function () {
        figure.textContent = "";
        figure.classList.remove("is-empty");
        figure.appendChild(big);
        figure.appendChild(el("figcaption", null, photoCredit(a)));
      };
      big.onerror = function () { fetchRemote(a, figure); };
      big.src = local;
      return;
    }
    fetchRemote(a, figure);
  }

  function fetchRemote(a, figure) {
    function fail() {
      var msg = figure.querySelector(".photo-fallback span");
      if (msg) msg.textContent = t("photoNone");
      figure.classList.add("is-empty");
    }
    var title = encodeURIComponent(a.wiki || a.model);
    fetch("https://en.wikipedia.org/api/rest_v1/page/summary/" + title, {
      headers: { Accept: "application/json" }
    })
      .then(function (r) { return r.ok ? r.json() : Promise.reject(); })
      .then(function (j) {
        var src = (j.originalimage && j.originalimage.source) ||
                  (j.thumbnail && j.thumbnail.source);
        if (!src) { fail(); return; }
        var img = new Image();
        img.alt = a.model;
        img.onload = function () {
          figure.textContent = "";
          figure.classList.remove("is-empty");
          figure.appendChild(img);
          figure.appendChild(el("figcaption", null, t("photoCredit") + (a.wiki || a.model)));
        };
        img.onerror = fail;
        img.src = src;
      })
      .catch(fail);
  }

  function photoSrc(a, size) {
    if (INLINE[a.id]) return INLINE[a.id];
    if (!PHOTOS[a.id]) return null;
    return "assets/photos/" + (size ? size + "/" : "") + a.id + ".webp";
  }

  function photoCredit(a) {
    var meta = PHOTOS[a.id];
    if (!meta) return t("photoCredit") + (a.wiki || a.model);
    return meta.credit + " · " + meta.licence + " · Wikimedia Commons";
  }

  var lastFocus = null;

  function openSheet(a) {
    var mil = isMil(a);
    lastFocus = document.activeElement;
    $scrim.textContent = "";

    var sheet = el("div", "sheet t-" + a.type);

    var fig = el("figure", "sheet__photo");
    var fb = el("div", "photo-fallback");
    fb.appendChild(silhouette());
    fb.appendChild(el("span", null, t("photoLoading")));
    fig.appendChild(fb);
    sheet.appendChild(fig);
    loadPhoto(a, fig);

    var head = el("div", "sheet__head");
    var title = el("div", "sheet__title");
    title.appendChild(el("span", "card__mfr", a.mfr + " · " + countryLabel(a.country)));
    var h2 = el("h2", null, a.model);
    h2.id = "sheetTitle";
    title.appendChild(h2);
    var role = field(a, "role");
    if (role) title.appendChild(el("p", "sheet__role", role));
    var tags = el("div", "tags");
    tags.appendChild(el("span", "tag tag--type", typeLabel(a.type)));
    tags.appendChild(el("span", "tag", engineLabel(a.engineKind)));
    var st = statusOf(a.status);
    tags.appendChild(el("span", "tag " + st.cls, st.label));
    if (a.iran) tags.appendChild(el("span", "tag tag--iran", t("inIran")));
    if (a.family) tags.appendChild(el("span", "tag", t("familyTag") + a.family));
    title.appendChild(tags);
    head.appendChild(title);

    var close = el("button", "close-btn");
    close.type = "button";
    close.setAttribute("aria-label", t("closeAria"));
    close.innerHTML = '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m6 6 12 12M18 6 6 18"/></svg>';
    close.addEventListener("click", closeSheet);
    head.appendChild(close);
    sheet.appendChild(head);

    var body = el("div", "sheet__body");
    var notes = field(a, "notes");
    if (notes) body.appendChild(el("p", "note", notes));

    var s1 = el("section");
    s1.appendChild(el("h3", "sectitle", mil ? t("secPerfMil") : t("secPerfCivil")));
    var g1 = el("dl", "specgrid");
    if (mil) {
      g1.appendChild(specRow(t("lCrew"),
        a.crew == null ? "—" : a.crew === 0 ? t("uncrewed")
                                            : (d(a.crew) + " " + t("uCrew")).trim(), true));
      g1.appendChild(specRow(t("lMaxSpeed"), num(a.speedKmh) + " km/h"));
      g1.appendChild(specRow(t("lRange"), num(a.rangeKm) + " km"));
      g1.appendChild(specRow(t("lCeiling"), num(a.ceilingM) + " m"));
      g1.appendChild(specRow(t("lMtow"), num(a.mtowKg) + " kg"));
    } else {
      g1.appendChild(specRow(t("lSeatsTyp"), a.seatsTypical == null ? "—" : num(a.seatsTypical) + " " + t("uPax"), true));
      g1.appendChild(specRow(t("lSeatsMax"), a.seatsMax == null ? "—" : num(a.seatsMax) + " " + t("uPax"), true));
      g1.appendChild(specRow(t("lRange"), num(a.rangeKm) + " km"));
      g1.appendChild(specRow(t("lCruise"), num(a.speedKmh) + " km/h"));
      g1.appendChild(specRow(t("lMtow"), num(a.mtowKg) + " kg"));
    }
    s1.appendChild(g1);
    body.appendChild(s1);

    var arm = field(a, "armament");
    if (arm) {
      var s0 = el("section");
      s0.appendChild(el("h3", "sectitle", t("secArm")));
      s0.appendChild(el("p", "armament", faNumbersIn(arm)));
      body.appendChild(s0);
    }

    var ref = mil ? REF_MIL : REF_CIVIL;
    var s2 = el("section");
    s2.appendChild(el("h3", "sectitle", t("secDims")));
    var scale = el("div", "scale");
    scale.appendChild(scaleRow(t("lLength"), a.lengthM, ref.lengthM, "m", ref.label));
    scale.appendChild(scaleRow(t("lSpan"), a.spanM, ref.spanM, "m", ref.label));
    scale.appendChild(scaleRow(t("lHeight"), a.heightM, ref.heightM, "m", ref.label));
    scale.appendChild(el("p", "scale__legend", lang === "fa"
      ? "خط عمودی روی هر نوار، اندازه‌ی متناظر " + ref.label + " را برای مقایسه نشان می‌دهد."
      : "The tick on each bar marks the matching dimension of a " + ref.label + " for comparison."));
    s2.appendChild(scale);
    body.appendChild(s2);

    var s3 = el("section");
    s3.appendChild(el("h3", "sectitle", t("secEngine")));
    var g3 = el("dl", "specgrid");
    g3.appendChild(specRow(t("lEngines"),
      (a.engineCount == null ? "—" : d(a.engineCount)) + " × " + engineLabel(a.engineKind), true));
    g3.appendChild(specRow(t("lEngineModel"), a.engineModel || "—"));
    g3.appendChild(specRow(t("lFirstFlight"), a.firstFlight ? d(a.firstFlight) : "—", true));
    g3.appendChild(specRow(t("lIntroduced"), a.introduced ? d(a.introduced) : "—", true));
    var builtRow = specRow(t("lBuilt"),
      a.built == null ? "—" : (num(a.built) + " " + t("uFrames")).trim(), true);
    if (a.builtFamily) {
      var qual = el("small", "qual", " · " + t("familyCount"));
      qual.title = t("familyCountTip");
      builtRow.querySelector("dd").appendChild(qual);
    }
    g3.appendChild(builtRow);
    s3.appendChild(g3);
    body.appendChild(s3);

    var links = el("div", "sheet__links");
    var wl = el("a", "linkbtn", t("wikiBtn"));
    wl.href = "https://en.wikipedia.org/wiki/" + encodeURIComponent((a.wiki || a.model).replace(/ /g, "_"));
    wl.target = "_blank";
    wl.rel = "noopener";
    links.appendChild(wl);

    var fam = el("button", "linkbtn");
    fam.type = "button";
    fam.textContent = t("familyBtn") + (a.family || a.mfr);
    fam.addEventListener("click", function () {
      closeSheet();
      $q.value = a.family || a.mfr;
      state.q = $q.value;
      state.cat = ""; state.type = ""; state.engine = ""; state.iran = false; state.prod = false;
      render();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
    links.appendChild(fam);

    var share = el("button", "linkbtn");
    share.type = "button";
    share.textContent = t("shareBtn");
    share.addEventListener("click", function () {
      var url = location.origin + location.pathname + location.search + "#/" + a.id;
      var done = function () {
        share.textContent = t("shareDone");
        setTimeout(function () { share.textContent = t("shareBtn"); }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(done, function () {});
      }
    });
    links.appendChild(share);

    var stamp = el("div", "sheet__stamp");
    stamp.innerHTML = '<svg class="mark" viewBox="0 0 48 48" aria-hidden="true">' +
      '<g fill="currentColor"><path d="M19.4 42a1.1 1.1 0 0 1-1.1-1.2l4.9-28.6h7.4v28.7a1.1 1.1 0 0 1-1.1 1.1Z"/>' +
      '<path d="M4.6 7.4h38.8a2.3 2.3 0 0 1 2.2 2.9l-.3 1a1.9 1.9 0 0 1-1.9 1.4H4.6a1.9 1.9 0 0 1-1.9-1.4l-.3-1a2.3 2.3 0 0 1 2.2-2.9Z"/></g></svg>';
    stamp.appendChild(el("span", "wordmark", "T-AIR"));
    links.appendChild(stamp);
    body.appendChild(links);

    sheet.appendChild(body);
    $scrim.appendChild(sheet);
    $scrim.hidden = false;
    document.body.style.overflow = "hidden";
    close.focus();

    /* the open aircraft becomes the address, so a card can be linked to */
    if (location.hash !== "#/" + a.id) {
      history.pushState({ id: a.id }, "", "#/" + a.id);
    }
  }

  function closeSheet() {
    $scrim.hidden = true;
    $scrim.textContent = "";
    document.body.style.overflow = "";
    if (location.hash.indexOf("#/") === 0) {
      history.pushState({}, "", location.pathname + location.search);
    }
    if (lastFocus) lastFocus.focus();
  }

  function openFromHash() {
    var id = location.hash.indexOf("#/") === 0 ? location.hash.slice(2) : "";
    var a = id && byId[id];
    if (a) { if ($scrim.hidden) openSheet(a); }
    else if (!$scrim.hidden) closeSheet();
  }

  window.addEventListener("popstate", function () {
    var id = location.hash.indexOf("#/") === 0 ? location.hash.slice(2) : "";
    if (id && byId[id]) { $scrim.hidden = true; openSheet(byId[id]); }
    else if (!$scrim.hidden) {
      $scrim.hidden = true;
      $scrim.textContent = "";
      document.body.style.overflow = "";
    }
  });

  $scrim.addEventListener("click", function (e) {
    if (e.target === $scrim) closeSheet();
  });

  /* arrow keys walk the result grid once a card has focus */
  /* keep Tab inside the open dialog */
  $scrim.addEventListener("keydown", function (e) {
    if (e.key !== "Tab" || $scrim.hidden) return;
    var f = $scrim.querySelectorAll('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])');
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  document.addEventListener("keydown", function (e) {
    var cards = null, i = -1;
    if (["ArrowRight", "ArrowLeft", "ArrowDown", "ArrowUp"].indexOf(e.key) > -1 &&
        $scrim.hidden && document.activeElement &&
        document.activeElement.classList.contains("card")) {
      cards = Array.prototype.slice.call($grid.querySelectorAll(".card"));
      i = cards.indexOf(document.activeElement);
      var perRow = Math.max(1, Math.round($grid.clientWidth /
        (cards[0] ? cards[0].parentNode.offsetWidth + 14 : 300)));
      var rtl = document.documentElement.dir === "rtl";
      var step = { ArrowDown: perRow, ArrowUp: -perRow,
                   ArrowRight: rtl ? -1 : 1, ArrowLeft: rtl ? 1 : -1 }[e.key];
      var next = cards[i + step];
      if (next) { e.preventDefault(); next.focus(); }
      return;
    }
    if (e.key === "Escape" && !$scrim.hidden) closeSheet();
    if (e.key === "/" && document.activeElement !== $q) {
      e.preventDefault();
      $q.focus();
      $q.select();
    }
  });

  /* ---------------------------------------------------------------- export */

  /* The artifact viewer runs the page in an iframe and blocks page-initiated
     downloads, so say that plainly instead of failing silently. */
  var EMBEDDED = (function () {
    try { return window.self !== window.top; } catch (e) { return true; }
  })();

  var EXPORT_FIELDS = ["id", "category", "type", "mfr", "model", "family", "country",
                       "firstFlight", "introduced", "status", "seatsTypical", "seatsMax",
                       "crew", "rangeKm", "speedKmh", "ceilingM", "mtowKg",
                       "lengthM", "spanM", "heightM", "engineCount", "engineKind",
                       "engineModel", "built", "builtFamily", "iran", "wiki",
                       "role", "role_en", "armament", "armament_en", "notes", "notes_en"];

  function csvCell(v) {
    if (v == null) return "";
    var s = String(v);
    return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
  }

  /* The claude.ai viewer mediates saves through its own capability; a hosted
     or local copy has no such host and uses an object URL. Ask once. */
  var dlNs = null, dlAsked = false;
  function downloadsHost() {
    if (dlAsked) return Promise.resolve(dlNs);
    dlAsked = true;
    if (!(window.claude && typeof window.claude.use === "function")) {
      return Promise.resolve(null);
    }
    return window.claude.use("downloads").then(
      function (ns) { dlNs = ns; return ns; },
      function () { return null; }
    );
  }

  function download(name, text, mime) {
    downloadsHost().then(function (ns) {
      if (ns) {
        ns.save({ filename: name, data: text }).then(
          function () { toast(t("exportSaved")); },
          function (err) {
            var code = err && err.code;
            if (code === "declined" || code === "rate_limited") return;
            toast(code === "extension_not_enabled" || code === "rejected_extension"
              ? t("exportCsvBlocked") : t("exportBlocked"));
          }
        );
        return;
      }
      saveViaLink(name, text, mime);
    });
  }

  function saveViaLink(name, text, mime) {
    if (EMBEDDED) { toast(t("exportBlocked")); return; }
    var blob = new Blob(["\ufeff" + text], { type: mime + ";charset=utf-8" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
  }

  var toastTimer;
  function toast(msg) {
    var box = document.getElementById("toast");
    box.textContent = msg;
    box.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { box.hidden = true; }, 4200);
  }

  function exportCsv() {
    var list = results();
    var rows = [EXPORT_FIELDS.join(",")];
    list.forEach(function (a) {
      rows.push(EXPORT_FIELDS.map(function (f) { return csvCell(a[f]); }).join(","));
    });
    download("t-air-" + list.length + ".csv", rows.join("\n"), "text/csv");
  }

  function exportJson() {
    var list = results().map(function (a) {
      var o = {};
      EXPORT_FIELDS.forEach(function (f) { if (a[f] != null) o[f] = a[f]; });
      return o;
    });
    download("t-air-" + list.length + ".json",
             JSON.stringify({ source: "T-AIR", count: list.length, aircraft: list }, null, 1),
             "application/json");
  }

  /* ----------------------------------------------------------------- about */

  function openAbout() {
    lastFocus = document.activeElement;
    $scrim.textContent = "";
    var sheet = el("div", "sheet sheet--about");

    var head = el("div", "sheet__head");
    var title = el("div", "sheet__title");
    title.appendChild(el("span", "card__mfr", "T-AIR"));
    var h2 = el("h2", null, t("aboutTitle"));
    h2.id = "sheetTitle";
    h2.style.fontFamily = "var(--fa)";
    title.appendChild(h2);
    head.appendChild(title);
    var close = el("button", "close-btn");
    close.type = "button";
    close.setAttribute("aria-label", t("closeAria"));
    close.innerHTML = '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m6 6 12 12M18 6 6 18"/></svg>';
    close.addEventListener("click", closeSheet);
    head.appendChild(close);
    sheet.appendChild(head);

    var body = el("div", "sheet__body prose");
    var civ = DATA.filter(function (a) { return a.category === "civil"; }).length;
    var fam = DATA.filter(function (a) { return a.builtFamily; }).length;
    var mfrs = {};
    DATA.forEach(function (a) { mfrs[a.mfr] = 1; });
    body.innerHTML = aboutHtml({
      total: d(DATA.length), civil: d(civ), mil: d(DATA.length - civ),
      mfrs: d(Object.keys(mfrs).length),
      iran: d(DATA.filter(function (a) { return a.iran; }).length),
      family: d(fam)
    });
    sheet.appendChild(body);

    $scrim.appendChild(sheet);
    $scrim.hidden = false;
    document.body.style.overflow = "hidden";
    close.focus();
  }

  function aboutHtml(n) {
    if (lang === "fa") {
      return [
        "<p>T-AIR یک مرجع سریع مشخصات هواپیماست: " + n.total + " مدل (" + n.civil +
        " غیرنظامی، " + n.mil + " نظامی) از " + n.mfrs + " سازنده، که " + n.iran +
        " فروندشان در ناوگان ایران بوده‌اند.</p>",
        "<h4>منابع</h4>",
        "<p>ارقام از مواد عمومی سازندگان و دانشنامه‌ها گردآوری شده است. این یک مرجع " +
        "سریع است، نه سند عملیاتی؛ برای هر کاربرد واقعی به اسناد رسمی سازنده مراجعه کنید.</p>",
        "<h4>قراردادها</h4>",
        "<ul>",
        "<li><b>نسخه در برابر خانواده</b> — هر رکورد یک نسخه است، ولی گاهی تنها عددِ " +
        "منتشرشده برای کل خانواده وجود دارد. " + n.family + " رکورد این‌طورند و کنار " +
        "عددشان «کل خانواده» نوشته شده است.</li>",
        "<li><b>برد</b> — برد استاندارد بدون مخزن کمکی؛ برای نظامی‌ها گاهی برد فِری است، نه شعاع عملیاتی.</li>",
        "<li><b>سرعت</b> — برای مسافربری سرعت سفر، برای نظامی سرعت بیشینه.</li>",
        "<li><b>دهانه بال</b> — برای بالگردها قطر روتور اصلی ثبت شده است.</li>",
        "<li><b>خدمه</b> — برای پهپادها صفر است؛ این یک مقدار خالی نیست، خودِ تعریف این دسته است.</li>",
        "<li><b>سقف پرواز</b> — سقف سرویس، نه سقف شناوری بالگرد.</li>",
        "</ul>",
        "<h4>ممیزی</h4>",
        "<p>اصلاحات داده به‌صورت لایه‌ی جدا در <code>scripts/fixes/</code> ثبت می‌شود، " +
        "نه ویرایش مستقیم جدول‌ها، تا معلوم بماند چه چیزی و چرا عوض شده. هر فایل یک " +
        "فهرست <code>UNRESOLVED</code> هم دارد: مواردی که هنوز حل نشده‌اند.</p>",
        "<h4>عکس‌ها</h4>",
        "<p>عکس‌ها از ویکی‌مدیا کامانز می‌آیند و فقط فایل‌هایی برداشته می‌شوند که " +
        "مجوز آزاد دارند. نام عکاس و مجوز زیر هر عکس نوشته می‌شود.</p>",
        "<h4>خروجی داده</h4>",
        "<p>دکمه‌های CSV و JSON بالای نتایج، همان مجموعه‌ای را که فیلتر کرده‌اید " +
        "بیرون می‌دهند. داخل نمای درون‌قابی کار نمی‌کنند؛ نسخه‌ی میزبانی‌شده یا فایل محلی را باز کنید.</p>"
      ].join("");
    }
    return [
      "<p>T-AIR is a quick specification reference: " + n.total + " aircraft (" + n.civil +
      " civil, " + n.mil + " military) from " + n.mfrs + " manufacturers, " + n.iran +
      " of which have flown in Iranian service.</p>",
      "<h4>Sources</h4>",
      "<p>Figures are compiled from manufacturers' public material and reference works. " +
      "This is a quick reference, not an operational document; for any real use, go to " +
      "the manufacturer's own documentation.</p>",
      "<h4>Conventions</h4>",
      "<ul>",
      "<li><b>Variant vs family</b> — each record is one variant, but sometimes the only " +
      "published production figure covers the whole family. " + n.family + " records are " +
      "in that position and are marked <i>family total</i> next to the number.</li>",
      "<li><b>Range</b> — standard range without auxiliary tanks; for military types this " +
      "is sometimes ferry range rather than combat radius.</li>",
      "<li><b>Speed</b> — cruise speed for airliners, maximum speed for military aircraft.</li>",
      "<li><b>Wingspan</b> — for helicopters this holds the main rotor diameter.</li>",
      "<li><b>Crew</b> — zero for uncrewed aircraft. That is the definition of the class, " +
      "not a missing value.</li>",
      "<li><b>Ceiling</b> — service ceiling, not a helicopter's hover ceiling.</li>",
      "</ul>",
      "<h4>Auditing</h4>",
      "<p>Corrections are recorded as a separate layer in <code>scripts/fixes/</code> rather " +
      "than edited into the source tables, so what changed and why stays readable. Each file " +
      "also carries an <code>UNRESOLVED</code> list of questions still open.</p>",
      "<h4>Photographs</h4>",
      "<p>Photographs come from Wikimedia Commons, and only files under a free licence are " +
      "used. The photographer and licence are printed under each picture.</p>",
      "<h4>Data export</h4>",
      "<p>The CSV and JSON buttons above the results export exactly the set you have " +
      "filtered to. They do not work inside the embedded viewer — open the hosted or local copy.</p>"
    ].join("");
  }

  /* ------------------------------------------------------------------ boot */

  var timer;
  $q.addEventListener("input", function () {
    clearTimeout(timer);
    timer = setTimeout(function () { state.q = $q.value; render(); }, 90);
  });
  $clear.addEventListener("click", function () {
    $q.value = ""; state.q = ""; render(); $q.focus();
  });

  function buildStats() {
    var civ = DATA.filter(function (a) { return a.category === "civil"; }).length;
    var rows = [
      [t("statModels"), DATA.length, ""],
      [t("statCivil"), civ, ""],
      [t("statMil"), DATA.length - civ, ""],
      [t("statIran"), DATA.filter(function (a) { return a.iran; }).length, "is-iran"]
    ];
    var $stats = document.getElementById("stats");
    $stats.textContent = "";
    rows.forEach(function (r) {
      var cell = el("div");
      cell.appendChild(el("dt", null, r[0]));
      cell.appendChild(el("dd", r[2] || null, d(r[1])));
      $stats.appendChild(cell);
    });
  }

  /* the dock only earns its shadow once it is actually pinned */
  var sentinel = document.getElementById("dockSentinel");
  var dock = document.getElementById("dock");
  if (window.IntersectionObserver && sentinel) {
    new IntersectionObserver(function (entries) {
      dock.classList.toggle("is-stuck", !entries[0].isIntersecting);
    }, { threshold: 0 }).observe(sentinel);
  }

  function boot(data) {
    HAS_PHOTOS = Object.keys(PHOTOS).length > 0 || Object.keys(INLINE).length > 0;
    DATA = data.map(function (a) {
      a._hay = haystack(a);
      a._model = norm(a.model);
      byId[a.id] = a;
      return a;
    });
    MAX_SEATS = DATA.reduce(function (m, a) { return Math.max(m, a.seatsTypical || 0); }, 1);
    MAX_SPEED = DATA.reduce(function (m, a) {
      return isMil(a) ? Math.max(m, a.speedKmh || 0) : m;
    }, 1);
    buildStats();
    buildTray();
    render();
    openFromHash();
  }

  applyLang();

  function loadPhotoIndex() {
    if (window.__PHOTOS__) {
      PHOTOS = window.__PHOTOS__.photos || {};
      return Promise.resolve();
    }
    return fetch("data/photos.json")
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) { if (j) PHOTOS = j.photos || {}; })
      .catch(function () { /* no local library yet */ });
  }

  if (window.__AIRCRAFT__) {
    PHOTOS = (window.__PHOTOS__ || {}).photos || {};
    boot(window.__AIRCRAFT__.aircraft);
  } else {
    Promise.all([
      fetch("data/aircraft.json").then(function (r) { return r.json(); }),
      loadPhotoIndex()
    ])
      .then(function (res) { boot(res[0].aircraft); })
      .catch(function () {
        $empty.hidden = false;
        $empty.querySelector("strong").textContent = t("loadFail");
      });
  }
})();
