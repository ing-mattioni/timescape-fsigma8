# Prosecuzione di P187–P189: matching scalare LTB–CMC e trasferimento a H1

Data: 2026-09-25. Punto di partenza: il report di ricerca con P187, P188 e
P189. I due problemi aperti erano:

1. costruire una famiglia geometrica ammissibile che soddisfi il criterio P187 su un intervallo;
2. dimostrare che il trasferimento dei suoi stati locali a H1 conserva dinamica, vincoli e closure costitutiva.

Questo report spiega come ho proceduto e che cosa ho ottenuto. Tiene
distinti tre livelli: quello che è dimostrato, quello che è derivato in modo
formale con conferma numerica, e quello che resta aperto.

## Correzioni (2026-09-25)

La versione originale di questo report è quella del commit `4d98b9f`
(SHA-256 `5019150b…`). Le correzioni seguenti sono solo testuali: nessuna nuova
simulazione, nessuna estensione del modello, nessuno status modificato. L'unico
calcolo nuovo è una conversione di unità (divisione per c) di valori già
registrati in `conformal_drift.out`.

1. **No-go H1 ristretto a ciò che è dimostrato.** Ora vale solo sotto
   l'identificazione geometrica materiale IM (§4.2), cioè regioni H1 = regioni
   materiali LTB con background FLRW esatti. La verifica numerica dei gate vale
   solo per la mappa M1 esaminata (§4.5). Ho tolto "impossibile per H1 così
   definito" e "l'enunciato è falso".
2. **Ipotesi del no-go scalare rese esplicite.** Sono H_A, H_B e H_asym (§0,
   §3.2, §3.5–§3.7).
3. **Eliminata l'identificazione non derivata fra la disomogeneità di
   λ = ∂_cS e il lapse perturbativo dell'osservatore wall ν_W.**
   - **Significato di λ.** λ conserva il suo significato cinematico: è il rapporto locale fra l'età propria della polvere e il parametro c, a etichetta fissa.
   - **Identificazione con α_r.** Anche l'identificazione con il clock regionale omogeneo α_r di CLK-H1 richiede una mappa esplicita. M1 ne è una scelta (§4.5).
   - **Cosa ho tolto.** Presupponevano una di queste identificazioni:
     - la voce "clock regionali non omogenei, cioè ν_W" fra le estensioni necessarie;
     - la conclusione "CLK-H1 violato";
     - il confronto con f̂.
   - **Termine 𝓑.** Non è più chiamato "termine di clock", ma termine di retroazione e dei pesi λ (§3.3).

   Questa voce è stata riformulata il 2026-09-26; vedi sotto.
4. **Larghezza dello strato limite.** La formula precedente valeva solo in
   unità interne. Ora è scritta in forma dimensionalmente corretta, insieme allo
   spessore proprio c/√2 (§3.4).
5. **Unità della deriva conforme.** I valori tabulati sono c·τ, adimensionali
   (unità interne). Ho aggiunto τ in unità fisiche e il confronto con il tasso
   medio ∂_c ln R. La sezione è ora una nota condizionata, fuori dal no-go (§4.6).
6. **Correzioni editoriali.**
   - Il riferimento ai profili generali punta ora a §3.6 invece che a §3.7.
   - Lo stato del repository è datato al momento della stesura.
   - Script e output sono indicati nell'archivio, non nel repository (§7).

## Correzioni (2026-09-26)

**Che cosa ho riformulato.** La voce 3 della lista precedente, dopo il
chiarimento che i due simboli della richiesta erano λ e ν_W. La versione del
2026-09-25 attribuiva la correzione all'identificazione λ ↔ α_r, e conteneva
formulazioni assolute come "λ non è un clock" e "non un clock fisico". Le ho
eliminate.

**La nuova versione.**

- L'identificazione rimossa è quella, non derivata, fra la disomogeneità di λ e il lapse perturbativo dell'osservatore wall ν_W.
- λ è descritto per il suo significato cinematico: rapporto locale fra età propria della polvere e c.
- L'identificazione con α_r è dichiarata possibile solo tramite una mappa esplicita.

**Punti modificati:** §3.3, §4.4, §4.5, §4.8 e §6. Nessun'altra modifica, e
nessun calcolo nuovo.

---

## 0. In breve

**Verifica del materiale di partenza.**

- P187 è corretto. Ho riprodotto tutti i dodici numeri della tabella BASE, identici a tutte le cifre stampate.
- Le formule P187 per le derivate in c di f̂, t̂, b̂ e Ĉ coincidono con differenze finite indipendenti entro 7·10⁻¹¹.
- P188 e P189 sono corretti; ho rifatto i calcoli.

**Primo punto aperto.** Nella famiglia selezionata la risposta è negativa
**sotto le ipotesi H_A, H_B e H_asym**, elencate qui sotto. Nel settore
generale il problema è ridotto ma non risolto.

**Ipotesi del no-go scalare.**

- **(H_A) Quadro di P187 e del Teorema A.**
  - Geometria LTB a bang simultaneo, con m = m₀r³ e k ∈ C¹, k ≥ 0.
  - Un ramo continuo di sezioni CMC ancorate (S(c,0) = S(c,1) = c), spaziali e nella regione regolare s > 0.
  - J > 0 e 0 < Ω_c < 1 lungo il ramo.
  - Mappa di clock selezionata c = τ_w(t;b) + C.
  - La dimostrazione del Teorema A è uno schizzo.
- **(H_B) Il ramo raggiunge il regime vicino al bang.** Verificato numericamente solo per BASE e SECOND, fino a c/m₀ = 10⁻⁶. Non dimostrato.
- **(H_asym) L'espansione formale della Proposizione B è valida.** Confermata numericamente su due ordini, senza stime d'errore rigorose.

**Risultati.**

- **Rigidità analitica (Teorema A, sotto H_A).**
  - Lungo il ramo, lo scarto 𝓔(c) di P187 è una funzione reale-analitica di c.
  - Di conseguenza il matching su un intervallo equivale al matching sull'intero ramo, e gli zeri di 𝓔 sono isolati.
  - Per BASE, sotto H_A e senza H_B né H_asym, basta il valore calcolato 𝓔(1) = 0.0864 ≠ 0: il criterio P187 non vale su *nessun* intervallo del ramo, non solo attorno a c = 1.
- **Identità esatta con il FLRW aperto.**
  - Vale 𝓔 = E_FLRW(f̂) − 𝓑/(3J²), con E_FLRW(f) = f(1−f)(12+18f+5f²)/(2+f)⁴ > 0.
  - 𝓑 è il termine di retroazione e dei pesi λ, 𝓑 = Q_λ + P_λ − 4πG(ρ_λ − ρ₀).
  - Un FLRW aperto non soddisfa mai il criterio.
  - In BASE, a c = 1, 𝓑 vale −2.4·10⁻³, mentre il tracker richiederebbe +0.132: segno sbagliato, ampiezza circa 50 volte minore.
- **Asintotica vicino al bang (Proposizione B).** È derivata in modo formale e confermata numericamente su due ordini:
  - 1 − Ω_c = (5/3)W ε + (√2/15)(3k(0) − 3k(1) − k_r(1))(c/m₀)/I_w + O(ε²);
  - 𝓔 = (5/12)W ε + O(ε²), senza alcun termine di ordine c;
  - qui ε ∝ (c/m₀)^{2/3} e W è un funzionale esplicito del profilo di curvatura.
- **Esito nella famiglia selezionata** (sotto H_A, H_B e H_asym). Per ogni κ* > 0 si ha W > 0.
  - Vicino al bang quindi 𝓔 ≈ (3/4)f̂ > 0 e b̂ ∝ c^{1/3} → 0.
  - Nessun membro della famiglia selezionata soddisfa P187 su alcun intervallo del proprio ramo.
  - Senza H_B o senza H_asym, la conclusione vale solo per i parametri calcolati esplicitamente (BASE, SECOND), tramite il Teorema A.
  - L'ostruzione ha un'origine fisica: il modo crescente ha esponente 2/3, mentre la frazione di vuoto del tracker cresce linearmente.
- **Settore generale.** Il problema non è risolto, ma è ridotto.
  - Il termine dominante W si può compensare.
  - In quel caso il termine lineare "di vuoto" del tracker può nascere solo dallo strato limite all'ancora esterna, e b̂(0⁺) è fissato dal salto di curvatura.
  - Con un profilo compensato esplicito, b̂ resta entro il 3% di una costante su tre decadi di c, ma 𝓔 ≈ 0.63 ε² ≠ 0.
  - Esistenza ed esclusione restano aperte.

**Secondo punto aperto.** Il no-go che ho dimostrato vale sotto una sola
identificazione, e la verifica numerica riguarda una sola mappa.

- **Identificazione geometrica materiale (IM).**
  - Le regioni muro e vuoto di H1 sono due regioni materiali LTB, cioè insiemi di gusci di polvere, con background di polvere FLRW esatti.
  - L'interfaccia Γ di H1 ha misura nulla e non porta stato.
- **Teorema D (GR generica).** Due regioni materiali di polvere FLRW distinte non possono confinare lungo uno stesso guscio. Fra loro serve un insieme di gusci con volume positivo.
- **No-go sotto IM.** Sotto IM le due regioni non coprono il dominio, e un trasferimento esatto non esiste.
  - Per identificazioni diverse non ho dimostrato nulla: per esempio regioni non materiali, o background regionali intesi come medie.
- **Fatti geometrici nella famiglia selezionata.**
  - Tutta l'inomogeneità indipendente dallo slicing sta nella transizione: in BASE, il 34% del volume e della massa.
  - Le sezioni ancorate non possono essere sincrone su entrambe le regioni FLRW esatte (dimostrato).
- **Gate del repository, solo per la mappa M1.** M1 è una scelta (§4.5). Con M1, `two_region_background_identity_residuals` segnala violate:
  - le righe regionali;
  - la retroazione a due regioni;
  - le equazioni medie GM (3.8)–(3.9).

  Le righe cinematiche automatiche passano. Il risultato non si estende ad altre mappe.
- **Cosa servirebbe sotto IM.** Una terza regione, oppure un'interfaccia di misura positiva con un proprio stato. Sarebbe un'estensione del modello da autorizzare, e non l'ho introdotta.

**Cosa non avevo cambiato al momento della stesura.**

- Nessuno status scientifico, nessun file del repository, nessuna operazione git.
- Script e output restano fuori dal repository, nell'archivio indicato al §7.
- Il report stesso è stato poi aggiunto a `reports/` su richiesta.

---

## 1. Come ho lavorato

**Materiale letto.**

- Il codice dell'esperimento (`geometry.py`, `solver.py`, `evolution.py`, `clock.py`), per conoscere esattamente:
  - il profilo, cioè k(r) = κ*χ(r), m(r) = m₀r³, con bang simultaneo;
  - l'equazione CMC con le ancore S(c,0) = S(c,1) = c;
  - l'operatore di lapse L[N] = −ΔN + UN;
  - le medie intrinseche e le definizioni di J, q_c, P_λ, Q_λ, ρ_λ.
- Per H1:
  - i report 1E-F (contratto), 1E-G (realizzazione continua) e F3 (gate cinematici);
  - `transfer/h1_realization.py`;
  - `scientific_status.py`.

**Strumenti.**

- **Come ho calcolato.** Ho usato il solver esistente, con il preset TIGHT dei test. Dove serviva ho alzato solo `max_nodes`, fino a 40000, per c piccolo.
- **Ambiente.** Python 3.13.12, NumPy 2.5.3, SciPy 1.18.1, con i warning trattati come errori. Il report di partenza usava 3.12.14, 2.3.5 e 1.17.0: i valori coincidono a tutte le cifre stampate.
- **Identità algebriche.** Sympy non è installato e non ho installato nulla. Ho controllato le identità a mano e poi numericamente: formule chiuse valutate su griglie, e differenze finite con estrapolazione di Richardson, usate solo come strumento di test.
- **Profili fuori dalla famiglia selezionata** (§3.6).
  - Ho sostituito la funzione `curvature()` solo nella memoria del processo di scratch; nessun file del package è stato toccato.
  - Per questi profili ho calcolato q dalla sola J del background, con differenze in ln c. Non ho usato `evolution.py`, perché i suoi limiti al centro assumono un centro piatto.
  - Questa via e `evolution.py` concordano su BASE: 1·10⁻¹¹ a c/m₀ = 10⁻³ e 2·10⁻⁹ a c = 1.

**Convenzioni.** Sono quelle di P187:

- f = t/(t+b), H_D = (2+f)/(3t), ρ_D = (1−f)/(6πGt²);
- τ_w = (2/3)t + (2b/9)ln(1+3t/(2b)), α_W = 2/(2+f);
- c = s_c è l'età propria della polvere alle due ancore.

Inoltre

$$\varepsilon(c)=\frac{(9/2)^{1/3}}{10}\Big(\frac{c}{m_0}\Big)^{2/3},\qquad
I_w=\int_0^1\frac{r^2\,dr}{\sqrt{1+r^2k(r)}} .$$

ε è il parametro di crescita della curvatura vicino al bang, cioè a_k/a per k → 0, come nel codice.

---

## 2. Verifica di P187–P189

### 2.1 P187

**Tabella BASE.** È BASE a c = 1, preset TIGHT
(`p187_base_table.out`). I valori coincidono con quelli del report, cifra per
cifra:

| Quantità | Report | Ricalcolo |
|---|---|---|
| J | 0.7211615981 | 0.7211615981 |
| ρ₀ | 0.02380663603 | 0.02380663603 |
| Ω_c | 0.6519291101 | 0.6519291101 |
| f̂ | 0.1420979592 | 0.1420979592 |
| t̂ | 1.0604612704 | 1.06046127 |
| b̂ | 6.4024275425 | 6.402427543 |
| Ĉ | −0.02269051745 | −0.02269051745 |
| q_c | 0.3275224674 | 0.3275224674 |
| q_required | 0.2410925714 | 0.2410925714 |
| 𝓔 | 0.08642989602 | 0.08642989602 |
| ∂_c ln b̂ | 0.3611131724 | 0.3611131724 |
| ∂_c Ĉ | −0.03548153952 | −0.03548153952 |

L'adattatore di clock del package (`tracker_clock`) restituisce esattamente
f̂ e c a partire da (t̂, b̂, Ĉ).

**Formule delle derivate.** Ho confrontato le formule P187 con differenze
centrali in c dei parametri ricostruiti, a parametri fisici fissi, con passi
h = 4·10⁻³, 2·10⁻³, 10⁻³ ed estrapolazione di Richardson. Il rapporto degli
errori è 4.00, come atteso per il secondo ordine:

| Derivata | Formula P187 | Differenze finite | Scarto |
|---|---|---|---|
| ∂_c f̂ | 0.0820215705 | 0.08202157051 | 2.1·10⁻¹² |
| ∂_c t̂ | 1.096452076 | 1.096452076 | 3.1·10⁻¹¹ |
| ∂_c b̂ | 2.312000921 | 2.312000921 | 7.3·10⁻¹¹ |
| ∂_c Ĉ | −0.03548153952 | −0.03548153955 | 2.9·10⁻¹¹ |

Ho anche rifatto a mano la derivazione di ∂_c ln b̂: il coefficiente di 𝓔
risulta J(2+f̂)²/(3f̂(2−f̂)), come nel report.

### 2.2 P188

Ho rifatto a mano i passaggi con R² R_r = (3m_b/2)r²T(3T − 2rβ'):

- ρ_ε = 1/(6πG T(T − (2/3)rβ'));
- ∂_ε ln ρ|₀ = (1−r²)²(2 − 6r²)/s = (2 − 10r² + 14r⁴ − 6r⁶)/s;
- il Laplaciano piatto vale (−60 + 280r² − 252r⁴)/s;
- la media con peso r² è nulla;
- la derivata radiale si annulla in r = 1.

Tutto è corretto, e il perimetro dichiarato nel report (bang non simultaneo,
sezioni sincrone) è rispettato.

### 2.3 P189

Le identità sono tutte corrette:

- l'inversione delle medie annidate, X = X̄ + (V/V_r)∂_r X̄, che segue da ∂_r(V X̄) = X V_r;
- la derivata 𝒟_r = ∂_r|_c − (S_r/λ)∂_c, che segue da 0 = λ dc + S_r dr a s fisso;
- il commutatore [∂_c, 𝒟_r] = −∂_c(S_r/λ)∂_c;
- i due Laplaciani, costruiti rispettivamente con A e con B.

---

## 3. Primo punto aperto: esiste una famiglia che soddisfa P187 su un intervallo?

### 3.1 Riformulazione

Poiché ∂_cV/V = 3J e ρ₀V = M, il criterio 𝓔 ≡ 0 con b e C costanti
equivale a una sola identità funzionale sul volume:

$$V(c)=\frac{M}{\rho_D(t)}=\frac{6\pi G M}{b}\,t^2(t+b),\qquad c=\tau_w(t;b)+C .$$

V(c) = ∫₀¹ v(S(c,r),r) dr, con v = 4πAR², dipende soltanto dalla forma della
sezione.

### 3.2 Teorema A: rigidità analitica

**Enunciato** (le sue ipotesi, insieme alla mappa di clock di P187,
costituiscono H_A). Consideriamo:

- una geometria LTB con bang simultaneo, m = m₀r³ e k ∈ C¹, k ≥ 0 (il settore del solver);
- un ramo continuo c ∈ I ↦ (S(c,·), K(c)) di sezioni CMC ancorate, spaziali e contenute nella regione regolare s > 0.

Allora S e K dipendono in modo reale-analitico da c. Di conseguenza V, J,
q_c, Ω_c e, dove J > 0 e 0 < Ω_c < 1, anche f̂ e 𝓔 sono funzioni
reale-analitiche su I.

**Schizzo della dimostrazione.**

1. **La geometria è analitica nel tempo.** La soluzione LTB a(s,k) è analitica congiuntamente in (s,k) per s > 0 e k ≥ 0: basta la soluzione parametrica. Quindi A, R e Θ sono analitiche in s e continue in r, anche se il profilo χ è soltanto C^∞ in r.
2. **Il problema ancorato è analitico.** Lo scrivo come F(S, K; c) = 0: l'operatore di curvatura media meno K, con S(0) = S(1) = c. F è analitica, perché è composta da funzioni analitiche nella variabile temporale.
3. **La linearizzazione è invertibile.** La linearizzazione è l'operatore di Jacobi L[N] = −ΔN + UN, più l'ancora centrale.
   - U = K_ijK^ij + 4πGρ(2γ² − 1) > 0 per la polvere.
   - La soluzione di L[φ] = 1 con φ(1) = 0 è positiva per il principio del massimo, quindi φ(0) > 0; è la stessa quantità che il solver controlla.
   - Ne segue che (δS, δK) ↦ (L[δS] − δK, δS(0)) ha nucleo banale, e il problema è non degenere in ogni punto del ramo.
4. **Si conclude con il teorema della funzione implicita analitico.** Dà dipendenza analitica locale. Per unicità locale coincide con il ramo dato, quindi il ramo è analitico su tutto I.
5. **Anche 𝓔 è analitica.** V è un integrale di una funzione analitica. F⁻¹ è analitica su (0,1) perché F' < 0; quindi 𝓔 è analitica.

**Classificazione:** DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION, per il
settore. È uno schizzo: i dettagli di analisi funzionale (spazi di Hölder e
centro singolare dell'ODE radiale) sono standard ma non li ho scritti per
esteso.

**Corollario A1.** Se 𝓔(c₀) ≠ 0 in un punto del ramo, gli zeri di 𝓔 sono
isolati. In particolare 𝓔 non si annulla su nessun sottointervallo.

**Conseguenza per BASE** (sotto H_A; non servono H_B né H_asym). 𝓔(1) =
0.0864, contro una differenza di 2·10⁻⁹ fra due vie di calcolo indipendenti.
Quindi BASE non soddisfa P187 su nessun intervallo del suo ramo.

Il report di partenza non estendeva il risultato "a intervalli non
esaminati". Per un ramo fissato questa estensione segue ora dal Teorema A,
dimostrato in forma di schizzo, e da un valore numerico.

Numericamente 𝓔 > 0 in tutti i punti campionati, da c/m₀ = 10⁻⁶ a
c/m₀ = 150 (otto decadi; `near_bang_*.out`, `late_BASE.out`).

### 3.3 Identità esatta: il criterio misurato rispetto al FLRW aperto

**L'identità.** Dall'identità di Raychaudhuri mediata dell'evoluzione,
3(J_c + J²) + 4πGρ_λ − Q_λ − P_λ = 0, e da Ω_c/2 = 4πGρ₀/(3J²), si ottiene in
modo esatto

$$\mathcal E=E_{\rm FLRW}(\widehat f)-\frac{\mathcal B}{3J^2},\qquad
E_{\rm FLRW}(f)=\frac{F(f)}{2}-q_{\rm required}(f)=\frac{f(1-f)(12+18f+5f^2)}{(2+f)^4},$$

$$\mathcal B=Q_\lambda+P_\lambda-4\pi G(\rho_\lambda-\rho_0).$$

**Conseguenze.**

- **Il FLRW aperto non basta mai.** Per un FLRW aperto di polvere q = Ω/2, quindi 𝓔 = E_FLRW(f) > 0 per ogni 0 < f < 1.
- **Cosa serve per il matching.** Il matching richiede 𝓑 = 3J²E_FLRW(f̂) > 0 esattamente: la retroazione e i termini con i pesi λ devono fornire proprio il contributo del tracker. Qui λ = ∂_cS è il rapporto locale fra età propria della polvere e parametro c, che entra come peso nelle medie BMR della famiglia di sezioni.

**Verifica.** Controllo sui valori accettati dal package
(`backreaction_split.out`). L'identità vale a 7·10⁻¹⁶:

| Caso | 𝓔 | E_FLRW(f̂) | Q_λ | P_λ | 4πG(ρ_λ − ρ₀) | 𝓑 | 𝓑 richiesto |
|---|---|---|---|---|---|---|---|
| BASE, c = 1 | 0.086430 | 0.084872 | +5.2·10⁻⁶ | −3.9·10⁻⁴ | +2.04·10⁻³ | −2.43·10⁻³ | +0.132 |
| BASE, c = 0.2 | 0.039176 | 0.037222 | +3.3·10⁻⁵ | −3.1·10⁻³ | +6.6·10⁻² | −6.9·10⁻² | +1.32 |
| SECOND, c = 0.7 | 0.14109 | 0.13903 | +9.0·10⁻⁵ | −3.4·10⁻³ | +4.5·10⁻³ | −7.8·10⁻³ | +0.530 |

**Andamento lungo il ramo** (`flrw_comparison.out`). In BASE vale
1.0045 ≤ 𝓔/E_FLRW(f̂) ≤ 1.29 lungo tutto il ramo campionato:

- 1.0065 a c/m₀ = 10⁻⁶;
- 1.29 attorno a c/m₀ = 2·10⁻²;
- 1.018 a c = 1;
- 1.0045 a c/m₀ = 150.

**Lettura.** Le medie di BASE sono, entro qualche percento, quelle di un FLRW
aperto con lo stesso Ω_c. La correzione è di segno sbagliato ed è dominata
dal peso λ² della densità (ρ_λ > ρ₀), non dalla retroazione cinematica Q_λ.

### 3.4 Proposizione B: asintotica vicino al bang

**Derivazione formale** (espansioni raccordate).

1. **Geometria locale.** R = r a₀(s)[1 + εk + O(ε²)], e quindi Θ = (2/s)[1 + (ε/3)(3k + rk_r)] + O(ε²/s).
2. **Soluzione esterna della CMC.** Il centro fissa K: la soluzione omogenea regolare cresce come sinh(r/ℓ_r)/(r/ℓ_r) ed è soppressa in modo esponenziale, con ℓ_r definita al punto 3. Ne segue, con u = S − c,

   $$u(r)=\frac{\varepsilon c}{3}\,[\,3k+rk_r-3k(0)\,]+O(\varepsilon^2c).$$
3. **Strato limite all'ancora esterna.** L'ancora S(c,1) = c impone uno strato di ampiezza −u(1).
   - **Equazione.** Nello strato l'equazione si riduce a u_rr = (2A(1)²/c²)u, con A(1) ≈ a₀(c)/√(1+k(1)) e a₀(c) = (9m₀/2)^{1/3}c^{2/3}.
   - **Larghezza nell'etichetta r** (adimensionale):

     $$\ell_r=\frac{c\sqrt{1+k(1)}}{\sqrt2\,a_0(c)}=\sqrt{\frac{1+k(1)}{2}}\;\Big(\frac{2c}{9m_0}\Big)^{1/3}\;\propto\;\Big(\frac{c}{m_0}\Big)^{1/3}.$$
   - **Unità interne.** Nelle unità interne del solver (lunghezze divise per c) si ha a₀ = (9m₀/(2c))^{1/3}, e la stessa espressione si scrive ℓ_r = √(1+k(1))/(√2 a₀). È la forma usata negli script.
   - **Spessore proprio.** A(1)ℓ_r = c/√2: lo strato ha spessore proprio della scala di Hubble, indipendente da m₀ e da k(1).
   - **Centro.** Non c'è strato al centro.
4. **Volume.** Sommando i contributi:

   $$\frac{V}{6\pi GMc^2}=1+\varepsilon W+\beta\,\frac{c}{m_0}+O(\varepsilon^2),$$

   $$W=\frac53\Big\langle\frac{(r^3k)_r}{r^2}\Big\rangle_w-2k(0),\qquad
   \beta=-\frac{\sqrt2}{30}\,\frac{3k(1)+k_r(1)-3k(0)}{I_w},$$

   dove ⟨·⟩_w è la media con peso w = r²/√(1+r²k).
5. **Algebra generale.** Se V = 6πGMc²(1 + αc^p), allora:
   - 1 − Ω = (1+p)αc^p;
   - f̂ ≈ (1+p)αc^p/3;
   - 𝓔 ≈ (3/4)(1 − p²)αc^p, cioè **𝓔/f̂ → (9/4)(1 − p)**.

   Con p = 2/3 (modo crescente) si ottiene 𝓔/f̂ → 3/4. Con p = 1 (frazione di vuoto lineare, come nel tracker) si ottiene 𝓔 = 0 al primo ordine. Quindi il termine di strato limite **non entra** in 𝓔 all'ordine c.

**Risultato:**

$$1-\Omega_c=\tfrac53W\varepsilon+2\beta\frac{c}{m_0}+O(\varepsilon^2),\qquad
\mathcal E=\tfrac{5}{12}W\varepsilon+O(\varepsilon^2).$$

**Conferma numerica del primo ordine** (`near_bang_*.out`, `general_profile.out`).
I profili con nucleo aperto e quello con W < 0 sono fuori dalla famiglia
selezionata:

| Caso | W | c/m₀ | 𝓔/ε osservato | 5W/12 | Scarto relativo |
|---|---|---|---|---|---|
| BASE | 0.998593 | 10⁻⁶ | 0.416055 | 0.416080 | −6.1·10⁻⁵ |
| BASE | | 10⁻⁵ | 0.415963 | | −2.8·10⁻⁴ (∝ ε) |
| SECOND | 1.992081 | 10⁻⁶ | 0.829958 | 0.830034 | −9.1·10⁻⁵ |
| k uniforme 0.2 (FLRW aperto) | 0.6 | 10⁻⁶ | 0.249997 | 0.25 | −1.3·10⁻⁵ |
| nucleo aperto, 0.1 → 0.4 | 1.795918 | 10⁻⁶ | 0.748242 | 0.748299 | −7.7·10⁻⁵ |
| nucleo aperto, 0.3 → 0.2 (verifica il termine −2k(0)) | 0.400552 | 10⁻⁶ | 0.166902 | 0.166897 | +3.0·10⁻⁵ |
| 0.3 → 0.1 | −0.0996 | 10⁻⁶ | Ω_c > 1: fuori dal dominio di P187, come previsto | | |

Lo scarto di BASE cresce di 10^{2/3} per decade. È quindi di ordine ε, e un
termine di ordine c in 𝓔 è assente, come previsto.

**Conferma del termine lineare di 1 − Ω** (`linear_term_check.out`):

| Caso | Scarto senza termine lineare | Scarto con termine lineare |
|---|---|---|
| BASE, c/m₀ = 10⁻⁶ | −6.5·10⁻³ | +1.8·10⁻⁵ |
| SECOND, c/m₀ = 10⁻⁶ | −6.8·10⁻³ | +4.3·10⁻⁶ |
| W < 0 (0.3 → 0.1), c/m₀ = 10⁻⁶ | −6.4·10⁻² | +2.9·10⁻⁴ |
| compensato (W = 0), c/m₀ = 10⁻⁶ | il solo termine lineare prevede 1.5842·10⁻⁷, osservato 1.5775·10⁻⁷ | −4.3·10⁻³ |

**Classificazione:** DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION. È una
derivazione formale, senza stime d'errore rigorose, confermata numericamente
a due ordini.

### 3.5 Corollario C: la famiglia selezionata

Nella famiglia selezionata k = κ*χ(r), con χ(0) = 0, χ' ≥ 0 e κ* > 0. Allora

W = (5/3)⟨(r³k)_r/r²⟩_w > 0

in senso stretto. Vicino al bang ne segue:

- 𝓔 ≈ (3/4)f̂ > 0;
- b̂ ≈ c/f̂ ∝ c^{1/3} → 0: il parametro ricostruito deriva verso zero, e un b costante non esiste.

Per κ* = 0 si ha Ω ≡ 1, che è fuori dal dominio.

Con il Teorema A se ne conclude che **nessun membro della famiglia
selezionata soddisfa P187 su alcun intervallo del proprio ramo**, sotto tre
ipotesi:

- **(H_A)** il quadro del Teorema A e di P187 (§3.2): ramo continuo di sezioni ancorate regolari, J > 0 e 0 < Ω_c < 1, mappa di clock selezionata. La dimostrazione del Teorema A è uno schizzo.
- **(H_B)** il ramo raggiunge il regime vicino al bang. È verificato numericamente per BASE e SECOND fino a c/m₀ = 10⁻⁶, ma non è dimostrato.
- **(H_asym)** l'espansione formale della Proposizione B è valida. È confermata numericamente, senza stime d'errore rigorose.

Per un singolo insieme di parametri bastano invece H_A e il Corollario A1,
con un solo valore calcolato 𝓔 ≠ 0.

**Interpretazione.**

- **Perché fallisce.** Con densità regolare al bang, l'inomogeneità cresce come il modo crescente, con esponente 2/3. Il tracker richiede invece una frazione di vuoto che cresce linearmente (vuoti di Milne vuoti), e il criterio P187 misura proprio questa differenza di esponente.
- **Scala dell'ostruzione.** Coincide, a meno di pochi percento, con quella di un FLRW aperto (§3.3).

### 3.6 Settore generale: fuori dalla famiglia selezionata

Considero profili k(r) ≥ 0 qualsiasi, anche con nucleo aperto. Con H_A, H_B
e H_asym, il matching su un intervallo richiede:

- **(N1)** W[k] = 0 (compensazione);
- **(N2)** 3k(0) > 3k(1) + k_r(1), altrimenti Ω_c > 1 oppure b̂ < 0;
- **(N3)** C = 0 e b = 45 m₀ I_w / [√2 (3k(0) − 3k(1) − k_r(1))]. Il b del tracker sarebbe dunque fissato dai dati di curvatura;
- **(N4)** l'annullarsi del coefficiente di ε² in 𝓔, e così via a tutti gli ordini.

Il termine esterno contiene solo potenze di c^{2/3}. Quindi il termine
lineare "di vuoto" del tracker può provenire **soltanto** dallo strato limite
all'ancora esterna.

**Esempio esplicito** (`compensated_profile.out`). Il profilo è
k = 0.3 + (0.1199 − 0.3)χ(r), cioè un vuoto centrale in un fondo meno aperto,
con W = 0:

| c/m₀ | 1 − Ω_c | f̂ | b̂ | 𝓔 | 𝓔/ε² |
|---|---|---|---|---|---|
| 10⁻⁶ | 1.5775·10⁻⁷ | 5.258·10⁻⁸ | 3.8036 | +1.7·10⁻¹⁰ | 0.626 |
| 10⁻⁵ | 1.5695·10⁻⁶ | 5.232·10⁻⁷ | 3.8228 | +3.7·10⁻⁹ | 0.631 |
| 10⁻⁴ | 1.5523·10⁻⁵ | 5.174·10⁻⁶ | 3.8652 | +8.0·10⁻⁸ | 0.634 |
| 4.365·10⁻⁴ | | | 3.9006 | 0 (zero isolato) | |
| 10⁻³ | 1.5579·10⁻⁴ | 5.193·10⁻⁵ | 3.8510 | −4.4·10⁻⁶ | −1.61 |
| 3·10⁻³ | 5.1049·10⁻⁴ | 1.702·10⁻⁴ | 3.5246 | −4.6·10⁻⁵ | −3.92 |

**Che cosa mostra l'esempio.**

- **Limite di b̂.** (N3) prevede b̂(0⁺) = 3.7873. L'estrapolazione in c^{1/3} dei primi due punti dà 3.7870.
- **Offset.** Ĉ/c → 0.
- **La compensazione funziona.** Toglie l'ostruzione dominante e produce un comportamento molto vicino a un tracker: b̂ entro il 3% su tre decadi.
- **Ma non basta.** 𝓔 ≈ 0.63 ε² ≠ 0. Lo zero a c/m₀ = 4.37·10⁻⁴ è una tangenza istantanea e non una propagazione, come richiede il Teorema A.

**Stato.** Nel settore generale il problema non è né risolto né escluso. È
ridotto a una successione infinita di condizioni scalari su una sola funzione
k(r), più la rigidità analitica. Conosco esplicitamente le prime tre
(N1–N3).

### 3.7 Esito del primo punto

- **Famiglia selezionata.** Il problema è chiuso **in senso negativo sotto H_A, H_B e H_asym**. Per BASE, e per ogni parametro specifico calcolato, bastano H_A e il valore calcolato 𝓔 ≠ 0: non servono H_B né H_asym.
- **Settore generale LTB a bang simultaneo.** Il problema resta aperto, ma con condizioni necessarie esplicite e un meccanismo identificato: la compensazione di W più lo strato limite all'ancora esterna.

---

## 4. Secondo punto aperto: trasferimento degli stati locali a H1

### 4.1 Che cosa richiede H1 nel repository

- **(R1) Due regioni FLRW esatte.** Muro e vuoto hanno background di polvere FLRW esatti, con 13 identità verificate sotto `ENFORCE`: righe regionali di Hamilton, Raychaudhuri e continuità; partizione; espansione media; Q̄ = (2/3)f_v f_w(Θ_v − Θ_w)²; W̄; e le equazioni GM (3.8)–(3.10) (report F3, §2.3).
- **(R2) Clock CLK-H1.** Il tasso regionale è omogeneo, la dipendenza spaziale è esclusa, il lapse perturbativo non è definito, e si richiede J_Ξ = 0 (F3 §2.4; 1E-E §11).
- **(R3) Geometria fissa.** Partizione e interfaccia sono fisse e lagrangiane, i pullback comoventi, le metriche regionali e di destinazione indipendenti dal tempo: Ȧ_Γ = 0, L̇_D = 0, J_f = 0 (1E-G).
- **(R4) Interfaccia senza stato.** Γ è un'interfaccia matematica di misura nulla, senza stato di spostamento e senza sorgenti superficiali (1E-F §1, §3).
- **(R5) Stato e dinamica.**
  - Lo stato è Y_bulk = (Δ_w, Z_w, Δ_v, Z_v), con le equazioni regionali della polvere.
  - La destinazione è Δ_d = m_w T_w[Δ_w] + m_v T_v[Δ_v] + d_F F_v, con F_v determinato dagli altri campi.
  - Le verifiche dinamiche sono R_Z = R_eff = 0 (1E-F §5–7).

"Conservare dinamica, vincoli e closure" significa che l'immagine degli stati
LTB soddisfa (R1)–(R5) entro le tolleranze imposte.

### 4.2 Teorema D: due FLRW distinti non confinano

**Enunciato.** Consideriamo uno spaziotempo di polvere a simmetria sferica
(LTB), con raggio areale continuo e senza shell crossing. Se due regioni
materiali sono regioni di polvere FLRW esatte (Λ = 0) e condividono un guscio
di bordo r₁, sono la stessa regione FLRW. Quindi una decomposizione
muro/vuoto in due FLRW esatti *distinti* richiede un insieme di gusci di
separazione di estensione positiva. Su ogni sezione spaziale regolare questo
insieme ha volume positivo.

**Dimostrazione.**

- In una regione FLRW esatta R(t,r) = a_i(t)Σ_i(r).
- La continuità di R in r₁ dà a₁(t)Σ₁(r₁) = a₂(t)Σ₂(r₁) per ogni t. Quindi a₁/a₂ è costante e H₁ ≡ H₂.
- Raychaudhuri, Ḣ + H² = −(4πG/3)ρ, dà ρ₁ ≡ ρ₂.
- Friedmann dà k₁/a₁² = k₂/a₂².
- La geometria locale è dunque la stessa. ∎

**Classificazione:** DERIVED_FROM_GENERIC_GR.

**Conseguenza per H1, sotto l'identificazione geometrica materiale (IM).**

**Che cosa assume IM.** Le regioni muro e vuoto di H1 sono identificate con
due regioni materiali LTB, cioè insiemi di gusci di polvere, i cui background
sono FLRW di polvere esatti. L'interfaccia Γ di H1 ha misura nulla e non porta
stato (R4).

**Che cosa segue.**

- La regione di separazione richiesta dal Teorema D non ha controparte in H1.
- L'identità di partizione f_w + f_v = 1, con f_r = V_r/V, non può valere.
- Assorbire la separazione in una delle due regioni violerebbe IM stessa, perché quella regione non sarebbe FLRW.
- Quindi, sotto IM, un trasferimento esatto non esiste. Questo è l'unico no-go H1 dimostrato in questo report.

**Che cosa non copre.** Non dice nulla su identificazioni diverse da IM, per
esempio:

- regioni H1 non identificate con insiemi di gusci;
- background regionali intesi come medie su regioni non omogenee;
- regioni di riferimento del carrier legate alla geometria LTB da mappe non materiali.

### 4.3 Proposizione E: dove sta l'inomogeneità nella famiglia selezionata

**Enunciato.** Nella famiglia selezionata lo spaziotempo è esattamente EdS
per r < r_c ed esattamente FLRW aperto per r > r_o. Ogni inomogeneità
indipendente dallo slicing sta in (r_c, r_o), dove k_r ≠ 0:

- lo shear σ² = (H_l − H_p)²/3, che si annulla se e solo se k_r = 0;
- il gradiente di densità sulle sezioni a età propria costante.

**Peso della transizione in BASE** (c = 1, `h1_regional_BASE.out`): la
transizione porta il 34.19% del volume e il 33.72% della massa a riposo.

**Lettura sotto IM.**

- **Le regioni sono le parti FLRW esatte.** Nucleo ed esterno sono le uniche regioni ammesse da IM, e la transizione resta scoperta (Teorema D).
- **Un'ulteriore identificazione, non dimostrata.** Supponiamo inoltre che le sorgenti regionali di H1 siano le perturbazioni della polvere, nel suo sistema di riposo, rispetto al background FLRW regionale. Allora Y_bulk = 0. Per linearità, e perché F_v è determinato dagli altri campi, la destinazione sarebbe Δ_d = 0.
- **Assorbire la transizione in una regione non è ammesso da IM.** Ciò che accade con altre regole di assegnazione l'ho esaminato solo per la mappa M1 (§4.5).

Sulle sezioni CMC i campi variano anche dentro le regioni esatte. È un effetto
di slicing: la sezione taglia età della polvere diverse. Che queste variazioni
non siano perturbazioni della polvere compatibili con le equazioni regionali è
un'osservazione qualitativa, non verificata in dettaglio. Non fa parte del
no-go.

### 4.4 Proposizione F: le sezioni ancorate non sono sincrone su entrambe le regioni esatte

**Enunciato.** Con le ancore S(c,0) = S(c,1) = c, la sezione CMC non può
essere sincrona sia vicino al centro (EdS) sia vicino al bordo (FLRW aperto).

**Dimostrazione.**

- Un tratto sincrono di FLRW ha ξ = 0, quindi K = −Θ_FLRW(c).
- Le ancore darebbero allora −K = 2/c e −K = Θ_aperto(c) contemporaneamente.
- Ma cΘ_aperto(c) > 2 per κ* > 0: contraddizione. ∎

**Numeri** (BASE, `h1_regional_BASE.out`).

| Regione | S/c a c = 1 | λ a c = 1 |
|---|---|---|
| nucleo | [1, 1.00119] | [1, 1.00112] |
| esterno | [1.0000006, 1.00305] | [1.000001, 1.00290] |

- **Vicino al bang.** Il nucleo è sincrono a meno di termini esponenzialmente piccoli. Nell'esterno la sezione esterna allo strato ha S − c ≈ εcκ*. Ne segue λ − 1 ≈ (5/3)εκ*: a c/m₀ = 10⁻⁵ si osserva 2.6·10⁻⁵, contro 2.55·10⁻⁵ previsto.
- **Che cosa è λ.** λ = ∂_cS è il rapporto locale fra l'età propria della polvere e il parametro c, a etichetta fissa: di quanto avanza l'età della polvere per unità di c lungo la famiglia di sezioni. Il solver lo documenta come "dS/ds_c, not a physical wall lapse".
- **Che cosa non ne segue: ν_W.** La disomogeneità di λ non è stata derivata come lapse perturbativo dell'osservatore wall ν_W (oggi `NOT_DEFINED`), e non la identifico con esso.
- **Che cosa non ne segue: α_r.** L'identificazione di λ con il clock regionale omogeneo α_r di CLK-H1 (R2) richiede una mappa esplicita. M1 ne propone una, α_r = ⟨λ⟩_r (§4.5). Senza una mappa di questo tipo, dalla disomogeneità di λ non segue alcuna affermazione né su CLK-H1 né su ν_W.
- **Classificazione.** La Proposizione F riguarda solo la non sincronia delle sezioni.

### 4.5 Verifica con il codice H1 del repository

**La mappa usata (M1).** Ho costruito un `H1Background` dalla famiglia
LTB–CMC con una mappa esplicita. È una scelta, esatta per regioni FLRW
sincrone. I risultati di questa sezione valgono solo per M1 e per le due
assegnazioni della transizione indicate, e non si estendono ad altre mappe.

In M1, α_r = ⟨λ⟩_r è la mappa esplicita, scelta e non derivata, fra il
rapporto cinematico λ e il clock regionale omogeneo α_r. Un'altra mappa
esplicita potrebbe dare esiti diversi.

- tempo comune t_D = c; f_v = V_v/V;
- Ξ_r = ⟨λΘ⟩_r; α_r = ⟨λ⟩_r; Θ_r = Ξ_r/α_r; ρ_r = M_r/V_r; R̄_r = ⟨R_u⟩_r;
- Θ = 3J, Q̄ = Q_λ, W̄ = R_λ, K_D = 0;
- i getti temporali sono calcolati con differenze finite in c, solo come strumento di test.

**Esecuzione.** Ho eseguito la funzione del repository
`two_region_background_identity_residuals` (`h1_gates_on_ltb.out`). Residui
relativi a Θ², per BASE a c = 1:

| Riga | Muro = nucleo + transizione | Muro = nucleo |
|---|---|---|
| Hamilton regionale, muro | 2.0·10⁻⁴ | 1.1·10⁻⁶ |
| Hamilton regionale, vuoto | 8.7·10⁻⁶ | 1.4·10⁻⁴ |
| Raychaudhuri regionale, muro/vuoto | 7.1·10⁻⁷ / 6.3·10⁻⁷ | 9.9·10⁻⁸ / 5.0·10⁻⁵ |
| retroazione a due regioni (riga 9) | 9.0·10⁻⁷ | 8.3·10⁻⁵ |
| W̄ mediato (riga 10) | 3.7·10⁻³ | 3.7·10⁻³ |
| GM (3.8) Hamilton mediato | 8.1·10⁻³ | 8.1·10⁻³ |
| GM (3.9) Raychaudhuri mediato | 1.1·10⁻³ | 1.1·10⁻³ |
| continuità, partizione, espansione media, GM (3.10) | ≤ 1.1·10⁻⁷ (rumore numerico) | ≤ 1.1·10⁻⁷ |

**Lettura.**

- **Righe automatiche.** Le righe che valgono per costruzione per regioni materiali passano.
- **Righe violate, con M1.** Falliscono di molti ordini sopra qualunque tolleranza di chiusura:
  - le righe regionali di Hamilton e Raychaudhuri;
  - la riga 9;
  - le righe medie GM.
- **Retroazione a due regioni, con M1.** Il confronto diretto delle retroazioni (`h1_regional_BASE.out`) mostra che la formula a due regioni sbaglia la Q totale di un fattore O(1) o più, con entrambe le assegnazioni:
  - con la transizione nel muro il residuo è +239 in forma relativa;
  - con il muro ridotto al solo nucleo è −0.98.
- **Vincolo K3 del report F3.** F3 aveva già notato che le righe regionali, la riga 9 e GM (3.8) sono compatibili solo se Σf_rα_rΘ_r = Σf_rΘ_r. In M1 i valori definiti come α_r = ⟨λ⟩_r sono α_w = 1.0033 e α_v = 1.0014, quindi la condizione non vale per M1. La conclusione dipende da questa mappa, e non riguarda ν_W.

### 4.6 Nota condizionata: l'operatore L_D

**Questa sezione non fa parte del no-go.** Presuppone di identificare L_D con
un Laplaciano delle sezioni LTB–CMC nelle etichette comoventi. Non ho
dimostrato questa identificazione, e non è IM.

**La grandezza misurata.** Sul ramo implementato la metrica di destinazione
deve essere indipendente dal tempo (R3). Misuro la deriva non conforme della
metrica delle sezioni h(c) = B²dr² + R²dΩ² nelle etichette comoventi:

τ = ∂_c ln B − ∂_c ln R = λ(H_l − H_p) − ∂_c ln γ (`conformal_drift.out`).

**Unità.**

- τ ha dimensione 1/lunghezza, con c = 1.
- L'output registrato è in unità interne (lunghezze divise per c): contiene cτ, adimensionale.
- τ in unità fisiche si ottiene dividendo per c, cioè per 1 e per 0.2. È solo aritmetica sui valori registrati.
- Per un confronto senza unità, riporto anche il rapporto con la media, sui punti campionati di ciascuna regione, del tasso di espansione areale: c·∂_c ln R vale 0.667–0.721 a c = 1 e 0.667–0.687 a c = 0.2, a seconda della regione.

| Regione | c·max\|τ\|, c = 1 | max\|τ\|, c = 1 [1/lunghezza] | c·max\|τ\|, c = 0.2 | max\|τ\|, c = 0.2 [1/lunghezza] |
|---|---|---|---|---|
| nucleo | 2.6·10⁻⁵ | 2.6·10⁻⁵ | 1.3·10⁻⁵ | 6.4·10⁻⁵ |
| transizione | 9.7·10⁻² | 9.7·10⁻² | 4.2·10⁻² | 2.1·10⁻¹ |
| esterno | 3.3·10⁻⁵ | 3.3·10⁻⁵ | 1.9·10⁻⁵ | 9.4·10⁻⁵ |

**Rapporto con il tasso medio.** Nella transizione la deriva vale circa il 14%
del tasso medio ∂_c ln R a c = 1 (0.0967/0.696) e il 6% a c = 0.2
(0.0421/0.678). Nelle regioni esatte vale ≲ 10⁻⁴.

**Lettura, sotto l'identificazione indicata.** Nessuno dei due Laplaciani di
P189 è un operatore fisso:

- D²_{Σ_c} evolve in modo non conforme, soprattutto nella transizione;
- D²_u, scritto in coordinate (c, r), contiene ∂_c.

Con quell'identificazione L̇_D = 0 non varrebbe. Senza di essa, questa sezione
non dice nulla.

### 4.7 Relazione con il criterio ker D𝒜 ⊆ ker D𝓑 di P188

**Dentro H1 stesso.** Il trasferimento dipende dalla morfologia, che è un
input esterno obbligatorio. Il report 1E-G misura, a parità di ampiezze
latenti, differenze di 0.63, 0.32 e 1.90 fra due morfologie. La morfologia
non fa parte dei dati mediati. Quindi, se 𝓑 è il campo trasferito, anche in
H1 l'inclusione dei nuclei fallisce, a meno di includere la morfologia fra
gli input.

**Il pezzo mancante.** L'informazione radiale che P189 recupera dalle medie
annidate andrebbe tradotta in una morfologia del carrier. Nel repository non
esiste una mappa che lo faccia.

### 4.8 Esito del secondo punto

**Che cosa è dimostrato.**

- **Sotto IM** (§4.2): un trasferimento **esatto** in H1 non esiste, per ogni famiglia LTB–CMC sferica con due regioni FLRW distinte. Segue dal Teorema D.
- **Con la mappa M1** (§4.5): nella famiglia selezionata i gate del repository indicati sono violati. Il risultato vale solo per M1.
- **Fatti geometrici** (Proposizioni E ed F): il supporto dell'inomogeneità nella transizione e la non sincronia delle sezioni ancorate.

**Che cosa non è dimostrato.**

- Non ho mostrato che il trasferimento sia impossibile per identificazioni diverse da IM, né per mappe diverse da M1.
- La nota sul Laplaciano (§4.6) dipende da un'identificazione non dimostrata.
- Dalla disomogeneità di λ non segue un risultato su ν_W. Su CLK-H1 segue solo tramite una mappa esplicita verso α_r, e ho esaminato soltanto M1.
- Il secondo punto aperto resta quindi aperto al di fuori di IM.

**Che cosa servirebbe sotto IM per un enunciato positivo.** Una terza
regione, oppure un'interfaccia di misura positiva dotata di un proprio stato e
di proprie sorgenti. Sarebbe una nuova equazione di modello che, secondo
AGENTS.md, richiede autorizzazione umana; non l'ho introdotta.

La mappa dalla morfologia sferica a medie annidate verso la morfologia del
carrier (§4.7) resta comunque un ingrediente mancante. È coerente con la voce
`H1_TO_WALL_DRESSED_SPATIAL_REALIZATION_AND_DENSITY_CODOMAIN_MAP`, già
elencata in `REMAINING_SCIENTIFIC_CLOSURES`.

---

## 5. Classificazioni e stato

| Risultato | Classificazione |
|---|---|
| Teorema A (rigidità analitica) | DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION; schizzo di dimostrazione |
| Identità 𝓔 = E_FLRW − 𝓑/(3J²) | identità algebrica esatta nello stesso settore di P187 |
| Proposizione B | DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION; formale, confermata numericamente |
| Corollario C | DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION, condizionato a H_A, H_B e H_asym |
| Teorema D | DERIVED_FROM_GENERIC_GR |
| No-go H1 (§4.2) | vale solo sotto l'identificazione geometrica materiale IM |
| Violazione dei gate H1 (§4.5) | evidenza numerica, solo per la mappa M1 |
| Proposizione E (supporto dell'inomogeneità) | DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION (settore selezionato) |
| Proposizione F (non sincronia delle sezioni ancorate) | DERIVED_ONLY_AFTER_ADDITIONAL_ASSUMPTION (settore e ancore selezionati) |
| Nota su L_D (§4.6) | condizionata a un'identificazione non dimostrata; fuori dal no-go |
| Tabelle numeriche | evidenza numerica per campioni, non certificati |

Restano invariati, e non ho modificato `scientific_status.py`:

```text
REGIONAL_COMMON_TIMESCAPE_BACKGROUND_EMBEDDING: NOT_DERIVED
ALL_TIME_TRANSFER_CONSTITUTIVE_COMPATIBILITY: NOT_DERIVED
PHYSICAL_TIMESCAPE_TRAJECTORY_EXISTENCE: NOT_DERIVED
UNIQUE_TIMESCAPE_PREDICTION: NOT_GRANTED
OBSERVATIONAL_AUTHORIZATION: NOT_GRANTED
RSD_AUTHORIZATION: NOT_GRANTED
SIGMA8_AUTHORIZATION: NOT_GRANTED
FSIGMA8_AUTHORIZATION: NOT_GRANTED
```

I risultati del §3 costituiscono evidenza per un eventuale audit su
`PHYSICAL_TIMESCAPE_TRAJECTORY_EXISTENCE` nella famiglia selezionata. Non li
ho usati per cambiare alcuno status. Phase 1F-D non è dichiarata risolta.

---

## 6. Limiti

- **La Proposizione B non è rigorosa.** Mancano stime d'errore per il problema singolarmente perturbato. La conferma numerica arriva fino a c/m₀ = 10⁻⁶.
- **H_B non è dimostrata.** Non ho provato che il ramo resti connesso fino al bang.
  - In alcuni punti vicini al bang il BVP del lapse ha superato il limite di nodi, anche con 40000 nodi: BASE a c/m₀ ∈ [2·10⁻⁵, 10⁻⁴] e SECOND a 10⁻⁵.
  - Il problema CMC era risolto in quei punti. È un fallimento numerico, non un'assenza di soluzione, e quei punti non entrano nelle conclusioni.
- **Il Teorema A è uno schizzo.** Gli ingredienti sono standard, ma non ho scritto la dimostrazione completa in spazi di funzioni.
- **Profili esplorati.** Solo k ≥ 0 e m = m₀r³, perché il solver inverte l'età solo per curvatura aperta. I profili esterni alla famiglia sono stati trattati con una sostituzione temporanea di `curvature()` nel processo di scratch.
- **La mappa M1 è una scelta.**
  - La violazione dei gate vale solo per M1.
  - Il Teorema D e le Proposizioni E ed F non dipendono da M1.
  - Il no-go H1 vale solo sotto IM.
- **λ e i clock di H1.**
  - λ = ∂_cS è il rapporto locale fra età propria della polvere e parametro c.
  - La sua disomogeneità non è identificata con il lapse perturbativo dell'osservatore wall ν_W: sarebbe un'identificazione non derivata.
  - L'identificazione con il clock regionale omogeneo α_r richiede una mappa esplicita. M1 ne è una scelta.
- **Getti temporali.** I getti usati per i gate H1 sono differenze finite in c.
- **Settore generale.** L'esistenza di una famiglia con 𝓔 ≡ 0 resta aperta.
- **Audit dell'export.** Non ho eseguito l'audit dell'export della sensibilità mista, che il report di partenza segnalava come aperto.
- **Repository, al momento della stesura.** Nessun codice aggiunto al package, nessun file del repository modificato, nessuna operazione git. Il report è stato aggiunto a `reports/` in seguito, su richiesta, senza script né output.

---

## 7. Riproducibilità

**Stato del repository durante i calcoli.** HEAD
`4f28a095e6401c31e0a90dfc4c35ae92cbc0592d`, con i 15 file dell'esperimento
non tracciati e nessun file tracciato modificato. Quei file sono ora nel
commit `6fad383`, con contenuto identico. Input del package usati:

```text
18e91aa2052329e0f53d81fb8b2cb9cad3d09f2746d58e2115b3389a3e0edaea  src/timescape_fsigma8/experimental_ltb_cmc/geometry.py
29e5bf7205cfd78778465e47c4332190a52fef8e092ce56829d223c3c746d980  src/timescape_fsigma8/experimental_ltb_cmc/solver.py
16b0c5983cca8947ea42535f92d4adc56bf00395b6f4ab8d4467dd9712d1a34f  src/timescape_fsigma8/experimental_ltb_cmc/evolution.py
ecc8d5495dff4d17dbe2c11c3d052207406cd8eced3d27c4d678c7614d1d9ac1  src/timescape_fsigma8/experimental_ltb_cmc/clock.py
622e1b3d974f2858148d5afeb76c6005f456f68bedde663d1fd3409cf799e97e  src/timescape_fsigma8/experimental_ltb_cmc/__init__.py
de4bf78e13378610b8a2f4d075ab7124f4b279b35da3fcb7b76b7000bf3d3714  src/timescape_fsigma8/transfer/h1_realization.py
a9350e244e1ad6e15af48c3f39141fb98e6da97ae8d5ec847e68c286e13ac685  src/timescape_fsigma8/transfer/matrix_backend.py
16bef0c8f2cdd3ad5dead6d07555fbe2c3061930bbc2dd519e0d1ad0379544a8  src/timescape_fsigma8/scientific_status.py
```

**Dove sono gli script.** Script e output non sono nel repository. Sono
nell'archivio `prosecuzione_P187_P189_20260925.zip` (SHA-256
`c7362cba791e6ccb9bd8bd8c7f9d46de757e112418689c682ef4b116a4ae2565`),
consegnato a parte, insieme alla versione originale di questo report.

**Come eseguire.** Una volta estratto l'archivio, gli script si lanciano
dalla radice del repository, con `<cartella>` uguale alla cartella estratta:

```sh
PYTHONPATH=<cartella> .venv/bin/python -B -W error <cartella>/<script>.py [argomenti]
```

Gli output sono stati scritti con `tee` durante le esecuzioni.

| Script | Argomenti | Output | Contenuto |
|---|---|---|---|
| `p187_common.py` | — | — | Ricostruzione P187, tracker, modelli BASE e SECOND, preset TIGHT |
| `p187_base_table.py` | — | `p187_base_table.out` | Tabella BASE e derivate con differenze finite (§2.1) |
| `near_bang_scan.py` | `BASE` | `near_bang_BASE.out` | 𝓔(c) su sette decadi e W (§3.4) |
| `near_bang_fill.py` | `BASE …`, `SECOND …`, `BASE 15 … 150` | `near_bang_BASE_fill.out`, `near_bang_SECOND.out`, `late_BASE.out` | Punti vicini al bang e tardivi |
| `general_profile.py` | — | `general_profile.out` | Profili fuori dalla famiglia selezionata, test di W e del termine −2k(0) |
| `linear_term_check.py` | — | `linear_term_check.out` | Termine lineare di strato limite in 1 − Ω |
| `compensated_profile.py` | — | `compensated_profile.out` | Profilo con W = 0: b̂(0⁺), zero isolato di 𝓔 |
| `flrw_comparison.py` | — | `flrw_comparison.out` | 𝓔/E_FLRW lungo i rami (legge solo gli output registrati) |
| `backreaction_split.py` | — | `backreaction_split.out` | Identità 𝓔 = E_FLRW − 𝓑/(3J²) |
| `h1_regional_diagnostics.py` | `BASE 5 1e-3 1e-5` | `h1_regional_BASE.out` | Regioni, retroazioni regionali, S/c e λ per regione, frazione della transizione |
| `h1_gates_on_ltb.py` | `1.0` | `h1_gates_on_ltb.out` | Gate H1 del repository sulla mappa M1 |
| `conformal_drift.py` | — | `conformal_drift.out` | Deriva non conforme della metrica delle sezioni |

Gli SHA-256 di tutti i file sono in `SHA256SUMS.txt`, nella stessa cartella.
