# Deployment Checklist - Phase 1

## Pre-Deployment (Local Testing)

### 1. Environment Setup
- [ ] Python 3.9+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with valid `GROQ_API_KEY`
- [ ] No syntax errors (`python -m py_compile *.py`)

### 2. Run Tests
```bash
python test_agent.py
```
- [ ] Basic search test passes
- [ ] PDF processing test passes
- [ ] Caching test passes
- [ ] Research gaps test passes
- [ ] Error handling test passes

### 3. Manual Testing
```bash
streamlit run app.py
```
- [ ] App loads without errors
- [ ] Can search for papers
- [ ] Summaries generate correctly
- [ ] PDF processing works
- [ ] Research gaps display properly
- [ ] Cache management works
- [ ] No console errors

### 4. Code Quality
- [ ] No hardcoded API keys in code
- [ ] All sensitive data in `.env`
- [ ] `.gitignore` includes `.env` and `.cache/`
- [ ] Error messages are user-friendly
- [ ] Logging works properly
- [ ] Code is commented

---

## Deployment to Render

### 1. Prepare Repository
```bash
# Make sure all files are committed
git add .
git commit -m "Phase 1: Production-ready research agent"
git push origin main
```

Files to include:
- [ ] All `.py` files
- [ ] `requirements.txt`
- [ ] `.env.template` (NOT `.env`)
- [ ] `render.yaml`
- [ ] `README.md`
- [ ] `.gitignore`

### 2. Render Configuration

#### Create New Web Service
1. [ ] Go to https://dashboard.render.com
2. [ ] Click "New +" → "Web Service"
3. [ ] Connect GitHub repository
4. [ ] Configure settings:

**Basic Settings:**
- [ ] Name: `ai-research-agent` (or your choice)
- [ ] Region: Choose closest to your users
- [ ] Branch: `main`
- [ ] Runtime: `Python 3`

**Build Settings:**
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`

**Environment Variables:**
- [ ] Add `GROQ_API_KEY` with your actual key
- [ ] (Optional) Add `SEMANTIC_SCHOLAR_API_KEY`

**Plan:**
- [ ] Select plan (Free tier works fine for testing)

### 3. Deploy
- [ ] Click "Create Web Service"
- [ ] Wait for build to complete (5-10 minutes)
- [ ] Check logs for errors

### 4. Post-Deployment Testing

**Basic Functionality:**
- [ ] Visit your Render URL
- [ ] App loads successfully
- [ ] Can perform a search
- [ ] Results display correctly
- [ ] PDF processing works
- [ ] No 500 errors

**Performance:**
- [ ] First search completes in <90 seconds
- [ ] Cached search completes in <5 seconds
- [ ] Page doesn't timeout
- [ ] Memory usage stable

**Error Handling:**
- [ ] Invalid query shows friendly error
- [ ] Broken PDF doesn't crash app
- [ ] Network errors handled gracefully

---

## Post-Deployment

### 1. Monitoring
- [ ] Set up health check in Render dashboard
- [ ] Monitor logs for errors
- [ ] Check memory/CPU usage
- [ ] Set up email alerts (optional)

### 2. Documentation
- [ ] Update README with live URL
- [ ] Document any deployment-specific config
- [ ] Add usage instructions
- [ ] Create demo video (optional)

### 3. User Testing
- [ ] Test with 5-10 different queries
- [ ] Try edge cases (very long queries, special characters)
- [ ] Test on different devices (mobile, tablet, desktop)
- [ ] Test on different browsers

### 4. Performance Optimization
- [ ] Check cache hit rate (should be >80%)
- [ ] Monitor average response time
- [ ] Identify slow queries
- [ ] Consider upgrading plan if needed

---

## Troubleshooting

### Build Fails
**Error:** `requirements.txt not found`
- Check file is in root directory
- Verify Git pushed correctly

**Error:** `No module named 'groq'`
- Verify `requirements.txt` includes all dependencies
- Check Python version compatibility

### Runtime Errors
**Error:** `Groq API key not found`
- Double-check environment variable in Render
- Variable name must be EXACTLY `GROQ_API_KEY`

**Error:** `Port already in use`
- Render automatically sets `$PORT`
- Make sure start command uses `--server.port $PORT`

**Error:** `Memory limit exceeded`
- Reduce `DEFAULT_PAPER_LIMIT` in config
- Upgrade to paid plan
- Disable PDF processing by default

### Performance Issues
**Slow searches:**
- Check Groq API rate limits
- Verify caching is working
- Reduce `max_tokens` in config

**Timeouts:**
- Increase timeout in Render dashboard
- Process fewer papers by default
- Disable PDF processing for large searches

---

## Rollback Plan

If deployment fails:

1. **Immediate:** 
   - Mark service as "Suspended" in Render
   - Display maintenance message

2. **Investigate:**
   - Check Render logs
   - Review error messages
   - Test locally

3. **Fix:**
   - Make fixes locally
   - Test thoroughly
   - Commit and push
   - Render auto-deploys

4. **Emergency:**
   - Revert to previous commit
   - Force redeploy in Render dashboard

---

## Security Checklist

- [ ] No API keys in code
- [ ] `.env` in `.gitignore`
- [ ] HTTPS enabled (automatic on Render)
- [ ] Rate limiting configured (Groq handles this)
- [ ] Error messages don't expose sensitive info
- [ ] Dependencies up to date
- [ ] Input validation for all user inputs

---

## Success Criteria

**Phase 1 is successful if:**

1. **Stability:**
   - No crashes in 48 hours of testing
   - Errors handled gracefully
   - Logs show no critical errors

2. **Performance:**
   - Searches complete in <90 seconds
   - Cache working (>80% hit rate)
   - Memory usage stable

3. **Functionality:**
   - All core features work
   - PDF processing successful (when available)
   - LLM summaries accurate
   - Research gaps identified

4. **User Experience:**
   - UI responsive
   - Error messages clear
   - Results well-formatted
   - Mobile-friendly

---

## Next Steps (Phase 2)

After successful deployment:
- [ ] Gather user feedback
- [ ] Monitor usage patterns
- [ ] Plan Phase 2 features
- [ ] Consider monetization strategy

---


