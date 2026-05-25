import easyocr
import os
import numpy as np
from pathlib import Path
from PIL import Image

# 이미지 폴더
folder = Path(r"C:\project\롯데관광연수")
output_file = folder / "extracted_text.md"

# 이미지 파일 목록 (번호 순 정렬)
images = sorted(
    folder.glob("ai게임 개발 - *.jpg"),
    key=lambda p: int(p.stem.split(" - ")[1])
)

print(f"총 {len(images)}장 처리 시작...")

# EasyOCR 리더 초기화 (한국어 + 영어)
reader = easyocr.Reader(['ko', 'en'], gpu=False, verbose=False)

results = []
for i, img_path in enumerate(images, 1):
    page_num = img_path.stem.split(" - ")[1]
    print(f"[{i}/{len(images)}] {img_path.name} 처리 중...")

    try:
        img_array = np.array(Image.open(img_path).convert('RGB'))
        texts = reader.readtext(img_array, detail=0, paragraph=True)
        content = "\n".join(texts)
        results.append(f"## 페이지 {page_num}\n\n{content}\n")
    except Exception as e:
        results.append(f"## 페이지 {page_num}\n\n[오류: {e}]\n")

# 결과 저장
with open(output_file, "w", encoding="utf-8") as f:
    f.write("# AI 실무 프롬프트 — OCR 추출본\n\n")
    f.write("\n---\n\n".join(results))

print(f"\n완료! → {output_file}")
