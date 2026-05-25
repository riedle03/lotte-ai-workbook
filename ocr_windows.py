import asyncio
import sys
from pathlib import Path

import winsdk.windows.globalization as win_glob
import winsdk.windows.graphics.imaging as win_imaging
import winsdk.windows.media.ocr as win_ocr
import winsdk.windows.storage as win_storage

folder = Path(r"C:\project\롯데관광연수")
output_file = folder / "extracted_text.md"

images = sorted(
    folder.glob("ai게임 개발 - *.jpg"),
    key=lambda p: int(p.stem.split(" - ")[1])
)

print(f"총 {len(images)}장 처리 시작...", flush=True)

# 한국어 OCR 엔진 준비
language = win_glob.Language("ko-KR")
engine = win_ocr.OcrEngine.try_create_from_language(language)

if engine is None:
    print("한국어 OCR 엔진을 찾을 수 없습니다. 영어로 시도합니다.")
    engine = win_ocr.OcrEngine.try_create_from_user_profile_languages()

async def ocr_image(img_path):
    file = await win_storage.StorageFile.get_file_from_path_async(str(img_path))
    stream = await file.open_async(win_storage.FileAccessMode.READ)
    decoder = await win_imaging.BitmapDecoder.create_async(stream)
    bitmap = await decoder.get_software_bitmap_async()
    result = await engine.recognize_async(bitmap)
    return result.text

async def main():
    results = []
    for i, img_path in enumerate(images, 1):
        page_num = img_path.stem.split(" - ")[1]
        print(f"[{i}/{len(images)}] 페이지 {page_num} 처리 중...", flush=True)
        try:
            text = await ocr_image(img_path)
            results.append(f"## 페이지 {page_num}\n\n{text}\n")
        except Exception as e:
            print(f"  오류: {e}", flush=True)
            results.append(f"## 페이지 {page_num}\n\n[오류: {e}]\n")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# AI 실무 프롬프트 — OCR 추출본\n\n")
        f.write("\n---\n\n".join(results))

    print(f"\n완료! → {output_file}", flush=True)

asyncio.run(main())
