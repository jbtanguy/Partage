
# conversion pdf en image

from pdf2image import convert_from_path
pages = convert_from_path('net1.pdf', dpi=300)
for idx, page in enumerate(pages):
      page.save('mazarinade'+str(idx)+'.jpg', 'JPEG')




