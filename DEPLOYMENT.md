# Schedule Optimizer - Deployment Guide for Render

This guide will help you deploy the Schedule Optimizer web service to Render.com.

## What You'll Get

A web application where you can:
- Upload your StaffScheduler.xlsx file
- Run the optimization in the cloud
- Download the optimized results with assignments and sanity checks

## Prerequisites

1. A GitHub account (to connect to Render)
2. A Render account (free tier works fine) - sign up at https://render.com
3. This repository pushed to GitHub

## Deployment Steps

### Option 1: Deploy via Render Dashboard (Easiest)

1. **Push this repository to GitHub** (if you haven't already)
   ```bash
   git add .
   git commit -m "Add schedule optimizer web service"
   git push origin main
   ```

2. **Log in to Render** at https://dashboard.render.com

3. **Create a New Web Service**
   - Click "New +" button in the top right
   - Select "Web Service"
   - Connect your GitHub account if you haven't already
   - Select this repository

4. **Configure the Service**
   - **Name**: schedule-optimizer (or any name you prefer)
   - **Region**: Choose closest to you
   - **Branch**: main (or your default branch)
   - **Runtime**: Docker
   - **Instance Type**: Free (sufficient for weekly use)

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically detect the Dockerfile and deploy
   - Wait 5-10 minutes for the initial build

6. **Access Your Service**
   - Once deployed, Render will provide a URL like: `https://schedule-optimizer-xxxx.onrender.com`
   - Visit this URL to access your optimizer

### Option 2: Deploy via Blueprint (Automated)

1. Push code to GitHub (see step 1 above)

2. In Render Dashboard:
   - Click "New +" → "Blueprint"
   - Connect your repository
   - Render will automatically use the `render.yaml` file
   - Click "Apply"

## Using the Web Service

1. **Open the URL** provided by Render in your browser

2. **Upload your Excel file**
   - Click "Choose File" and select your `StaffScheduler.xlsx`
   - Click "Optimize Schedule"

3. **Wait for processing**
   - The optimization runs for up to 60 seconds
   - Progress indicator will show

4. **Download result**
   - The optimized file will automatically download as `StaffScheduler_Optimized.xlsx`
   - Check the new "Sanity" sheet for validation

## Important Notes

### Free Tier Limitations
- **Spin down**: Free tier services sleep after 15 minutes of inactivity
- **Spin up**: First request after sleep takes ~30 seconds to wake up
- **Build time**: Initial deployment takes 5-10 minutes
- Perfect for weekly use!

### File Size
- Maximum file size: 16MB (configurable in app.py)
- Typical schedule files are well under this limit

### Processing Time
- Optimization runs for up to 60 seconds
- Configurable in app.py (max_time parameter)

## Troubleshooting

### Service won't start
- Check the Render logs in the dashboard
- Ensure all files are committed and pushed to GitHub
- Verify Dockerfile and requirements.txt are present

### Optimization fails
- Check that your Excel file has the correct format:
  - Day sheets: Mon, Tue, Wed, Thu, Fri, Sat, Sun
  - Weekly sheet with parameters
  - Correct cell ranges for COST, PREF, HOURS
- View detailed error in browser or Render logs

### Slow first request
- Free tier services sleep after inactivity
- First request wakes the service (~30 seconds)
- Subsequent requests are fast

## Monitoring

Access logs and metrics in Render Dashboard:
- **Logs**: Real-time application logs
- **Metrics**: CPU, memory, request stats
- **Events**: Deployment history

## Costs

**Free Tier** (Recommended for weekly use):
- 750 hours/month free
- Perfect for occasional use
- Service sleeps when idle

**Paid Tiers** (If you need always-on):
- Starter: $7/month - no sleep, faster
- Standard: $25/month - more resources

For weekly use, **FREE TIER IS PERFECT**!

## Updating the Service

When you make changes to the code:

```bash
git add .
git commit -m "Update optimizer"
git push origin main
```

Render will automatically detect the push and redeploy (takes ~5 minutes).

## Environment Variables (Advanced)

You can configure these in Render Dashboard under "Environment":

- `PORT`: Default 8080 (set automatically by Render)
- Add custom variables as needed

## Security Notes

- Files are processed in temporary directories and deleted after
- No data is stored on the server
- Each request is isolated
- Use HTTPS (provided by Render automatically)

## Support

- Render documentation: https://render.com/docs
- GitHub issues: [Your repository issues page]

## Next Steps

1. Deploy to Render using steps above
2. Bookmark your service URL
3. Use it weekly to optimize schedules!
4. (Optional) Set up a custom domain in Render settings

Happy optimizing! 📅✨
