// 高德矢量瓦片 amap vector tile 的 websocket 解析暂停
// 一个人解析实在无趣 如有志同道合的朋友可以加QQ 34⑦5020⑦⑦
// 或给我发email adodo1#126.com
self._wkHandlers = {};
(function d(a) {
    function b(c, d) {
        function f(a, b, c) {
            a = {
                Ko: Date.now(),
                Fo: h,
                error: a,
                result: b
            };
            if (c)
                for (var g in c)
                    c.hasOwnProperty(g) && (a[g] = c[g]);
            d(a)
        }
        var g = c.MA
          , h = c.Fo
          , l = c.Hz
          , m = c.pq
          , v = c.pW || []
          , s = a._wkHandlers[g];
        s ? s[l] ? m ? s[l].apply(s, v.concat(f)) : f(null, s[l].apply(s, v)) : f("Unknown cmd: " + l) : f("Can not find handler for: " + g)
    }
    var c = [];
    a.Ct = function(a) {
        c.push.apply(c, a)
    }
    ;
    a.addEventListener("message", function(d) {
        function f(b) {
            if (w) {
                w.push(b);
                var d = !!b.P_;
                d || u++;
                if (u > h)
                    console.error("Resp len wrong!!");
                else if (b = u === h,
                d || b) {
                    d = 1 < w.length ? {
                        t1: w
                    } : w[0];
                    d.Ko = Date.now();
                    d.p7 = t;
                    if (c.length) {
                        try {
                            a.postMessage(d, c)
                        } catch (g) {
                            a.postMessage(d),
                            console.error(g)
                        }
                        c.length = 0
                    } else
                        a.postMessage(d);
                    w.length = 0;
                    b && (f = w = null)
                }
            } else
                console.error("Seemed callback already sent!!")
        }
        var g = d.data;
        d = g.q1 || [g];
        for (var h = d.length, u = 0, t = Date.now() - g.Ko, w = [], g = 0; g < h; g++)
            b(d[g], f)
    }, !1)
}
)(self);
;


function _prep_h4() {
    function a(b, c, d) {
        for (var f = 0, g = d.length; f < g; f++) {
            var h = d.charCodeAt(f);
            if (128 > h)
                b.setUint8(c++, h >>> 0 & 127 | 0);
            else if (2048 > h)
                b.setUint8(c++, h >>> 6 & 31 | 192),
                b.setUint8(c++, h >>> 0 & 63 | 128);
            else if (65536 > h)
                b.setUint8(c++, h >>> 12 & 15 | 224),
                b.setUint8(c++, h >>> 6 & 63 | 128),
                b.setUint8(c++, h >>> 0 & 63 | 128);
            else if (1114112 > h)
                b.setUint8(c++, h >>> 18 & 7 | 240),
                b.setUint8(c++, h >>> 12 & 63 | 128),
                b.setUint8(c++, h >>> 6 & 63 | 128),
                b.setUint8(c++, h >>> 0 & 63 | 128);
            else
                throw Error("bad codepoint " + h);
        }
    }
    function c(a, b, c) {
        var d = ""
          , f = b;
        for (b += c; f < b; f++)
            if (c = a.getUint8(f),
            0 === (c & 128))
                d += String.fromCharCode(c);
            else if (192 === (c & 224))
                d += String.fromCharCode((c & 15) << 6 | a.getUint8(++f) & 63);
            else if (224 === (c & 240))
                d += String.fromCharCode((c & 15) << 12 | (a.getUint8(++f) & 63) << 6 | (a.getUint8(++f) & 63) << 0);
            else if (240 === (c & 248))
                d += String.fromCharCode((c & 7) << 18 | (a.getUint8(++f) & 63) << 12 | (a.getUint8(++f) & 63) << 6 | (a.getUint8(++f) & 63) << 0);
            else
                throw Error("Invalid byte " + c.toString(16));
        return d
    }
    function d(a) {
        for (var b = 0, c = 0, d = a.length; c < d; c++) {
            var f = a.charCodeAt(c);
            if (128 > f)
                b += 1;
            else if (2048 > f)
                b += 2;
            else if (65536 > f)
                b += 3;
            else if (1114112 > f)
                b += 4;
            else
                throw Error("bad codepoint " + f);
        }
        return b
    }
    function f(a, b) {
        this.offset = b || 0;
        this.view = a
    }
    function g(c, f, h) {
        var k = typeof c;
        if ("string" === k) {
            var q = d(c);
            if (32 > q)
                return f.setUint8(h, q | 160),
                a(f, h + 1, c),
                1 + q;
            if (256 > q)
                return f.setUint8(h, 217),
                f.setUint8(h + 1, q),
                a(f, h + 2, c),
                2 + q;
            if (65536 > q)
                return f.setUint8(h, 218),
                f.setUint16(h + 1, q),
                a(f, h + 3, c),
                3 + q;
            if (4294967296 > q)
                return f.setUint8(h, 219),
                f.setUint32(h + 1, q),
                a(f, h + 5, c),
                5 + q
        }
        if (c instanceof ArrayBuffer) {
            q = c.byteLength;
            if (256 > q)
                return f.setUint8(h, 196),
                f.setUint8(h + 1, q),
                (new Uint8Array(f.buffer)).set(new Uint8Array(c), h + 2),
                2 + q;
            if (65536 > q)
                return f.setUint8(h, 197),
                f.setUint16(h + 1, q),
                (new Uint8Array(f.buffer)).set(new Uint8Array(c), h + 3),
                3 + q;
            if (4294967296 > q)
                return f.setUint8(h, 198),
                f.setUint32(h + 1, q),
                (new Uint8Array(f.buffer)).set(new Uint8Array(c), h + 5),
                5 + q
        }
        if ("number" === k) {
            if (c << 0 !== c)
                return f.setUint8(h, 203),
                f.setFloat64(h + 1, c),
                9;
            if (0 <= c) {
                if (128 > c)
                    return f.setUint8(h, c),
                    1;
                if (256 > c)
                    return f.setUint8(h, 204),
                    f.setUint8(h + 1, c),
                    2;
                if (65536 > c)
                    return f.setUint8(h, 205),
                    f.setUint16(h + 1, c),
                    3;
                if (4294967296 > c)
                    return f.setUint8(h, 206),
                    f.setUint32(h + 1, c),
                    5;
                throw Error("Number too big 0x" + c.toString(16));
            }
            if (-32 <= c)
                return f.setInt8(h, c),
                1;
            if (-128 <= c)
                return f.setUint8(h, 208),
                f.setInt8(h + 1, c),
                2;
            if (-32768 <= c)
                return f.setUint8(h, 209),
                f.setInt16(h + 1, c),
                3;
            if (-2147483648 <= c)
                return f.setUint8(h, 210),
                f.setInt32(h + 1, c),
                5;
            throw Error("Number too small -0x" + (-c).toString(16).substr(1));
        }
        if ("undefined" === k)
            return f.setUint8(h, 212),
            f.setUint8(h + 1, 0),
            f.setUint8(h + 2, 0),
            3;
        if (null === c)
            return f.setUint8(h, 192),
            1;
        if ("boolean" === k)
            return f.setUint8(h, c ? 195 : 194),
            1;
        if ("object" === k) {
            var k = 0
              , r = Array.isArray(c)
              , u = null;
            r ? q = c.length : (u = Object.keys(c),
            q = u.length);
            16 > q ? (f.setUint8(h, q | (r ? 144 : 128)),
            k = 1) : 65536 > q ? (f.setUint8(h, r ? 220 : 222),
            f.setUint16(h + 1, q),
            k = 3) : 4294967296 > q && (f.setUint8(h, r ? 221 : 223),
            f.setUint32(h + 1, q),
            k = 5);
            if (r)
                for (r = 0; r < q; r++)
                    k += g(c[r], f, h + k);
            else
                for (r = 0; r < q; r++)
                    var t = u[r]
                      , k = k + g(t, f, h + k)
                      , k = k + g(c[t], f, h + k);
            return k
        }
        throw Error("Unknown type " + k);
    }
    function h(a) {
        var b = typeof a;
        if ("string" === b) {
            var c = d(a);
            if (32 > c)
                return 1 + c;
            if (256 > c)
                return 2 + c;
            if (65536 > c)
                return 3 + c;
            if (4294967296 > c)
                return 5 + c
        }
        if (a instanceof ArrayBuffer) {
            c = a.byteLength;
            if (256 > c)
                return 2 + c;
            if (65536 > c)
                return 3 + c;
            if (4294967296 > c)
                return 5 + c
        }
        if ("number" === b) {
            if (a << 0 !== a)
                return 9;
            if (0 <= a) {
                if (128 > a)
                    return 1;
                if (256 > a)
                    return 2;
                if (65536 > a)
                    return 3;
                if (4294967296 > a)
                    return 5;
                if (1.8446744073709552E19 > a)
                    return 9;
                throw Error("Number too big 0x" + a.toString(16));
            }
            if (-32 <= a)
                return 1;
            if (-128 <= a)
                return 2;
            if (-32768 <= a)
                return 3;
            if (-2147483648 <= a)
                return 5;
            if (-9223372036854775E3 <= a)
                return 9;
            throw Error("Number too small -0x" + a.toString(16).substr(1));
        }
        if ("undefined" === b)
            return 3;
        if ("boolean" === b || null === a)
            return 1;
        if ("object" === b) {
            b = 0;
            if (Array.isArray(a))
                for (var c = a.length, f = 0; f < c; f++)
                    b += h(a[f]);
            else
                for (var g = Object.keys(a), c = g.length, f = 0; f < c; f++)
                    var k = g[f]
                      , b = b + (h(k) + h(a[k]));
            if (16 > c)
                return 1 + b;
            if (65536 > c)
                return 3 + b;
            if (4294967296 > c)
                return 5 + b;
            throw Error("Array or object too long 0x" + c.toString(16));
        }
        throw Error("Unknown type " + b);
    }
    var k = {
        j6: function(a) {
            if (void 0 === a)
                return "undefined";
            var b, c;
            a instanceof ArrayBuffer ? (c = "ArrayBuffer",
            b = new DataView(a)) : a instanceof DataView && (c = "DataView",
            b = a);
            if (!b)
                return JSON.stringify(a);
            for (var d = [], f = 0; f < a.byteLength; f++) {
                if (20 < f) {
                    d.push("...");
                    break
                }
                var g = b.getUint8(f).toString(16);
                1 === g.length && (g = "0" + g);
                d.push(g)
            }
            return "<" + c + " " + d.join(" ") + ">"
        }
    };
    k.S7 = a;
    k.R7 = c;
    k.Q7 = d;
    f.prototype.map = function(a) {
        for (var b = {}, c = 0; c < a; c++) {
            var d = this.parse();
            b[d] = this.parse()
        }
        return b
    }
    ;
    f.prototype.qz = function(a) {
        var b = new ArrayBuffer(a);
        (new Uint8Array(b)).set(new Uint8Array(this.view.buffer,this.offset,a), 0);
        this.offset += a;
        return b
    }
    ;
    f.prototype.Cv = function(a) {
        var b = c(this.view, this.offset, a);
        this.offset += a;
        return b
    }
    ;
    f.prototype.hz = function(a) {
        for (var b = Array(a), c = 0; c < a; c++)
            b[c] = this.parse();
        return b
    }
    ;
    f.prototype.parse = function() {
        var a = this.view.getUint8(this.offset);
        if (160 === (a & 224))
            return this.offset++,
            this.Cv(a & 31);
        if (128 === (a & 240))
            return this.offset++,
            this.map(a & 15);
        if (144 === (a & 240))
            return this.offset++,
            this.hz(a & 15);
        if (0 === (a & 128))
            return this.offset++,
            a;
        if (224 === (a & 224))
            return a = this.view.getInt8(this.offset),
            this.offset++,
            a;
        if (212 === a && 0 === this.view.getUint8(this.offset + 1))
            this.offset += 3;
        else {
            switch (a) {
            case 217:
                return a = this.view.getUint8(this.offset + 1),
                this.offset += 2,
                this.Cv(a);
            case 218:
                return a = this.view.getUint16(this.offset + 1),
                this.offset += 3,
                this.Cv(a);
            case 219:
                return a = this.view.getUint32(this.offset + 1),
                this.offset += 5,
                this.Cv(a);
            case 196:
                return a = this.view.getUint8(this.offset + 1),
                this.offset += 2,
                this.qz(a);
            case 197:
                return a = this.view.getUint16(this.offset + 1),
                this.offset += 3,
                this.qz(a);
            case 198:
                return a = this.view.getUint32(this.offset + 1),
                this.offset += 5,
                this.qz(a);
            case 192:
                return this.offset++,
                null;
            case 194:
                return this.offset++,
                !1;
            case 195:
                return this.offset++,
                !0;
            case 204:
                return a = this.view.getUint8(this.offset + 1),
                this.offset += 2,
                a;
            case 205:
                return a = this.view.getUint16(this.offset + 1),
                this.offset += 3,
                a;
            case 206:
                return a = this.view.getUint32(this.offset + 1),
                this.offset += 5,
                a;
            case 207:
                var a = this.view.getUint32(this.offset + 1)
                  , b = this.view.getUint32(this.offset + 5);
                this.offset += 9;
                return 4294967296 * a + b;
            case 208:
                return a = this.view.getInt8(this.offset + 1),
                this.offset += 2,
                a;
            case 209:
                return a = this.view.getInt16(this.offset + 1),
                this.offset += 3,
                a;
            case 210:
                return a = this.view.getInt32(this.offset + 1),
                this.offset += 5,
                a;
            case 211:
                return a = this.view.getInt32(this.offset + 1),
                b = this.view.getUint32(this.offset + 5),
                this.offset += 9,
                4294967296 * a + b;
            case 222:
                return a = this.view.getUint16(this.offset + 1),
                this.offset += 3,
                this.map(a);
            case 223:
                return a = this.view.getUint32(this.offset + 1),
                this.offset += 5,
                this.map(a);
            case 220:
                return a = this.view.getUint16(this.offset + 1),
                this.offset += 3,
                this.hz(a);
            case 221:
                return a = this.view.getUint32(this.offset + 1),
                this.offset += 5,
                this.hz(a);
            case 202:
                return a = this.view.getFloat32(this.offset + 1),
                this.offset += 5,
                a;
            case 203:
                return a = this.view.getFloat64(this.offset + 1),
                this.offset += 9,
                a
            }
            throw Error("Unknown type 0x" + a.toString(16));
        }
    }
    ;
    k.If = function(a) {
        var b = new DataView(a)
          , b = new f(b)
          , c = b.parse();
        // 解析的核心就是上面一句了
        // 要是有大佬看上这个项目愿意打赏我会更有动力去反编译出来 ;)
        if (b.offset !== a.byteLength)
            throw Error(a.byteLength - b.offset + " trailing bytes");
        return c
    }
    ;
    k.Cq = function(a) {
        var b = new ArrayBuffer(h(a))
          , c = new DataView(b);
        g(a, c, 0);
        return b
    }
    ;
    return {
        Cq: function(a, b) {
            b(null, {
                ao: a.ao,
                Mc: a.Mc,
                yb: k.Cq(a.yb)
            })
        },
        If: function(a, b) {
            b(null, {
                ao: a.ao,
                Mc: a.Mc,
                yb: k.If(a.yb)
            })
        }
    }
}
;if (self._wkHandlers["msg__def_msg"]) {
    console.log(self._wkHandlers["msg__def_msg"]);
    throw new Error("msg__def_msg already exists!");
}
self._wkHandlers["msg__def_msg"] = _prep_h4.call(null, self) || {};
_prep_h4 = null;
;function _prep_h5(a) {
    return {
        injectCode: function(b, c) {
            var d = null
              , f = null;
            try {
                d = (new Function("self",b))(a)
            } catch (g) {
                f = g.toString()
            }
            c(f, d)
        }
    }
}
;if (self._wkHandlers["msg__g_"]) {
    console.log(self._wkHandlers["msg__g_"]);
    throw new Error("msg__g_ already exists!");
}
self._wkHandlers["msg__g_"] = _prep_h5.call(null, self) || {};
_prep_h5 = null;
;function _prep_h6() {
    return {
        checkup: function() {
            var a = Array.prototype.slice.call(arguments, 0);
            a.pop()(null, a)
        }
    }
}
;if (self._wkHandlers["msg__cln_msg"]) {
    console.log(self._wkHandlers["msg__cln_msg"]);
    throw new Error("msg__cln_msg already exists!");
}
self._wkHandlers["msg__cln_msg"] = _prep_h6.call(null, self) || {};
_prep_h6 = null;
