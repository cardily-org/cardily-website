# URL Rewrite Configuration - Clean URLs Without .html Extensions

## What Was Changed

All internal links in your HTML files have been updated to remove `.html` extensions, and server configuration files have been added to handle URL rewriting on the server side.

## Changes Made

### 1. Server Configuration Files Created

#### `.htaccess` (Apache Servers)
- Enables URL rewriting to serve `.html` files without the extension in the URL
- Redirects any requests with `.html` to the extensionless version (301 redirect)
- Compatible with most shared hosting providers and Apache web servers

#### `web.config` (IIS/Windows Servers)
- Provides the same functionality for Windows-based IIS servers
- Automatically redirects `.html` URLs to clean URLs
- Compatible with Azure App Service and Windows hosting

### 2. Updated All HTML Files

All internal links have been updated from:
- `index.html` → `/`
- `projects.html` → `/projects`
- `research.html` → `/research`
- `newsletters.html` → `/newsletters`
- `get-involved.html` → `/get-involved`
- `careers.html` → `/careers`
- `newsletter-december-2025.html` → `/newsletter-december-2025`

### Files Updated:
- index.html
- research.html
- projects.html
- newsletters.html
- get-involved.html
- careers.html
- newsletter-december-2025.html

## How It Works

1. **User visits**: `https://yoursite.com/research`
2. **Server rewrites internally to**: `research.html`
3. **Browser shows**: `https://yoursite.com/research` (clean URL)

If someone tries to access `https://yoursite.com/research.html`, they will be automatically redirected to `https://yoursite.com/research`.

## Benefits

✅ **Cleaner URLs**: No `.html` extensions visible to users  
✅ **Better SEO**: Search engines prefer clean URLs  
✅ **Professional appearance**: URLs look more modern and polished  
✅ **Security through obscurity**: Technology stack less obvious  
✅ **Future-proof**: Easy to change backend technology without breaking URLs

## Deployment Instructions

### For Apache Servers (Most Common)
1. Upload the `.htaccess` file to your website's root directory
2. Ensure `mod_rewrite` is enabled on your server
3. Upload all updated HTML files
4. Test the URLs without `.html` extensions

### For IIS/Windows Servers
1. Upload the `web.config` file to your website's root directory
2. Ensure URL Rewrite module is installed on IIS
3. Upload all updated HTML files
4. Test the URLs without `.html` extensions

### For Static Hosting (GitHub Pages, Netlify, Vercel)
- **GitHub Pages**: Automatically handles extensionless URLs if files are named correctly
- **Netlify**: Create a `_redirects` file with: `/* /index.html 200`
- **Vercel**: Configuration is automatic for static sites

## Testing

After deployment, test these URLs:
- ✅ `https://yoursite.com/` (should show index.html)
- ✅ `https://yoursite.com/research` (should show research.html)
- ✅ `https://yoursite.com/projects` (should show projects.html)
- ✅ `https://yoursite.com/research.html` (should redirect to /research)

## Troubleshooting

### If Clean URLs Don't Work:

1. **Apache**: Check if `mod_rewrite` is enabled
   ```bash
   sudo a2enmod rewrite
   sudo service apache2 restart
   ```

2. **IIS**: Install URL Rewrite Module
   - Download from: https://www.iis.net/downloads/microsoft/url-rewrite

3. **Shared Hosting**: Contact your hosting provider to ensure:
   - mod_rewrite is enabled (Apache)
   - AllowOverride is set to All
   - URL Rewrite module is installed (IIS)

### If You Get 404 Errors:
- Ensure all HTML files are uploaded
- Check that `.htaccess` or `web.config` is in the root directory
- Verify file permissions (644 for .htaccess, 755 for directories)

## Important Notes

- **Case Sensitivity**: URLs are now case-sensitive on Linux servers
- **Anchors**: Hash links like `/#about` work exactly as before
- **External Links**: Only update links within your control
- **Backwards Compatibility**: Old `.html` URLs automatically redirect to new clean URLs

## Reverting Changes

If you need to revert:
1. Remove `.htaccess` or `web.config` file
2. Use find/replace to add `.html` back to all internal links
3. Replace `/` with `index.html` for homepage links

---

**Created**: December 14, 2025  
**Purpose**: Remove .html extensions from URLs for improved UX and security
