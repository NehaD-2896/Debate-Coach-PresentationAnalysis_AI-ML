# Presentation Analysis UI

Reference-style learner experience for the Presentation Analysis Engine.

- Upload PPTX/PDF
- Start microphone recording in the browser
- Live timer
- Stop & analyze
- Duration is calculated automatically
- Backend receives the presentation + audio + computed duration
- Results show delivery, speech, content, per-slide feedback and transcript

Run from this folder:

```powershell
npm install
npm run dev
```

The browser UI uses `VITE_API_BASE_URL` or defaults to `http://127.0.0.1:8010`.
