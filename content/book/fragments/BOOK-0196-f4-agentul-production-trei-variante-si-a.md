#### F4. Agentul Production: trei variante si aprobare

Production poate folosi **acelasi model** ca Research, dar primeste alte instructiuni, contexte si instrumente. El propune variantele A (scurt si dinamic), B (explicativ cu diagrame) si C (demonstratie practica). Video-ul efectiv necesita un motor de randare, continut vizual autorizat si integrare tehnica.

```text
DACA handoff_invalid: OPRESTE
PENTRU stil IN [A, B, C]:
    genereaza_scenariu_original()
    genereaza_storyboard()
    verifica_durata_si_afirmatiile_factuale()
    DACA exista_renderer_autorizat: genereaza_preview()
    ALTFEL: livreaza_documente_de_productie()
STATUS = WAITING_HUMAN_APPROVAL
```

Utilizatorul poate aproba, combina sau respinge variante. Aprobarea trebuie asociata **hash-ului artefactului concret**; orice modificare ulterioara necesita o noua aprobare. Incarcarea unui clip pe canal necesita OAuth si drepturi efective de publicare, iar schimbarea vizibilitatii din privat in public poate cere o aprobare distincta. In configuratia didactica publicarea este dezactivata.

```yaml
name: editorial_research_demo
research:
  source_mode: fixture
  max_videos: 12
  allowed_content: metadata_only
  allow_third_party_caption_download: false
production:
  variant_names: [scurt_dinamic, explicativ, demonstratie]
  video_renderer: not_configured
  publisher: disabled
  approval_required: true
  publish_default_privacy: private
```

`fixture` inseamna date de test cunoscute. YouTube Data API permite citirea anumitor metadate publice, dar `captions.download` necesita drept de editare a videoclipului, deci nu ofera transcrierile oricarui creator: [PlaylistItems.list](https://developers.google.com/youtube/v3/docs/playlistItems/list), [Captions.download](https://developers.google.com/youtube/v3/docs/captions/download), [Videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert).

**Evaluare:** urmarim identificarea clipurilor noi, duplicatele, provenienta surselor, afirmatiile neverificate, originalitatea scenariilor, versiunile aprobate si absenta oricarei publicari neautorizate. Un sistem care produce trei scenarii JSON nu a generat trei videoclipuri MP4.

