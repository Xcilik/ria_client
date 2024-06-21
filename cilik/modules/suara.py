import speech_recognition as sr
from pydub import AudioSegment

from cilik.core.database import add_top_cmd
from cilik.core.handler import CILIK


def convert_audio_to_text(audio_file, language):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language=language)
            return text
        except sr.UnknownValueError:
            return "Tidak dapat mengenali suara."
        except sr.RequestError as e:
            return f"Terjadi kesalahan pada layanan Google: {str(e)}"


# Fungsi untuk mengonversi file suara menjadi teks dalam bahasa tertentu
@CILIK.UBOT("totext", SUDO=True)
async def anuan(client, message):
    await add_top_cmd(message.command[0])
    results = []
    rep = message.reply_to_message
    if not rep:
        return await message.reply("**Reply to voice or media!**")
    if rep.text or rep.sticker:
        return await message.reply("**Reply to voice or media!**")
    else:
        msg = await message.reply("<code>Converting to Text...</code>")
        audio_file = await rep.download(file_name="audio.ogg")
        supported_languages = ["id-ID"]  # Menambahkan bahasa Indonesia (id-ID)

        # Mengonversi file suara ke format WAV
        wav_audio_file = "audio.wav"
        audio = AudioSegment.from_file(audio_file)
        audio.export(wav_audio_file, format="wav")

        for lang in supported_languages:
            text = convert_audio_to_text(wav_audio_file, lang)
            results.append(f"<code>{text}</code>")

        response_text = "\n\n".join(results)
        await message.reply_text(
            f"<b>Hasil konversi suara ke teks:</b>\n\n{response_text}"
        )
        await msg.delete()
