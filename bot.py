from src.openai_service.open_ai import get_ai_response, announce_ai_response
from src import stt_google_free
from src.websocket.controller import act
from src.azure_service.text_to_speech import TextToSpeech
from src.play_instrument import play_sound

import asyncio



class Vtuber:
    def __init__(self):
        self.text_to_speech = TextToSpeech()
        self.messages = []

    def run(self):
        self.conversation()

    # 악기를 연주해달라는 내용이 있으면 바로 악기 연주
    def check_listen_instrument(self, user_content):
        without_spaces = user_content.replace(" ", "")
        keyword = "악기연주해줘"
        return keyword in without_spaces
    
    # 마법을 보여달라고 하면 거기에 맞춰 동작
    def check_magic(self, user_content):
        without_spaces = user_content.replace(" ", "") # 띄어쓰기 제거
        keywords = ["마법보여줘", "마법한번보여줘", "마술보여줘", "마술한번부려봐","마술한번해봐"]
        return any(keyword in without_spaces for keyword in keywords)

    async def conversation(self):

        while True:
            try:
                user_content = stt_google_free.stt_google()
                print(f"user : {user_content}")

                # GPT 입력 형식을 맞추기 위한 용도
                self.messages.append({"role": "user", "content": user_content})

                if(self.check_listen_instrument(user_content)):
                    assistant_content = "아직 이것 밖에 할 줄 모르지만, 이 곡이라도 연주해볼게."
                    print(f"MAO : {assistant_content}")

                    await self.print_tts_sound(assistant_content, user_content)
                    await act(system_message="play")
                    play_sound(f"musics/달빛에그려지는.WAV")
                else:
                    assistant_content = get_ai_response(self.messages)
                    print(f"MAO : {assistant_content}")
                    await self.print_tts_sound(assistant_content, user_content)
                    await act(system_message="rollback")

            except Exception as e:
                print(e)

    async def print_tts_sound(self, assistant_content, user_content=""):
        # pitch : 음의 높낮이
        # rate : 빠르기
        tts_task = asyncio.create_task(self.text_to_speech.speak(assistant_content, pitch='+15%', rate="+25%"))
        if(self.check_magic(user_content)):
            await act(system_message="magic")
        else:
            await act(system_message="talk")
        await tts_task  # TTS 출력을 기다림
        self.is_speak = False
        
        # 이게 있어야 GPT 답변을 토대로 기억함.
        self.messages.append({"role": "assistant", "content": assistant_content})