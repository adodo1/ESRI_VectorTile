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
;function _prep_h1(a) {
    function b(a, b, d) {
        for (var f = a.yb, g = [], h = a.Hi, m = null, p = null, q = {}, J = 1, W = f.length; J < W; J += 1) {
            var M = f[J]
              , Q = M[1].split("&")
              , m = k(r ? r : Q[0])
              , p = k(Q[2])
              , x = Q[0] + Q[2];
            q[x] || (q[x] = {
                DN: [],
                KM: [],
                yk: [],
                bA: [],
                AY: m,
                borderColor: p,
                xb: M[2]
            });
            var m = q[x].DN
              , p = q[x].KM
              , Q = q[x].yk
              , x = q[x].bA
              , C = M[0]
              , G = M[3] * Math.pow(2, 2);
            if ((M = M[5]) && M.length)
                for (var y = 0, A = M.length; y < A; y += 1)
                    for (var D = M[y].split("-")[1].split("^"), z = 0, L = D.length; z < L; z += 1)
                        -1 === c(g, D[z]) && g.push(D[z]);
            M = 0;
            for (y = C.length; M < y; M += 1) {
                for (var E = C[M], E = testnnn(E), A = l(E, h, b), E = A[1], D = A[2], A = [], z = 0, L = E.length - 1; z < L; z += 1) {
                    var F = E[z]
                      , H = E[z + 1]
                      , N = [F[0] - 0 * G, F[1] - 0.3 * G]
                      , P = [H[0] - 0 * G, H[1] - 0.3 * G]
                      , U = D[z]
                      , Y = D[z + 1]
                      , S = U[0]
                      , ca = Y[0]
                      , U = U[1]
                      , Y = Y[1];
                    0 === S && S === ca || 256 === S && S === ca || 0 === U && U === Y || 256 === U && U === Y || (d ? ((H[0] - F[0]) * (N[1] - F[1]) < (N[0] - F[0]) * (H[1] - F[1]) && (m.push(N[0], N[1], 2),
                    m.push(H[0], H[1], -1),
                    m.push(F[0], F[1], -1),
                    m.push(N[0], N[1], 2),
                    m.push(P[0], P[1], 2),
                    m.push(H[0], H[1], -1),
                    x.push([F, H, P, N])),
                    Q.push(N[0], N[1], -1, P[0], P[1], -1)) : Q.push(F[0], F[1], -1, H[0], H[1], -1));
                    A.push([N[0], N[1]])
                }
                E.pop();
                D = u.EN(d ? A : E, [], 0, 1);
                x.push(d ? A : E);
                E = 0;
                for (A = D.length; E < A; E += 1)
                    for (z = 0; 3 > z; z += 1)
                        p.push(D[E][z][0], D[E][z][1], 3)
            }
        }
        a.yb = [];
        for (E in q)
            q.hasOwnProperty(E) && (Q = [q[E].AY, q[E].borderColor, q[E].xb],
            q[E].bA.qo = !0,
            a.yb.push([new Float32Array(q[E].DN), new Float32Array(q[E].KM), new Float32Array(q[E].yk), Q, q[E].bA]));
        a.dm = g;
        return a
    }
    function c(a, b) {
        if (a && !a.length)
            return -1;
        if (a.indexOf)
            return a.indexOf(b);
        for (var c = 0; c < a.length; c += 1)
            if (a[c] === b)
                return c;
        return -1
    }
    function d(a, b, c, d) {
        for (var g = "solid solid_roundcap solid_squarecap dash railway dash_crewel".split(" "), h = a.yb.slice(1), l = h.length - 1; 0 <= l; l--)
            h[l].FK = l;
        h.sort(function(a, b) {
            return a[2] > b[2] ? 1 : a.FK > b.FK ? 1 : -1
        });
        for (var m = {}, l = 0, n = h.length; l < n; l += 1) {
            var p = h[l], r = p[1].split("&"), u, Q, x, C, G;
            u = Q = x = C = G = null;
            var y, A, D, z, L = null, E = !1;
            y = A = D = z = null;
            r[1] && (u = k(r[1]));
            Q = parseInt(r[0]);
            x = r[2];
            x !== g[0] && (x === g[1] ? y = "round" : x === g[2] ? y = "square" : 0 === x.indexOf(g[5]) ? (L = !0,
            D = [3, 2]) : 0 === x.indexOf(g[3]) ? D = eval("[" + x.substring(5).split(")")[0] + "]") : 0 === x.indexOf(g[4]) && (C = u,
            u = r[4] ? k(r[4]) : [1, 1, 1, u[3]],
            D = [12, 12],
            E = !0,
            G = 3,
            Q = 1));
            r[3] && r[4] && 3 < r.length && (G = Q + parseInt(r[3]),
            C = k(r[4]),
            x = r[5],
            x !== g[0] && (x === g[1] ? A = "round" : x === g[2] ? A = "square" : 0 !== x.indexOf(g[5]) && 0 === x.indexOf(g[3]) && (G += 1,
            z = eval("[" + x.substring(5).split(")")[0] + "]"))));
            if (b) {
                if (D)
                    for (r = D.length - 1; 0 <= r; r -= 1)
                        D[r] *= d;
                if (z)
                    for (r = z.length - 1; 0 <= r; r -= 1)
                        z[r] *= d
            }
            x = [];
            x.Vd = 0;
            var F = []
              , H = [];
            f(x, H, F, p[0], a.Hi, b, c, d, y);
            "app" === q && (Q /= 4,
            G /= 4);
            r = [Q, u, D, G, C, z, L, E, y, A, p[3]];
            r.L6 = !0;
            p = p[2];
            m[p] || (m[p] = []);
            F.qo = !0;
            m[p].push([new Float32Array(x), new Uint16Array(H), r, F])
        }
        a.yb = m;
        return a
    }
    function f(a, b, c, d, f, g, h, k, m) {
        for (var p = 0, q = d.length; p < q; p += 1) {
            var r = a.length / 11
              , u = r + 6
              , x = testnnn(d[p])
              , C = l(x, f, h);
            if (1 < C[1].length) {
                for (var x = C[0], G = C[2], y = 0, C = C[1].length; y < C; y += 1) {
                    if (0 < y) {
                        var A = x[2 * y] - x[2 * y - 2]
                          , D = x[2 * y + 1] - x[2 * y - 1];
                        a.Vd += Math.sqrt(A * A + D * D) * (g ? k : 1)
                    }
                    var A = x[2 * y], D = x[2 * y + 1], z = G[y][0], L = G[y][1], E, F;
                    y === C - 1 ? (E = x[2 * C - 2],
                    F = x[2 * C - 1]) : (E = x[2 * y + 2],
                    F = x[2 * y + 3]);
                    var H, N;
                    0 === y ? (H = A,
                    N = D) : (H = x[2 * y - 2],
                    N = x[2 * y - 1]);
                    if (0 !== y) {
                        var P = y === C - 1 ? 0 : -1;
                        a.push(A, D, z, L, 1, H, N, P, E, F, a.Vd);
                        a.push(A, D, z, L, -1, H, N, P, E, F, a.Vd)
                    } else
                        a.push(A, D, z, L, 0, H, N, 0, E, F, a.Vd),
                        a.push(A, D, z, L, 1, H, N, 0, E, F, a.Vd),
                        a.push(A, D, z, L, 1, H, N, 1, E, F, a.Vd),
                        a.push(A, D, z, L, 0, H, N, 1, E, F, a.Vd),
                        a.push(A, D, z, L, -1, H, N, 1, E, F, a.Vd),
                        a.push(A, D, z, L, -1, H, N, 0, E, F, a.Vd),
                        m && (b.push(r + 2, r + 0, r + 3),
                        b.push(r + 2, r + 1, r + 0),
                        b.push(r + 3, r + 0, r + 4),
                        b.push(r + 4, r + 0, r + 5));
                    y !== C - 1 ? (P = 0 === y ? 0 : 1,
                    a.push(A, D, z, L, 1, H, N, P, E, F, a.Vd),
                    a.push(A, D, z, L, -1, H, N, P, E, F, a.Vd)) : (a.push(A, D, z, L, 0, H, N, 0, E, F, a.Vd),
                    a.push(A, D, z, L, 1, H, N, 0, E, F, a.Vd),
                    a.push(A, D, z, L, 1, H, N, -1, E, F, a.Vd),
                    a.push(A, D, z, L, 0, H, N, -1, E, F, a.Vd),
                    a.push(A, D, z, L, -1, H, N, -1, E, F, a.Vd),
                    a.push(A, D, z, L, -1, H, N, 0, E, F, a.Vd));
                    y !== C - 1 ? (b.push(u + 4 * y, u + 4 * y + 3, u + 4 * y + 1),
                    b.push(u + 4 * y, u + 4 * y + 2, u + 4 * y + 3)) : m && (A = u + 4 * (C - 1),
                    b.push(A + 1, A + 2, A + 0),
                    b.push(A + 2, A + 3, A + 0),
                    b.push(A + 0, A + 4, A + 5),
                    b.push(A + 0, A + 3, A + 4))
                }
                c.push(G)
            }
        }
    }
    function g(a, b) {
        var c = a.yb
          , d = []
          , f = []
          , g = [];
        h(a, f, g, b);
        var l = [[[0, 0], [255, 0], [255, 255], [0, 255]]];
        l.qo = !0;
        d.push([new Float32Array(f), new Uint16Array(g), k("ff" + a.AI.substr(1)), "regions:land", l]);
        c.sort(function(a, b) {
            return "string" === typeof a ? -1 : "string" === typeof b ? 1 : a[2] > b[2] ? 1 : a[2] < b[2] ? -1 : 0
        });
        for (var n = 1, p = c.length; n < p; n += 1) {
            var q = c[n]
              , f = []
              , g = []
              , l = []
              , r = k(q[1].split("&")[0]);
            m(f, g, l, q[0], a.Hi, b);
            l.qo = !0;
            d.push([new Float32Array(f), new Uint16Array(g), r, q[3], l])
        }
        a.yb = d;
        return a
    }
    function h(a, b, c, d) {
        var f = a.Hi
          , g = Math.pow(2, 2);
        a = 256 * f.x * d - 53109887 * g;
        f = 256 * f.y * d - 26262068 * g;
        b.push(a, f);
        g = 256 * d;
        d = a + g;
        b.push(d, f);
        f += g;
        b.push(a, f);
        b.push(d, f);
        c.push(0, 1, 2, 1, 3, 2)
    }
    function k(a) {
        for (var b = [], c = 0, d = a.length; c < d; c += 2)
            b.push(parseInt(a.substr(c, 2), 16) / 255);
        b.push(b.shift());
        return b
    }
    function l(tilecoors, xyz_tilesize, tilesize2048) {
        var d01 = 0
          , f01 = 0
          , d01 = 256 * xyz_tilesize.x
          , f01 = 256 * xyz_tilesize.y;

        xyz_tilesize = [];
        for (var g01 = [], h01 = [], k01 = Math.pow(2, 2), l01 = 0, m01 = tilecoors.length; l01 < m01; l01 += 2) {
            var n01 = (d01 + tilecoors[l01]) * tilesize2048 - 53109887 * k01
              , p01 = (f01 + tilecoors[l01 + 1]) * tilesize2048 - 26262068 * k01
              , q01 = h01.length;

            if (0 === xyz_tilesize.length || n01 !== h01[q01 - 2] || p01 !== h01[q01 - 1])
                // if#1
                1 < xyz_tilesize.length ?
                    // if#2
                    n01 === h01[q01 - 2] && n01 === h01[q01 - 4] ?
                        (h01[q01 - 1] = p01,
                        xyz_tilesize[xyz_tilesize.length - 1][1] = p01,
                        g01[xyz_tilesize.length - 1][1] = tilecoors[l01 + 1]) :
                        // if#2else
                        p01 === h01[q01 - 1] && p01 === h01[q01 - 3] ?
                            (h01[q01 - 2] = n01,
                            xyz_tilesize[xyz_tilesize.length - 1][0] = n01,
                            g01[xyz_tilesize.length - 1][0] = tilecoors[l01]) :
                            // else
                            (h01.push(n01),
                            h01.push(p01),
                            xyz_tilesize.push([n01, p01]),
                            g01.push([tilecoors[l01], tilecoors[l01 + 1]])) :

                        (h01.push(n01),
                        h01.push(p01),
                        xyz_tilesize.push([n01, p01]),
                        g01.push([tilecoors[l01], tilecoors[l01 + 1]]))
        }
        return [h01, xyz_tilesize, g01]
    }
    function m(a, b, c, d, f, g) {
        for (var h = 0, k = d.length; h < k; h += 1) {
            var m = a.length / 2
              , p = l(testnnn(d[h]), f, g);
            2 < p[1].length && (m = u.EN(p[1], [], m),
            m.length && (a.push.apply(a, p[0]),
            b.push.apply(b, m),
            c.push(p[2])))
        }
    }
    function testnnn(a) {
        var b, c, d, f, g;
        c = [];
        d = NaN;
        f = 0;
        for (g = a.length; f < g; f += 1)
            b = a[f],
            b = this.vW.indexOf(b),
            isNaN(d) ?
                d = 27 * b :
                (c.push(d + b - 333), d = NaN);
        return c
    }



    var p = Number.EPSILON || 2E-16, q, r = null, u = {
        me: function(a) {
            for (var b = a.length, c = 0, d = b - 1, f = 0; f < b; d = f++)
                c += a[d][0] * a[f][1] - a[f][0] * a[d][1];
            return 0.5 * c
        },
        I2: function() {
            return function(a, b) {
                var c = a.length;
                if (3 > c)
                    return null;
                var d = [], f = [], g = [], h, k, l;
                if (0 < u.me(a))
                    for (k = 0; k < c; k++)
                        f[k] = k;
                else
                    for (k = 0; k < c; k++)
                        f[k] = c - 1 - k;
                var m = 2 * c;
                for (k = c - 1; 2 < c && !(0 >= m--); ) {
                    h = k;
                    c <= h && (h = 0);
                    k = h + 1;
                    c <= k && (k = 0);
                    l = k + 1;
                    c <= l && (l = 0);
                    var n;
                    a: {
                        var q = n = void 0
                          , r = void 0
                          , x = void 0
                          , C = void 0
                          , G = void 0
                          , y = void 0
                          , A = void 0
                          , D = void 0
                          , q = a[f[h]][0]
                          , r = a[f[h]][1]
                          , x = a[f[k]][0]
                          , C = a[f[k]][1]
                          , G = a[f[l]][0]
                          , y = a[f[l]][1];
                        if (p > (x - q) * (y - r) - (C - r) * (G - q))
                            n = !1;
                        else {
                            var z = void 0
                              , L = void 0
                              , E = void 0
                              , F = void 0
                              , H = void 0
                              , N = void 0
                              , P = void 0
                              , U = void 0
                              , Y = void 0
                              , S = void 0
                              , Y = U = P = D = A = void 0
                              , z = G - x
                              , L = y - C
                              , E = q - G
                              , F = r - y
                              , H = x - q
                              , N = C - r;
                            for (n = 0; n < c; n++)
                                if (A = a[f[n]][0],
                                D = a[f[n]][1],
                                !(A === q && D === r || A === x && D === C || A === G && D === y) && (P = A - q,
                                U = D - r,
                                Y = A - x,
                                S = D - C,
                                A -= G,
                                D -= y,
                                Y = z * S - L * Y,
                                P = H * U - N * P,
                                U = E * D - F * A,
                                Y >= -p && U >= -p && P >= -p)) {
                                    n = !1;
                                    break a
                                }
                            n = !0
                        }
                    }
                    if (n) {
                        d.push([a[f[h]], a[f[k]], a[f[l]]]);
                        g.push([f[h], f[k], f[l]]);
                        h = k;
                        for (l = k + 1; l < c; h++,
                        l++)
                            f[h] = f[l];
                        c--;
                        m = 2 * c
                    }
                }
                return b ? g : d
            }
        }(),
        EN: function(a, b, c, d) {
            var f, g, h, k = {};
            b = 0;
            for (f = a.length; b < f; b++)
                h = a[b][0] + ":" + a[b][1],
                k[h] = b;
            a = u.I2(a, !1);
            if (!a)
                return [];
            if (d)
                return a;
            var l = [];
            b = 0;
            for (f = a.length; b < f; b++)
                for (g = a[b],
                d = 0; 3 > d; d++)
                    h = g[d][0] + ":" + g[d][1],
                    h = k[h],
                    l.push(h + c);
            return l
        },
        k6: function(a) {
            return 0 > u.me(a)
        }
    };
    return {
        WB: function(c, f) {
            q = c.mode;
            var h = c.Gu
              , k = c.tr;
            r = c.Mt;
            for (var l = [], m = Math.pow(2, 20 - h), h = 0, n = c.ce.length; h < n; h += 1) {
                var p = c.ce[h];
                switch (p.Mc) {
                case "region":
                    l.push(g(p, m));
                    break;
                case "road":
                    l.push(d(p, k, m, c.IM));
                    break;
                case "building":
                    l.push(b(p, m, c.LW))
                }
            }
            c.ce = l;
            if (a) {
                k = [];
                h = 0;
                for (n = l.length; h < n; h++)
                    if ((m = l[h].yb) && m.length)
                        for (var p = 0, u = m.length; p < u; p++)
                            m[p].buffer && m[p].buffer instanceof ArrayBuffer && k.push(m[p].buffer);
                a.Ct(k)
            }
            f(null, {
                data: c
            })
        },
        b7: function() {}
    }
}
;if (self._wkHandlers["w1__def_w1"]) {
    console.log(self._wkHandlers["w1__def_w1"]);
    throw new Error("w1__def_w1 already exists!");
}
self._wkHandlers["w1__def_w1"] = _prep_h1.call(null, self) || {};
_prep_h1 = null;
;function _prep_h2(a) {
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
;if (self._wkHandlers["w1__g_"]) {
    console.log(self._wkHandlers["w1__g_"]);
    throw new Error("w1__g_ already exists!");
}
self._wkHandlers["w1__g_"] = _prep_h2.call(null, self) || {};
_prep_h2 = null;
;function _prep_h3() {
    return {
        checkup: function() {
            var a = Array.prototype.slice.call(arguments, 0);
            a.pop()(null, a)
        }
    }
}
;if (self._wkHandlers["w1__cln_w1"]) {
    console.log(self._wkHandlers["w1__cln_w1"]);
    throw new Error("w1__cln_w1 already exists!");
}
self._wkHandlers["w1__cln_w1"] = _prep_h3.call(null, self) || {};
_prep_h3 = null;
