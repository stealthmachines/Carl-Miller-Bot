import urllib.request
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

URLS = [
    "https://forum.zchg.org/uploads/default/original/1X/c42071a0d0f10f3ae02927c0665ed12f822afdcf.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/e3ac132714b948a08b28e79dcb8414056c4bcc6b.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/d39ea9809076ac9ec6a4b2865bdc699e8df3be14.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/f3d3f59357f652333abab55b0be53e1d5d50a72c.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/e9bf221f8db4d8c927c882fdf9b805b75cb8ee96.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/eac776505961d9b3d7953a1b164588d9c43202e8.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/30d86f26b97819bb85849f5a7ccbea2c8630e4c7.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/55c1f1f02ce8d59dd621518ae3ca982983b1b6a3.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/8cc155eea15a602e7eb4505a60e1fa0512537e7e.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/00c5b774ad8341221095e94f17c05ed500ba7155.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/6a7c7bf6c1882de4fd6e26710b892d0a0436a5e6.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/0eb13c0d5bf8e822a2b762f028d879baabd38bdb.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/d8a7a3801bdefa82a8e77f8314ab771513de2082.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/3913454345b5e466bb5ee528adae39f7e887aff6.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/0a6bbeb87adbc3dbe0c7af0a6de0c06a1c74143e.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/4a2720d3b242afb68080e36dd2b98466e1b1e82f.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/6f7020246b251433ecf18d2001a5cb156987f8b8.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/fdd805a4807aca897f7d779971d729e1f7641d55.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/987165db37e8529fdf2724eba1f58a8e50660f0e.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/e1b184836d1868955d1bf9b8e1645940a8674138.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/cff55d8304c5e134a677b6df56b80c07886fb3a8.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/02d2d89076a179ac1d3cb7617806fbd76062abef.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/34fc2515ba95b7320d7e0f75aa396069dc463710.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/d16078699b0135de9b8d38a5f3b430f00f7c4c32.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/8da65dbbc78510972e4c41a2cee1c69db676284e.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/5bb5478b54da8f4479edee9d9133bc0e58bb2f7c.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/6eff9f91c289bb53533237b8a5830c2b9aaa0a6d.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/de56d452dfd82ddc828be6311da360495228767d.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/39143d6d210e9bd5a8f5660680e6c7ac454ce7b4.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/63f2a50fb6ca47d67e73e1e337ddf16b4fea1cca.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/f0369937a357c66c09078aa22ff1cfa5f1522a8a.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/d0c4b19d59c310d94550f08d0be9db0dc3c18118.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/4c0b9608abd476a56dfb90fb5da99a5c5c5b4dcb.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/ea59f107a3f5c0314de836670465f8b1067d2b6e.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/3bdd94b0f6cac7b334f2455fa37813ceb70fcb05.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/8045dd456f5e250eea5e14279b5b6ebbb0718507.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/0f28d7714b922718f1fb4aae19cb92d506422dd4.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/2c647be9d10bdb9b84ccf574ad3fb4ef0c6216d2.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/be226fb49ecac3a579fd2ceb4d4dbe1728f7fcce.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/979892a07ec71826d70a35cf6dfdc52cf2b64446.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/37e18231fbb27b9ac448e3ddf295e5e03304f23c.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/d638da9ccd815ddd822e2fa1249b03de1e726050.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/9cc67327092330aaff4f1942469c57f8d8610d58.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/5812a6574367d9b4f8366c0233b4639cc3f3bc09.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/258d45f4c3d859c28653c463ec3c3f8ab3c3958a.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/57d56686613b83da47d3f7aa43723d67d13e5ef1.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/a8e4604eae0ca2a752a51693b1714be9c32ed551.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/a8a30362a61f5dd09ee10a53485b759a5f20b8e2.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/35a4ea23965a163e48ef05f262c2d9755972fc0f.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/2b302a58abe9dd33bd9add0967502ca7168ff7e7.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/3eee8f682d8716843f76eb7b903827dfcd438cab.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/bf6d1553c80f23d541e19aee9ae069d4ca359749.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/d24b5687d199c2249b11a5ba22ee6d4ebd5444ea.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/ab0f1217a1bafbefdbe92973f292e5b971670495.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/ceeb2b5fe3d3040b7f5e22930bf0bd2b073e.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/dcec337b035fa0cd06dd06a842cf9a5557de9fee.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/1dd80945f4f337e638f310be5b0981f2b06a48a3.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/d451223159e969f4a5c9cbaf2038e625f330d21a.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/65dd946667e36992e39d538f7beeaadbd4253137.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/36a8c16f56eab8430caeaf966430cbb6a102b198.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/39f8e72b374cdd0a44e98d0b60e81d95d82dfc86.jpeg",
    "https://forum.zchg.org/uploads/default/original/1X/3c3e5850f624e2866648e217b59c22e41286c545.jpeg",
]

OUT_DIR = r"C:\Users\Owner\Downloads\Legal-Vision-main\Legal-Vision-main\Carl Miller\16AmJur2d_images"
os.makedirs(OUT_DIR, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://zchg.org/',
}

for i, url in enumerate(URLS):
    fname = f"img_{i+1:02d}_{url.split('/')[-1]}"
    fpath = os.path.join(OUT_DIR, fname)
    if os.path.exists(fpath):
        print(f"[{i+1:02d}/{len(URLS)}] SKIP {fname}")
        continue
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(fpath, 'wb') as f:
            f.write(data)
        size = len(data) // 1024
        print(f"[{i+1:02d}/{len(URLS)}] OK   {fname} ({size}KB)")
        time.sleep(0.5)
    except Exception as e:
        print(f"[{i+1:02d}/{len(URLS)}] ERR  {fname}: {e}")

print("\nDone. Files in:", OUT_DIR)
