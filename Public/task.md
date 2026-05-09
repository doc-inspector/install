# Hero Office Animation — v3 Refactor

## User Feedback (v2):
1. Prea multe documente cad — trebuie ONE at a time, chibi se duce după el
2. Scoatem documentele de pe jos (floor docs + near desks)
3. Head shake mai rațional — privește documentul care cade, arată nemulțumire cu sens
4. Grid-ul 3D extins mai sus (nu doar zona de floor)
5. Omulețul + mesele prea vizibile — reduce alpha
6. Animație throw mai elaborată:
   - Cu mâna: prinde + aruncă, documentul zboară spre coș
   - Cu piciorul: prinde cu mâna, lovește cu piciorul, doc zboară
   - Să se vadă documentul zbură în arc spre coș
7. Prima dată: cade de pe imagine (nu instant pe podea)
8. CYCLE: 
   - Docs cad ~30 sec (one at a time)
   - Stop 15 sec — chibi se suie pe imagine, fericit, zâmbește
   - Restart — devine nervos, iar cade jos
   - Loop infinit

## Implementation Plan:
- Remove floorDocs entirely
- Remove desk floor docs  
- Single doc spawn — wait until chibi finishes before next
- Throw animation with projectile arc (doc flies to bin)
- State machine: ACTIVE_PHASE (30s) → HAPPY_PHASE (15s) → loop
- Grid extends from top of hero to bottom
- Reduce all alphas ~30%
- Chibi falls off image first time
- Head looks at falling doc, then shakes head with meaning
- Happy face (smile) when on image during break
