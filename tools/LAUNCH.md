# Launching thewonderagency.co

1. In GitHub: repo Settings → Pages → Source: deploy from branch `main`, folder `/ (root)`.
2. At your domain provider, set DNS for thewonderagency.co:
   - A records for `@`: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
   - CNAME for `www`: thewondergroup.github.io
   - Remove the old Webflow records.
3. Run `tools/go-live.sh`, commit and push. It moves the site from /v3/ to the root, removes the
   preview's noindex tags, restores the real robots.txt and adds the CNAME file.
4. Back in Settings → Pages: custom domain thewonderagency.co, then tick "Enforce HTTPS"
   once GitHub has issued the certificate.
5. Unpublish the Webflow site.
6. Add the site to Google Search Console and Bing Webmaster Tools and submit
   https://thewonderagency.co/sitemap.xml.

Analytics: paste a snippet (e.g. Plausible or Cloudflare Web Analytics) into tools/build/analytics.html
and rebuild; it is added to every page.
