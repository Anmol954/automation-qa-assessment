"""
embed_screenshots_in_pdf.py
----------------------------
Appends a "Section 5: Evidence Screenshots" section to the existing PDF.
Uses PyMuPDF (fitz); colors as (r,g,b) float tuples.

Run:  python embed_screenshots_in_pdf.py
"""

import os
import fitz  # PyMuPDF

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH   = os.path.join(SCRIPT_DIR, "Task1_QA_Report.pdf")

# Screenshot manifest
SCREENSHOTS = [
    ("realworld_home.png",
    "realworld_home.png - Conduit home page"),
    ("realworld_logged_in.png",
    "realworld_logged_in.png - Logged-in state with username shown"),
    ("realworld_article_created.png",
    "realworld_article_created.png - Article page with Edit/Delete controls visible"),
    ("realworld_failed_update_no_error.png",
    "realworld_failed_update_no_error.png - Failed article update with silent 422"),
    ("realworld_login_error.png",
    "realworld_login_error.png - Login error message with poor UX styling"),
    ("realworld_profile.png",
    "realworld_profile.png - User profile page"),
    ("realworld_weak_password.png",
    "realworld_weak_password.png - Weak password accepted during sign-up"),
    ("realworld_invalid_email.png",
    "realworld_invalid_email.png - Invalid email accepted during sign-up"),
    ("realworld_dup_user_first.png",
    "realworld_dup_user_first.png - First duplicate-username registration succeeded"),
    ("realworld_dup_user_second.png",
    "realworld_dup_user_second.png - Second duplicate-username registration also succeeded"),
    ("realworld_404_original.png",
    "realworld_404_original.png - demo.realworld.io returns 404 / NoSuchBucket"),
    ("realworld_comment_programmatic.png",
    "realworld_comment_programmatic.png - Comment text entered programmatically"),
    ("realworld_comment_no_post.png",
    "realworld_comment_no_post.png - Post Comment click did not submit the comment"),
]

# Colors (r, g, b) floats 0-1
ACCENT   = (72/255,  37/255, 177/255)   # #4825b1
MUTED    = (122/255,118/255,110/255)    # #7a766e
BG_PAGE  = (244/255,243/255,241/255)    # #f4f3f1
WHITE    = (1.0, 1.0, 1.0)

PAGE_W, PAGE_H = 595, 842   # A4 points
MX, MY         = 40, 50     # margins
CW             = PAGE_W - 2*MX
IMG_MAX_W      = CW - 4
IMG_MAX_H      = 320        # max height per image block


def new_page(doc):
    p = doc.new_page(width=PAGE_W, height=PAGE_H)
    p.draw_rect(fitz.Rect(0, 0, PAGE_W, PAGE_H), color=None, fill=BG_PAGE)
    return p


def draw_header(page, y):
    """Accent banner + subtitle."""
    page.draw_rect(fitz.Rect(MX, y, PAGE_W - MX, y + 30),
                   color=None, fill=ACCENT)
    page.insert_text((MX + 8, y + 21),
                     "5.  Evidence Screenshots",
                     fontsize=14, color=WHITE, fontname="helv")
    page.insert_text(
        (MX, y + 46),
        "Visual evidence captured by automated Playwright tests "
        "(demo.realworld.show).",
        fontsize=8.5, color=MUTED, fontname="helv"
    )
    return y + 62


def embed_screenshots(doc):
    page = new_page(doc)
    cy   = MY
    cy   = draw_header(page, cy)
    n    = 0

    for fname, caption in SCREENSHOTS:
        fpath = os.path.join(SCRIPT_DIR, fname)
        if not os.path.exists(fpath):
            print(f"  [SKIP] {fname} - not found")
            continue

        n += 1

        # Get image dimensions via Pixmap
        try:
            pm   = fitz.Pixmap(fpath)
            sw   = pm.width
            sh   = pm.height
            pm   = None
        except Exception as e:
            print(f"  [WARN] {fname}: {e}")
            sw, sh = 800, 450

        scale = min(IMG_MAX_W / sw, IMG_MAX_H / sh, 1.0)
        iw    = sw * scale
        ih    = sh * scale

        CAPTION_H = 30
        block_h   = ih + CAPTION_H + 18

        # New page if needed
        if cy + block_h > PAGE_H - MY:
            page = new_page(doc)
            cy   = MY

        # Thin border rect
        border = fitz.Rect(MX, cy, MX + iw + 4, cy + ih + 4)
        page.draw_rect(border, color=MUTED, fill=WHITE, width=0.5)

        # Embed image
        img_rect = fitz.Rect(MX + 2, cy + 2, MX + 2 + iw, cy + 2 + ih)
        page.insert_image(img_rect, filename=fpath)

        # Caption
        page.insert_text(
            (MX, cy + ih + 10),
            f"Fig. {n}: {caption}",
            fontsize=7.5, color=MUTED, fontname="helv"
        )

        cy += block_h
        print(f"  [IMG {n:02d}] {fname}")

    print(f"\n  Embedded {n} screenshot(s).")


# Main
print(f"Opening: {PDF_PATH}")
doc = fitz.open(PDF_PATH)
print(f"  Pages before: {doc.page_count}")

embed_screenshots(doc)

import tempfile, shutil
tmp = PDF_PATH + ".tmp"
doc.save(tmp, garbage=4, deflate=True)
pages_after = doc.page_count
doc.close()
shutil.move(tmp, PDF_PATH)
print(f"  Pages after:  {pages_after}")
print(f"\nSaved: {PDF_PATH}")
print("Done.")
