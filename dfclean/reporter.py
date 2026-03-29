from __future__ import annotations
import json, pandas as pd
from dfclean.utils import _describe_change

class CleanReport:
    def __init__(self, before, after, steps_log):
        self.before=before; self.after=after; self.steps_log=steps_log
        self._summary=_describe_change(before,after)

    def __str__(self):
        s=self._summary
        lines=["="*52,"  dfclean  |  Cleaning Report","="*52,
            f"  Rows  : {s['rows_before']:,} -> {s['rows_after']:,}  (-{s['rows_removed']:,})",
            f"  Nulls : {s['nulls_before']:,} -> {s['nulls_after']:,}",
            f"  Dupes : {s['duplicates_before']:,} -> {s['duplicates_after']:,}",
            f"  Cols  : {s['cols_before']} -> {s['cols_after']}","-"*52]
        for st in self.steps_log: lines.append(f"  [{st['step']}] {st['detail']}")
        lines.append("="*52); return "\n".join(lines)

    def __repr__(self): return self.__str__()

    def to_dict(self):
        cols=[]
        for col in self.before.columns:
            if col not in self.after.columns: cols.append({"column":col,"status":"dropped"}); continue
            cols.append({"column":col,"status":"kept","dtype_before":str(self.before[col].dtype),
                "dtype_after":str(self.after[col].dtype),"nulls_before":int(self.before[col].isna().sum()),
                "nulls_after":int(self.after[col].isna().sum())})
        return {"summary":self._summary,"steps":self.steps_log,"columns":cols}

    def to_json(self,indent=2): return json.dumps(self.to_dict(),indent=indent,default=str)

    def save_html(self,path="dfclean_report.html"):
        s=self._summary
        table=pd.DataFrame(self.to_dict()["columns"]).to_html(index=False,border=0,classes="dt")
        steps="".join(f"<li><b>{st['step']}</b>: {st['detail']}</li>" for st in self.steps_log)
        html=f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>dfclean Report</title>
<style>body{{font-family:system-ui;max-width:860px;margin:2rem auto;}}
h1{{color:#e94560;}}h2{{color:#0f3460;border-bottom:2px solid #e94560;}}
.cards{{display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1.5rem;}}
.card{{flex:1;min-width:140px;background:#f8f9fc;border-left:4px solid #e94560;border-radius:6px;padding:.8rem 1.2rem;}}
.card .val{{font-size:1.6rem;font-weight:700;color:#e94560;}}.card .label{{font-size:.8rem;color:#555;text-transform:uppercase;}}
.dt{{border-collapse:collapse;width:100%;}}.dt th{{background:#0f3460;color:#fff;padding:.5rem .8rem;text-align:left;}}
.dt td{{padding:.4rem .8rem;border-bottom:1px solid #e2e6ea;}}</style></head><body>
<h1>dfclean Report</h1><div class="cards">
<div class="card"><div class="val">{s['rows_removed']:,}</div><div class="label">Rows removed</div></div>
<div class="card"><div class="val">{s['nulls_before']-s['nulls_after']:,}</div><div class="label">Nulls fixed</div></div>
<div class="card"><div class="val">{s['duplicates_before']:,}</div><div class="label">Dupes found</div></div>
<div class="card"><div class="val">{s['cols_before']-s['cols_after']}</div><div class="label">Cols dropped</div></div>
</div><h2>Steps</h2><ul>{steps}</ul><h2>Column Details</h2>{table}</body></html>"""
        with open(path,"w",encoding="utf-8") as f: f.write(html)
        return path
