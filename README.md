# sky-blog-images

Featured images for skydesigners.lk blog articles. Public so the CMS and WhatsApp can load them.

- `images/<yyyy>/<mm>/<slug>-v<n>.png`: published images. Never overwrite or delete one; a revision is a new `-v<n>`.
- `render/<yyyy>-<mm>-<slug>-v<n>.json`: a spec dropped here (by n8n, from the Drive folder "Images to host") is rendered by the
  "Render featured images" GitHub Action with `tools/build_post.py` (the approved Sky design with five layouts: panel, stat, grid, split, center; 1200x675 @2x) into `images/`, then removed.
  A spec whose image already exists becomes `.exists`; a broken spec becomes `.error`.
