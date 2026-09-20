# Video Walkthrough Outline (3-5 min)

| Time | Section | Talking points | Visual |
|---|---|---|---|
| 0:00-0:45 | Problem | Stockouts vs overstock across 6 bars / 16 brands; 416 historical stockout events (6.3% of records) | Title slide + stockout-by-bar table (notebook section 2) |
| 0:45-1:45 | Approach and modeling | Transactions -> dense daily panel (96 series x 366 days, 84% zero days); ABC (69 A / 19 B / 8 C); temporal 80/20 split; 4 models; rolling mean wins on WAPE (1.66), Holt-Winters best on RMSE | Notebook: ABC + weekday charts, model comparison table |
| 1:45-3:00 | Inventory logic and simulation | Par = L x forecast + Z x sigma x sqrt(L), L = 2; order up to par with in-transit stock; backtest vs static baseline | Simulated stock vs par line plot; policy table |
| 3:00-4:00 | Business impact and scale | 95%: stockout days -73%, lost ml -83%; 99%: -87% / -92%; cost = 5.4x / 7.1x more stock; daily job to manager dashboard; risks: lead-time variance, events, breakage | KPI comparison table; risks slide |
| 4:00-4:30 | Next steps | Promotion calendar, POS feed, holding-cost-based service level per class | Summary slide |
