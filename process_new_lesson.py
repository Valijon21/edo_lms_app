import os
import sys
import argparse
import subprocess
import urllib.request
import logging
from pathlib import Path

# Load core logging configuration
from core.logging_setup import setup_logging

# Initialize logging for this script
setup_logging("process_new_lesson.log")
logger = logging.getLogger("process_new_lesson")

# Kerakli kutubxonalarni tekshirib o'rnatamiz
def install_and_import(package, install_name=None):
    try:
        __import__(package)
    except ImportError:
        inst_name = install_name or package
        logger.info(f"Kutubxona o'rnatilmoqda: {inst_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", inst_name])
        except Exception as e:
            logger.exception(f"Kutubxonani o'rnatishda xatolik yuz berdi ({inst_name}): {e}")
            raise

install_and_import("yt_dlp", "yt-dlp")
install_and_import("cv2", "opencv-python")
install_and_import("youtube_transcript_api")
install_and_import("dotenv", "python-dotenv")

import yt_dlp
import cv2
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig

# Loyiha papkalari
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def get_free_proxies():
    """YouTube cheklovlarini aylanib o'tish uchun bepul proksilarni yuklab olish."""
    logger.info("YouTube IP blokini chetlab o'tish uchun bepul proksilarni yuklab olamiz...")
    try:
        url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read().decode("utf-8")
        proxies = [line.strip() for line in content.split("\n") if line.strip()]
        logger.info(f"Jami {len(proxies)} ta bepul proksilar topildi.")
        return proxies[:15]
    except Exception as e:
        logger.error(f"Bepul proksilarni yuklab olishda xatolik: {e}")
        return []


def download_audio_only(url, output_path):
    """YouTube-dan faqat audio formatni eng kichik hajmda yuklab olish."""
    logger.info(f"YouTube-dan audio oqimni yuklab olish boshlandi: {url}")
    if output_path.exists():
        try:
            output_path.unlink()
        except Exception:
            pass

    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "outtmpl": str(output_path.with_suffix("")),  # Extension avtomat qo'shiladi
        "quiet": True,
        "nocheckcertificate": True,
    }
    # Avval cookies.txt-ni tekshiramiz
    cookie_file = BASE_DIR / "cookies.txt"
    if cookie_file.exists():
        ydl_opts["cookiefile"] = str(cookie_file)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        logger.error(f"Audioni yuklab bo'lmadi: {e}")
        return False


def transcribe_local_audio_whisper(audio_or_video_path, output_txt_path):
    """faster-whisper modelini ishga tushirib, local audio/videoni o'zbekcha matnga aylantirish."""
    # faster-whisper-ni tekshirib o'rnatamiz
    install_and_import("faster_whisper", "faster-whisper")
    from faster_whisper import WhisperModel

    logger.info("[AI ASR] faster-whisper modeli yuklanmoqda (model: base)...")
    try:
        # CPU-da juda tez va kam xotira bilan ishlashi uchun 'base' (140MB) va 'int8' ishlatamiz
        model = WhisperModel("base", device="cpu", compute_type="int8")
        logger.info("[AI ASR] Nutqni matnga aylantirish boshlandi. Iltimos kuting...")
        
        segments, info = model.transcribe(str(audio_or_video_path), beam_size=5, language="uz")
        
        output_txt_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_txt_path, "w", encoding="utf-8") as f:
            for segment in segments:
                minutes = int(segment.start // 60)
                seconds = int(segment.start % 60)
                f.write(f"[{minutes:02d}:{seconds:02d}] {segment.text}\n")
                
        logger.info(f"[AI ASR] Transkript muvaffaqiyatli saqlandi: {output_txt_path}")
        return True
    except Exception as e:
        logger.exception(f"[AI ASR] Ovozni matnga o'girishda xatolik yuz berdi: {e}")
        return False


def fetch_transcript(video_id, output_txt_path):
    """YouTube API orqali transkriptni yuklash (agar u mavjud bo'lsa)."""
    logger.info(f"Video transkriptini YouTube API-dan yuklash boshlandi (ID: {video_id})...")
    proxy_url = os.getenv("PROXY_URL")
    transcript_list = None

    # 1. .env proksini tekshirish
    if proxy_url:
        logger.info(f".env faylidagi proksidan foydalanilmoqda: {proxy_url}")
        try:
            proxy_config = GenericProxyConfig(http_url=proxy_url, https_url=proxy_url)
            transcript_list = YouTubeTranscriptApi(proxy_config=proxy_config).fetch(
                video_id, languages=["uz", "ru", "en"]
            )
        except Exception as e:
            logger.warning(f".env proksisi xatolik berdi: {e}")

    # 2. Bepul proksilar rotatsiyasi
    if not transcript_list:
        free_proxies = get_free_proxies()
        for proxy in free_proxies:
            proxy_address = f"http://{proxy}"
            try:
                proxy_config = GenericProxyConfig(http_url=proxy_address, https_url=proxy_address)
                transcript_list = YouTubeTranscriptApi(proxy_config=proxy_config).fetch(
                    video_id, languages=["uz", "ru", "en"]
                )
                logger.info(f"Muvaffaqiyatli yuklandi (Proksi: {proxy_address})!")
                break
            except Exception:
                pass

    # 3. To'g'ridan-to'g'ri bog'lanish
    if not transcript_list:
        try:
            transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=["uz", "ru", "en"])
        except Exception:
            pass

    if transcript_list:
        # Faylga yozamiz
        output_txt_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_txt_path, "w", encoding="utf-8") as f:
            for entry in transcript_list:
                text = entry.text
                start = entry.start
                minutes = int(start // 60)
                seconds = int(start % 60)
                f.write(f"[{minutes:02d}:{seconds:02d}] {text}\n")
        logger.info(f"Transkript API orqali yuklandi va saqlandi: {output_txt_path}")
        return True

    logger.warning("YouTube API orqali transkript topilmadi (subtitr yo'q yoki IP bloklangan).")
    return False


def download_video(url, output_path):
    """Proksi va kukilarni aylanib o'tish bilan videoni 720p yuklash."""
    logger.info(f"YouTube videoni 720p sifatda yuklab olish boshlandi: {url}")
    if output_path.exists():
        try:
            output_path.unlink()
        except Exception:
            pass

    # Cookies.txt tekshirish
    cookie_file = BASE_DIR / "cookies.txt"
    if cookie_file.exists():
        logger.info("Loyiha papkasidagi cookies.txt fayli ishlatilmoqda...")
        ydl_opts = {
            "format": "best[height<=720]/bestvideo[height<=720]+bestaudio/best",
            "outtmpl": str(output_path.with_suffix("")),
            "merge_output_format": "mp4",
            "quiet": False,
            "cookiefile": str(cookie_file),
            "nocheckcertificate": True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            logger.warning(f"cookies.txt orqali yuklash o'xshamadi: {e}")

    # Brauzer kukilari
    browsers = ["chrome", "edge", "firefox", "opera"]
    for browser in browsers:
        logger.info(f"Browser cookies orqali yuklashga urinib ko'ramiz: {browser}")
        ydl_opts = {
            "format": "best[height<=720]/bestvideo[height<=720]+bestaudio/best",
            "outtmpl": str(output_path.with_suffix("")),
            "merge_output_format": "mp4",
            "quiet": True,
            "cookiesfrombrowser": (browser,),
            "nocheckcertificate": True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            logger.info(f"Muvaffaqiyatli yuklandi! Ishlatilgan brauzer: {browser}")
            return True
        except Exception:
            pass

    # Proksilar rotatsiyasi
    logger.info("Brauzer cookies orqali yuklab bo'lmadi. Bepul proksilar rotatsiyasini boshlaymiz...")
    free_proxies = get_free_proxies()
    for proxy in free_proxies:
        proxy_address = f"http://{proxy}"
        ydl_opts = {
            "format": "best[height<=720]/bestvideo[height<=720]+bestaudio/best",
            "outtmpl": str(output_path.with_suffix("")),
            "merge_output_format": "mp4",
            "quiet": True,
            "proxy": proxy_address,
            "socket_timeout": 15,
            "nocheckcertificate": True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            logger.info(f"Muvaffaqiyatli yuklandi! Ishlatilgan proksi: {proxy_address}")
            return True
        except Exception:
            pass

    # Oxirgi chora
    logger.info("To'g'ridan-to'g'ri cookies-siz urinib ko'ramiz...")
    try:
        ydl_opts = {
            "format": "best[height<=720]/bestvideo[height<=720]+bestaudio/best",
            "outtmpl": str(output_path.with_suffix("")),
            "merge_output_format": "mp4",
            "quiet": False,
            "nocheckcertificate": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        logger.error(f"Videoni yuklab bo'lmadi: {e}")
        return False


def extract_keyframes(video_path, output_dir, interval_seconds):
    """Videodan kadrlarni ajratib olish va alohida papkaga saqlash."""
    logger.info(f"Videodan kadrlar (skrinshotlar) ajratib olish boshlandi: {video_path}")
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        logger.error("Xatolik: Videoni ochib bo'lmadi!")
        return False

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    logger.info(f"Video parametrlari: FPS: {fps:.2f}, Jami kadrlar: {total_frames}, Davomiyligi: {duration:.2f} soniya")

    saved_count = 0
    for sec in range(0, int(duration), interval_seconds):
        frame_id = int(sec * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = cap.read()

        if ret:
            filename = f"frame_{sec:03d}s.jpg"
            filepath = output_dir / filename
            cv2.imwrite(str(filepath), frame, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
            logger.info(f"Kadr saqlandi: {filename} (Vaqt: {sec}s)")
            saved_count += 1

    cap.release()
    logger.info(f"Ajratish yakunlandi. Jami {saved_count} ta rasm {output_dir} papkasida saqlandi.")
    return True


def main():
    parser = argparse.ArgumentParser(description="Yangi dars ma'lumotlarini avtomat tahlil qilish skripti (ASR Whisper bilan).")
    parser.add_argument("--slug", required=True, help="Darsning unikal nomi (masalan: chiquvchi_hujjatlar). Papkalar shu nomda bo'ladi.")
    parser.add_argument("--yt-url", help="YouTube video havolasi (ixtiyoriy).")
    parser.add_argument("--video-file", help="Loyihaga tashlangan local video fayli nomi (masalan: chiquvchi.mp4).")
    parser.add_argument("--interval", type=int, default=10, help="Skrinshotlar orasidagi vaqt (soniya). Standart: 10")

    args = parser.parse_args()
    slug = args.slug.strip().lower()

    # Papkalarni yaratamiz (Har bir dars uchun ALOHIDA nomlar sohasi / namespace)
    lesson_media_dir = BASE_DIR / "media" / "courses" / slug
    lesson_media_dir.mkdir(parents=True, exist_ok=True)
    transcript_file = BASE_DIR / "media" / "transcripts" / f"{slug}_transcript.txt"

    # local video faylni aniqlash
    local_video_path = None
    if args.video_file:
        candidate = BASE_DIR / args.video_file
        if candidate.exists():
            local_video_path = candidate
    if not local_video_path:
        for name in [f"{slug}.mp4", "video.mp4", "kiruvchi.mp4"]:
            candidate = BASE_DIR / name
            if candidate.exists():
                local_video_path = candidate
                break

    # 1. Transkriptni olish (YouTube API yoki Local Whisper orqali)
    transcript_success = False

    # A. YouTube API orqali urinib ko'ramiz
    if args.yt_url:
        video_id = None
        if "v=" in args.yt_url:
            video_id = args.yt_url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in args.yt_url:
            video_id = args.yt_url.split("youtu.be/")[1].split("?")[0]

        if video_id:
            transcript_success = fetch_transcript(video_id, transcript_file)

    # B. Agar transkript yuklanmagan bo'lsa, local audio/video orqali Whisper yordamida yaratamiz!
    if not transcript_success:
        logger.info("YouTube API transkripti topilmadi. Mahalliy sun'iy intellekt (ASR faster-whisper) orqali transkripsiyani boshlaymiz...")
        
        # Ovoz beruvchi fayl
        audio_source = None
        temp_audio = None
        if local_video_path and local_video_path.exists():
            audio_source = local_video_path
        elif args.yt_url:
            # Agar local video bo'lmasa, faqat audioni yuklab olamiz
            temp_audio = BASE_DIR / f"temp_audio_{slug}.m4a"
            if download_audio_only(args.yt_url, temp_audio):
                audio_source = temp_audio

        if audio_source and audio_source.exists():
            transcript_success = transcribe_local_audio_whisper(audio_source, transcript_file)
            
            # Vaqtinchalik audio faylni o'chiramiz
            if audio_source == temp_audio and temp_audio.exists():
                try:
                    os.remove(temp_audio)
                    logger.info("Vaqtinchalik yuklangan audio oqim o'chirildi.")
                except Exception as e:
                    logger.warning(f"Vaqtinchalik audio faylni o'chirishda xatolik: {e}")
        else:
            logger.error("Nutqni matnga o'girish uchun video yoki audio fayl manbai topilmadi!")

    # 2. Videodan skrinshotlar ajratish
    temp_video = BASE_DIR / f"temp_{slug}.mp4"
    if not local_video_path and args.yt_url:
        # Agar local video bo'lmasa va skrinshot kerak bo'lsa, uni yuklab olamiz
        if download_video(args.yt_url, temp_video):
            local_video_path = temp_video

    if local_video_path and local_video_path.exists():
        extract_keyframes(local_video_path, lesson_media_dir, args.interval)
        # Vaqtinchalik faylni o'chirish
        if local_video_path == temp_video and temp_video.exists():
            try:
                os.remove(temp_video)
                logger.info("Vaqtinchalik yuklangan video fayl o'chirildi.")
            except Exception as e:
                logger.warning(f"Vaqtinchalik video faylni o'chirishda xatolik: {e}")
    else:
        logger.warning("Skrinshotlarni ajratish uchun video topilmadi!")

    logger.info("=== JARAYON YAKUNLANDI ===")
    logger.info(f"1. Rasmlar papkasi: {lesson_media_dir}")
    logger.info(f"2. Transkript fayli: {transcript_file if transcript_file.exists() else 'Yaratilmadi'}")


if __name__ == "__main__":
    main()
