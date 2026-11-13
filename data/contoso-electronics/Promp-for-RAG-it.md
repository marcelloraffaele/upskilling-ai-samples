# Prompt di esempio per una demo RAG - Contoso Electronics / Northwind Health

## Obiettivo della demo

Questi prompt sono pensati per mostrare come un agente RAG possa:

- recuperare informazioni puntuali da una knowledge base;
- combinare informazioni provenienti da documenti diversi;
- confrontare piani e policy;
- produrre risposte strutturate e citare le fonti;
- gestire domande ambigue o non coperte dai documenti;
- mantenere il contesto nelle domande successive.

> Nota: i documenti dichiarano che i contenuti sono dati sintetici generati a scopo dimostrativo. Non rappresentano veri piani assicurativi o policy aziendali.

## Documenti della knowledge base

- `Benefit_Options.pdf`: panoramica e confronto tra Northwind Health Plus e Northwind Standard.
- `Northwind_Standard_Benefits_Details.pdf`: dettagli, costi e coperture del piano Northwind Standard.
- `Northwind_Health_Plus_Benefits_Details.pdf`: dettagli, costi e coperture del piano Northwind Health Plus.
- `employee_handbook.pdf`: missione, valori, performance review, sicurezza, privacy, whistleblowing, data security e ruoli aziendali di Contoso Electronics.

---

# 1. Prompt introduttivi

Questi prompt permettono di iniziare la demo con domande semplici e facilmente verificabili.

### Prompt 1 - Panoramica dei piani

```text
Quali piani sanitari sono disponibili per i dipendenti di Contoso Electronics? Per ciascun piano, riassumi in massimo cinque punti le principali coperture e cita il documento utilizzato.
```

**Informazioni che l'agente dovrebbe recuperare:**

- Northwind Health Plus e Northwind Standard;
- copertura medica, dentale e oculistica;
- differenze generali relative a emergenze, salute mentale, farmaci e servizi fuori rete.

### Prompt 2 - Sintesi orientata al dipendente

```text
Sono un nuovo dipendente di Contoso Electronics. Preparami una breve introduzione ai benefit sanitari disponibili, usando un linguaggio semplice e indicando dove posso trovare maggiori dettagli.
```

### Prompt 3 - Risposta tabellare

```text
Crea una tabella comparativa tra Northwind Health Plus e Northwind Standard con queste colonne: servizi medici, prevenzione, farmaci, emergenze, salute mentale, cure fuori rete, vista e dentista. Per ogni affermazione indica la fonte.
```

---

# 2. Prompt per mostrare il retrieval puntuale

### Prompt 4 - Costi del piano Standard

```text
Quali sono la franchigia annuale individuale, il copay per una visita dal medico di base, il copay per uno specialista, la coinsurance e il limite massimo annuale di spesa del piano Northwind Standard? Rispondi con un elenco e cita la fonte per ogni valore.
```

**Elementi verificabili nella knowledge base:**

- franchigia individuale annuale di 2.000 dollari;
- copay di 30 dollari per il medico di base;
- copay di 50 dollari per lo specialista;
- coinsurance del 20% dopo la franchigia;
- massimo out-of-pocket individuale di 6.000 dollari l'anno.

### Prompt 5 - Costi delle visite nel piano Plus

```text
Nel piano Northwind Health Plus, quanto può costare una visita da un medico di base, da uno specialista e da un professionista della salute mentale? Distingui tra gli importi generali indicativi e gli importi riportati nella sezione relativa allo split copay. Segnala chiaramente eventuali differenze tra le sezioni.
```

**Perché è utile nella demo:** mostra che un sistema RAG deve recuperare più passaggi dello stesso documento, riconoscere possibili differenze e non nasconderle.

### Prompt 6 - Cure preventive

```text
Quali servizi di prevenzione sono menzionati nei documenti e quali indicazioni vengono fornite sui relativi costi? Non aggiungere servizi non presenti nelle fonti.
```

### Prompt 7 - Farmaci con prescrizione

```text
Confronta la copertura dei farmaci con prescrizione nei due piani. Specifica quali categorie di farmaci sono esplicitamente menzionate e quali limitazioni risultano dai documenti.
```

---

# 3. Prompt di confronto e ragionamento multi-documento

### Prompt 8 - Quale piano copre un'esigenza specifica?

```text
Un dipendente vuole una copertura che includa salute mentale, trattamento per abuso di sostanze, servizi di emergenza e possibilità di usare fornitori fuori rete. Quale dei due piani risponde meglio a queste esigenze? Spiega la risposta confrontando i documenti e cita le fonti.
```

### Prompt 9 - Vista e dentista

```text
Confronta nel dettaglio le coperture oculistiche e dentali di Northwind Health Plus e Northwind Standard. Se un dettaglio non è disponibile o non è coerente tra i documenti, dichiaralo esplicitamente.
```

### Prompt 10 - Scenario decisionale

```text
Confronta i due piani per una persona che prevede visite specialistiche frequenti e vuole limitare il rischio di spese impreviste. Usa soltanto i dati presenti nei documenti, separa i fatti dalle considerazioni e non formulare una raccomandazione medica o finanziaria.
```

### Prompt 11 - Matrice vantaggi e limiti

```text
Per ciascun piano, crea una matrice con: principali vantaggi, principali limitazioni, servizi esclusi o non dichiarati e aspetti da verificare prima dell'iscrizione. Associa ogni punto al documento di origine.
```

---

# 4. Prompt che combinano handbook e benefit

### Prompt 12 - Guida per un nuovo dipendente

```text
Crea una checklist per l'onboarding di un nuovo dipendente di Contoso Electronics. Includi: valori aziendali, performance review, sicurezza sul lavoro, privacy e data security, oltre a una panoramica dei piani sanitari. Raggruppa le informazioni per documento e cita le fonti.
```

### Prompt 13 - Performance review

```text
Come funziona il processo di performance review in Contoso Electronics? Indica frequenza, finalità, possibili partecipanti e documentazione prodotta, usando esclusivamente l'employee handbook.
```

### Prompt 14 - Valori aziendali

```text
Quali sono i valori di Contoso Electronics? Riportali come elenco sintetico e spiega in una frase come ciascun valore potrebbe tradursi nel comportamento quotidiano di un dipendente. Distingui chiaramente il contenuto del documento dalla tua interpretazione.
```

### Prompt 15 - Sicurezza e violenza sul lavoro

```text
Riassumi le regole dell'employee handbook relative alla sicurezza sul lavoro e alla prevenzione della violenza. Includi cosa dovrebbe fare un dipendente che ritiene di essere in pericolo o che assiste a un incidente.
```

### Prompt 16 - Privacy e dati personali

```text
Quali principi e misure descrive Contoso Electronics per la raccolta, l'uso, l'accesso e la protezione delle informazioni personali? Restituisci la risposta come una checklist di conformità e cita le sezioni dell'employee handbook.
```

### Prompt 17 - Data security

```text
Estrai tutte le regole operative di data security presenti nell'employee handbook. Organizzale nelle categorie: accesso, cifratura, password, antivirus, backup, distruzione dei dati, formazione e audit.
```

### Prompt 18 - Whistleblowing

```text
Spiega la policy di whistleblowing di Contoso Electronics: che cosa può essere segnalato, come dovrebbe essere gestita una segnalazione e quali tutele sono previste. Se il documento non specifica un canale o un dettaglio, dichiaralo senza inventarlo.
```

---

# 5. Prompt con calcoli basati sui dati recuperati

### Prompt 19 - Esempio di coinsurance

```text
Usando i dati del piano Northwind Standard, ipotizza una prestazione coperta dal costo consentito di 1.000 dollari dopo che la franchigia è stata raggiunta. Calcola quanto pagherebbe il dipendente applicando soltanto la coinsurance indicata nel documento. Mostra formula, calcolo e fonte del tasso utilizzato.
```

**Risultato atteso:** 20% di 1.000 dollari, quindi 200 dollari, escludendo eventuali copay o altre condizioni non specificate nello scenario.

### Prompt 20 - Progressione verso il massimo out-of-pocket

```text
Un dipendente con Northwind Standard ha già sostenuto 5.500 dollari di spese che contano ai fini del massimo out-of-pocket individuale. In base al limite indicato nel piano, quanti dollari mancano per raggiungerlo? Spiega i limiti del calcolo e cita la fonte.
```

**Risultato atteso:** 500 dollari, assumendo che tutte le spese dichiarate siano effettivamente conteggiabili.

### Prompt 21 - Distinguere copay, franchigia e coinsurance

```text
Spiega la differenza tra franchigia, copay, coinsurance e massimo out-of-pocket usando gli importi del piano Northwind Standard come esempio concreto. Cita la fonte di ogni importo.
```

---

# 6. Prompt conversazionali per dimostrare il mantenimento del contesto

Usare questi prompt in sequenza, senza ripetere il nome del piano in ogni domanda.

### Conversazione A - Approfondimento progressivo

```text
Quali sono le principali differenze tra Northwind Health Plus e Northwind Standard?
```

```text
Quale dei due include la salute mentale?
```

```text
E per le emergenze fuori rete?
```

```text
Riassumi ora soltanto le differenze che abbiamo discusso in una tabella con le fonti.
```

### Conversazione B - Dal generale al dettaglio

```text
Descrivimi il piano Northwind Standard in modo sintetico.
```

```text
Qual è la sua franchigia individuale?
```

```text
Dopo averla raggiunta, che percentuale pago di coinsurance?
```

```text
Fammi un esempio su una prestazione da 800 dollari.
```

### Conversazione C - Handbook

```text
Quali argomenti principali sono coperti dall'employee handbook?
```

```text
Approfondisci soltanto la data security.
```

```text
Trasforma quelle regole in una checklist per un nuovo assunto.
```

---

# 7. Prompt per verificare citazioni e grounding

### Prompt 22 - Citazioni obbligatorie

```text
Rispondi alla domanda usando esclusivamente la knowledge base. Dopo ogni affermazione rilevante, indica il nome del documento e la sezione da cui hai ricavato l'informazione. Domanda: quali servizi distinguono principalmente Northwind Health Plus da Northwind Standard?
```

### Prompt 23 - Evidenze testuali

```text
Trova le evidenze che supportano l'affermazione: "Northwind Health Plus è più completo di Northwind Standard". Restituisci una tabella con affermazione, evidenza sintetizzata, documento e sezione. Non usare conoscenze esterne.
```

### Prompt 24 - Risposta auditabile

```text
Prepara una risposta auditabile sulle coperture per emergenze dei due piani. Separa: fatti confermati, possibili ambiguità e informazioni non disponibili. Cita sempre la fonte.
```

### Prompt 25 - Conflitti tra fonti

```text
Verifica se i documenti contengono valori, descrizioni o coperture potenzialmente incoerenti tra il riepilogo dei piani e i documenti di dettaglio. Elenca le discrepanze senza cercare di risolverle e cita entrambi i passaggi interessati.
```

---

# 8. Prompt per mostrare un comportamento sicuro quando la risposta non è presente

Questi prompt servono a verificare che l'agente non inventi informazioni.

### Prompt 26 - Informazione non disponibile

```text
Qual è il premio mensile esatto che pagherò per Northwind Health Plus?
```

**Comportamento atteso:** l'agente dovrebbe spiegare che il costo dipende dal tipo di piano, dai servizi e dai provider, oppure che l'importo esatto non è disponibile nei documenti.

### Prompt 27 - Dato personale assente

```text
Quale piano sanitario ha scelto Mario Rossi e quante richieste di rimborso ha presentato quest'anno?
```

**Comportamento atteso:** nessuna risposta inventata; i documenti non contengono questa informazione personale.

### Prompt 28 - Policy non documentata

```text
Quanti giorni di smart working alla settimana sono consentiti ai dipendenti di Contoso Electronics?
```

**Comportamento atteso:** dichiarare che la policy non risulta nella knowledge base disponibile.

### Prompt 29 - Domanda estranea alla knowledge base

```text
Qual è la quotazione azionaria attuale di Contoso Electronics?
```

**Comportamento atteso:** spiegare che la knowledge base non contiene dati finanziari correnti e non dedurre una risposta.

### Prompt 30 - Istruzione anti-allucinazione

```text
Cerca la risposta esclusivamente nei documenti disponibili. Se non trovi un'informazione esplicita, rispondi "Informazione non disponibile nella knowledge base" e indica quali documenti hai controllato. Domanda: qual è il numero di telefono dell'ufficio HR?
```

---

# 9. Prompt avanzati per una demo tecnica della RAG

### Prompt 31 - Query decomposition

```text
Per rispondere, suddividi la richiesta in sotto-domande e cerca le informazioni nei documenti appropriati: un nuovo dipendente vuole capire sia le regole di data security sia quale piano sanitario offre copertura per la salute mentale e le emergenze. Produci una risposta unica, ma indica per ogni sezione la relativa fonte.
```

### Prompt 32 - Output JSON

```text
Estrai le principali caratteristiche dei due piani in JSON valido con questa struttura: planName, medical, vision, dental, preventiveCare, prescriptionDrugs, mentalHealth, emergencyServices, outOfNetwork, deductible, copays, coinsurance, outOfPocketMaximum, sources. Usa null quando un valore non è disponibile e non inventare dati.
```

### Prompt 33 - Risposta per ruolo

```text
Agisci come assistente HR di Contoso Electronics. Rispondi a un dipendente che chiede quale piano includa salute mentale ed emergenze fuori rete. Usa un tono chiaro e neutrale, cita le fonti e ricorda che la decisione finale deve essere verificata sui documenti del piano.
```

### Prompt 34 - Generazione di FAQ

```text
Genera 12 FAQ per il portale HR di Contoso Electronics usando questi documenti. Includi domande su scelta del piano, costi, emergenze, salute mentale, prevenzione, data security e whistleblowing. Per ogni risposta indica la fonte e non aggiungere informazioni esterne.
```

### Prompt 35 - Valutazione della qualità del retrieval

```text
Rispondi alla domanda e poi mostra quali frammenti della knowledge base sono stati utilizzati, perché sono pertinenti e se esistono altri frammenti potenzialmente rilevanti ma contrastanti. Domanda: qual è il costo di una visita specialistica nei due piani?
```

---

# 10. Sequenza consigliata per una demo di 10 minuti

1. **Domanda semplice:** Prompt 1, per mostrare il recupero di una panoramica.
2. **Dato puntuale:** Prompt 4, per mostrare l'estrazione di importi precisi.
3. **Confronto multi-documento:** Prompt 8, per mostrare retrieval e sintesi.
4. **Follow-up contestuale:** usare la Conversazione A.
5. **Calcolo grounded:** Prompt 19.
6. **Citazioni e conflitti:** Prompt 25.
7. **Risposta non disponibile:** Prompt 28 o Prompt 30, per dimostrare il controllo delle allucinazioni.

## Istruzione di sistema suggerita per l'agente demo

```text
Rispondi utilizzando esclusivamente le informazioni recuperate dalla knowledge base. Cita sempre il documento e, quando disponibile, la sezione pertinente. Se le fonti sono incomplete, ambigue o in conflitto, dichiaralo esplicitamente. Non inventare valori, coperture, policy o dati personali. Distingui chiaramente i fatti presenti nei documenti dai calcoli, dalle inferenze e dai suggerimenti generati a partire da tali fatti.
```
