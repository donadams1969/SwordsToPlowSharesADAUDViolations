import fitz, re, glob, os, json
A="/vercel/share/artifacts/"
files=sorted(glob.glob(A+"Gillson_FINAL_Binder*.pdf"))
for f in files:
    n=int(re.search(r"Binder(\d)",f).group(1))
    d=fitz.open(f); N=len(d)
    blank=[];bad=[];seq_bad=[]
    for i,p in enumerate(d):
        t=p.get_text().strip()
        m=re.findall(r"B%d-(\d{4})"%n,t)
        want="%04d"%(i+1)
        if want not in m: seq_bad.append(i+1)
        body=re.sub(r"B%d-\d{4}"%n,"",t).strip()
        if len(body)<15 and not p.get_images() and len(p.get_drawings())<3: blank.append(i+1)
    toc=d.get_toc()
    oor=[x for x in toc if x[2]<1 or x[2]>N]
    # index check: find index page(s), parse "B#-####" ranges
    print(os.path.basename(f), "pages",N, "size %.1fMB"%(os.path.getsize(f)/1e6), "bookmarks",len(toc),"out-of-range",len(oor),"blank",blank,"bates-mismatch",seq_bad[:10],len(seq_bad))
    # bookmark -> page text matches bates of target
    # index entries
    idx_pages=[i for i in range(min(N,12)) if "MASTER INDEX" in d[i].get_text()]
    ents=[]
    for i in idx_pages:
        for m in re.finditer(r"B%d-(\d{4})(?:\s*(?:to|\u2013|-|\u2014)\s*B%d-(\d{4}))?"%(n,n),d[i].get_text()):
            ents.append((int(m.group(1)),int(m.group(2)) if m.group(2) else None))
    bad=[e for e in ents if e[0]>N or (e[1] and (e[1]>N or e[1]<e[0]))]
    print("   index pages",[x+1 for x in idx_pages],"entries",len(ents),"bad",bad[:5])
    # bookmark titles vs page start: check each L1/L2 bookmark's target page begins a new doc (non-empty)
    tp=[x[2] for x in toc]; print("   bookmark pages monotonic-nondecreasing:", all(tp[i]<=tp[i+1] for i in range(len(tp)-1)) )
